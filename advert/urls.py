from django.urls import path
from .views import ad_list, my_ads, ad_create, ad_detail, ad_edit, ad_delete, create_response, my_responses, update_response_status

urlpatterns = [
    path('', ad_list, name='ad_list'),  # главная страница со списком объявлений
    path('my-ads/', my_ads, name='my_ads'),
    path('create/', ad_create, name='ad_create'),
    path('<int:pk>/', ad_detail, name='ad_detail'),
    path('<int:pk>/edit/', ad_edit, name='ad_edit'),
    path('<int:pk>/delete/', ad_delete, name='ad_delete'),
    path('<int:pk>/response/', create_response, name='create_response'),
    path('my-responses/', my_responses, name='my_responses'),
    path('response/<int:pk>/<str:status>/', update_response_status, name='update_response_status'),
]