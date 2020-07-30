from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:item_name>', views.entry, name='<str:item>'),
    path("new_page", views.new_page, name='new_page'),
    path('rand', views.rand, name="rand"),
    path('edit/<str:item>', views.edit, name='edit')
]   