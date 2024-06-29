from django.urls import path
from . import views

app_name='home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/remove/<int:product_id>/', views.CartView.as_view(), name='cart_remove'),
    path('cart/buy/', views.BuyView.as_view(), name='buy'),
    path('allproducts/', views.AllProductsView.as_view(), name='all_products'),
    path('add/<int:product_id>/', views.ProductView.as_view(), name='add'),
    path('product/<int:product_id>/', views.ProductView.as_view(), name='product'),
    path('product/review/<int:product_id>/', views.ReviewView.as_view(), name='review'),
    path('prodcut/review/delete<int:review_id>/', views.ReviewDeleteView.as_view(),name='delete_review'),
    path('user/<int:user_id>/', views.UserView.as_view(), name='user'),
]