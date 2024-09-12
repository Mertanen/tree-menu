from django.urls import path

from .views import HomeView

app_name = 'menu'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<int:item_id>/', HomeView.as_view(), name='menu_item'),
]