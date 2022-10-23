from random import randrange


def generate_account_number():
    result = randrange(10000000, 100000000, 1)
    return result


def is_valid_account_number(account):
    if len(str(account)) == 8:
        return True
    return False


def pay(account):
    if account % 2 != 0 or str(account)[-1] == '0':
        print('Ошибка оплаты!')
    else:
        print('Заказ оплачен')
