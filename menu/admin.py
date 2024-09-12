from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Menu, MenuItem


admin.site.register(Menu)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent_link', 'menu_link')
    list_display_links = ('id', 'title',)
    list_filter = ('menu',)
    fieldsets = (
        (None, {
            'fields': (('menu', 'parent'), 'title',)
        }),
    )

    class Media:
        js = ('apps/menu/admin/menu_item_filter.js',)

    def parent_link(self, obj: MenuItem):
        if obj.parent:
            url = reverse('admin:menu_menuitem_change', args=[obj.parent.id])
            return format_html('<a href="{}">{}</a>', url, obj.parent.title)
        return '-'
    parent_link.short_description = MenuItem._meta.get_field('parent').verbose_name

    def menu_link(self, obj: MenuItem):
        url = reverse('admin:menu_menu_change', args=[obj.menu.id])
        return format_html('<a href="{}">{}</a>', url, obj.menu.title)
    menu_link.short_description = MenuItem._meta.get_field('menu').verbose_name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            menu_id = request.GET.get('menu') or request.POST.get('menu')
            if menu_id:
                try:
                    menu_id = int(menu_id)
                    kwargs['queryset'] = MenuItem.objects.filter(menu_id=menu_id)
                except (ValueError, Menu.DoesNotExist):
                    kwargs['queryset'] = MenuItem.objects.none()
            elif request.resolver_match.kwargs.get('object_id'):
                item_id = request.resolver_match.kwargs['object_id']
                menu_id = MenuItem.objects.get(pk=item_id).menu_id
                kwargs['queryset'] = MenuItem.objects.filter(menu_id=menu_id)
            else:
                kwargs['queryset'] = MenuItem.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

