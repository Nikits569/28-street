from .models import *
from django.http import HttpResponseForbidden
import urllib.parse
import json
from django.conf import settings

cookie_value = "%7B%22user%22%3A+%22Alice%22%2C+%22age%22%3A+25%7D"

class LogPageTransitionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логируем каждый запрос пользователя
        print(f"User requested: {request.path}")  # Путь страницы, на которую идет запрос

        my_cookie_value = request.COOKIES.get('BOX_like_total', None)  # Второй аргумент - значение по умолчанию

        if request.path:
            if my_cookie_value is not None:
                decoded_str = urllib.parse.unquote(my_cookie_value)
                print(decoded_str)
                decoded_str = json.loads(decoded_str)
                for i in decoded_str.keys():
                    like = Base.objects.filter(slug=i).first()
                    if like:
                        print(like.name)
                        like.like = decoded_str[i]
                        like.save()
                    else:
                        print('Nothing')

            else:
                print('No cookie found')
        # Получаем ответ
        response = self.get_response(request)

        # Логируем после обработки запроса (например, статус ответа)
        print(f"Response status: {response.status_code}")

        return response



#ALLOWED_ADMIN_IPS = getattr(settings, 'ALLOWED_ADMIN_IPS', [])
#
#
#class AdminIPRestrictMiddleware:
#    def __init__(self, get_response):
#        self.get_response = get_response
#
#    def __call__(self, request):
#        # Проверяем, что запрос к админке
#        if request.path.startswith('/admin/'):
#            ip = get_client_ip(request)
#            if ip not in ALLOWED_ADMIN_IPS:
#                return HttpResponseForbidden("Доступ запрещён.")
#        return self.get_response(request)


def get_client_ip(request):
    # Получаем IP клиента из заголовков
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip