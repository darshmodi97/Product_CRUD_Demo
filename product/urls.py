from django.urls import path
from product import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('create/', views.create_product, name='create-product'),
    path('create-category/', views.create_category, name='create-category'),
    path('view-data/<int:pk>/', views.view_data, name='view_model'),
    path('delete/<int:pk>/', views.delete_product, name='delete'),
    path('edit/<int:pk>/', views.edit_product, name='edit'),
    path('tag/<slug:slug>/', views.tag_filter, name='tag'),

]
