from django.shortcuts import render


def main_view(request):
    """ Главная страница """
    return render(request, 'shop/main.html')

