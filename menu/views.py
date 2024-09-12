from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpRequest
from menu.models import MenuItem


def get_menu_items(request: HttpRequest):
    menu_id = request.GET.get('menu_id')
    if menu_id:
        items = MenuItem.objects.filter(menu_id=menu_id).values('id', 'title')
        return JsonResponse(list(items), safe=False)
    return JsonResponse([], safe=False)


class HomeView(TemplateView):
    template_name = 'menu/home/home.html'
