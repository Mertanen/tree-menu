from django import template
from django.template import Context
from django.urls import resolve
from django.http import HttpRequest
from menu.models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/templatetags/draw_menu.html', takes_context=True)
def draw_menu(context: Context, menu_title: str):
    request: HttpRequest = context['request']
    current_url = request.path
    item_id: int = resolve(current_url).kwargs.get('item_id')

    items = MenuItem.objects.filter(menu__title=menu_title).select_related('parent').prefetch_related('parent')

    item_dict = {item.id: item for item in items}

    active_item = item_dict.get(item_id)

    def get_ancestors(item):
        ancestors = []
        while item and item.parent_id:
            item = item_dict.get(item.parent_id)
            if item:
                ancestors.append(item)
        return ancestors

    active_ancestors = get_ancestors(active_item) if active_item else []

    def build_tree(parent=None):
        subtree = []
        for item in items:
            if item.parent_id == (parent.id if parent else None):
                subtree.append({
                    'item': item,
                    'children': build_tree(item),
                    'is_active': item == active_item or item in active_ancestors,
                })
        return subtree

    menu_tree = build_tree()

    return {
        'menu_title': menu_title,
        'items': menu_tree,
    }
