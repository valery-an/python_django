from django.contrib import messages
from django.db.models import Min, Max, Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from app_shop.models import Shop, Category, Product

from services.review import ProductReview
from services.viewed_products import History


class MainView(TemplateView):
    """ Главная страница """
    template_name = 'shop/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_categories = Category.objects.filter(is_active=True).order_by('?').annotate(price_min=Min('products__price'))[:3]
        products = Product.objects.filter(amount__gte=1).defer('description', 'parameters')
        popular_products = products.annotate(num_orders=Count('order_items')).order_by('-num_orders')[:8]
        limited_products = products.order_by('amount')[:16]
        context['selected_categories'] = selected_categories
        context['popular_products'] = popular_products
        context['limited_products'] = limited_products
        return context


class ProductListView(ListView):
    """
    Страница каталога товаров из выбранной категории товаров
    с возможностью применения фильтров и добавления товара в корзину
    """
    template_name = 'shop/catalog.html'
    paginate_by = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.products = None
        self.shops = None
        self.price_range = None

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, name=self.kwargs['category'])
        self.products = Product.objects.filter(category=category, amount__gte=1).defer('description', 'parameters')
        shop_ids = self.products.values_list('shop', flat=True)
        self.shops = Shop.objects.filter(id__in=shop_ids).only('name')
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = self.products.annotate(reviews_amount=Count('reviews'), orders_amount=Count('order_items'))
        price_range = self.request.GET.get('price')
        if price_range:
            price_range = price_range.split(';')
            queryset = queryset.filter(price__gte=int(price_range[0]), price__lte=int(price_range[1]))
            self.price_range = price_range
        name = self.request.GET.get('title')
        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(description__icontains=name))
        shops = self.request.GET.getlist('shops')
        if shops:
            queryset = queryset.filter(shop__name__in=shops)
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        sort = self.request.GET.get('sort', 'ascending')
        if sort == 'ascending':
            return ordering
        else:
            return f'-{ordering}'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.products
        min_price = products.aggregate(Min('price'))['price__min']
        max_price = products.aggregate(Max('price'))['price__max']
        if self.price_range:
            price_from = int(self.price_range[0])
            price_to = int(self.price_range[1])
        else:
            price_from = min_price
            price_to = max_price
        ordering = self.get_ordering()
        if ordering and ordering.startswith('-'):
            sort_class = 'Sort-sortBy_inc'
            ordering = ordering[1:]
        else:
            sort_class = 'Sort-sortBy_dec'
        context[f'{ordering}_sort'] = sort_class
        context['min_price'] = min_price
        context['max_price'] = max_price
        context['price_from'] = price_from
        context['price_to'] = price_to
        context['shops'] = self.shops
        return context


class ProductHistoryListView(ListView):
    """
    Страница просмотренных пользователем товаров
    с возможностью добавления товара в корзину
    """
    template_name = 'shop/product_history.html'
    context_object_name = 'products_list'

    def get_queryset(self):
        return History(self.request.user).get_products(products_number=8)


class ProductDetailView(DetailView):
    """
    Страница детальной информации о товаре с возможностью
    добавления товара в корзину и добавления к нему отзыва
    """
    model = Product
    template_name = 'shop/product.html'
    reviews_template = 'shop/reviews.html'

    def get(self, request, *args, **kwargs):
        history = History(request.user)
        history.add_product(self.get_object())
        history.delete_products()
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            self.template_name = self.reviews_template
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = self.object.images.all()
        parameters = self.object.parameters.split('\n')
        product = ProductReview(self.object)
        context['images'] = images
        context['parameters'] = parameters
        context['reviews'] = product.get_reviews()
        context['reviews_amount'] = product.get_reviews_amount()
        context['reviews_template'] = self.reviews_template
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        review = request.POST.get('review')
        if review and len(review) > 10:
            product = ProductReview(self.object)
            if product.add_review(user=request.user, text=review):
                messages.success(request, 'Отзыв добавлен')
                return redirect('product', self.object.pk)
            messages.error(request, 'Вы уже оставляли отзыв на этот товар')
        else:
            messages.error(request, 'Отзыв слишком короткий')
        return render(request, self.template_name, context=context)
