from django.urls import path
from .views import main, form, uploader, detail, top_kp


urlpatterns = [
    path('', main, name='home'),
    path('form', form, name='add_new'),
    path('uploader/<str:uploader_id>', uploader, name='by_uploader'),
    path('detail/<int:doc_id>', detail, name='detail'),
    path('top', top_kp, name='top_kp'),
]
