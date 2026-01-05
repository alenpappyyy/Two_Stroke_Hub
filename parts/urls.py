from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PartViewSet, parts_store
from . import views

router = DefaultRouter()
router.register(r'api', PartViewSet, basename='parts_api')


app_name = 'parts'   

urlpatterns = [
    path('store/', parts_store, name='parts_store'),
    path('', views.parts_list, name='parts_list'),
    path('add/', views.add_part, name='add_part'),
    path('<int:pk>/', views.part_detail, name='part_detail'),

]

urlpatterns += router.urls
