from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm

urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('about/',AboutView.as_view(),name="about"),
    path('contact/',ContactView.as_view(),name="contact"),
    path('category/<slug:val>',views.Category.as_view(),name="category"),
    path('product-detail/<int:pk>',views.ProductDetail.as_view(),name="product-detail"),
    path('category-title/<val>',views.CategoryTitle.as_view(),name="category-title"),
    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('address/',views.ProfileView.as_view(),name="address"),
    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),
    path('removecart/',views.remove_cart),
    path('cart/',views.show_cart,name="showcart"),
    path('checkout/',views.Checkout.as_view(),name="checkout"),
    path('status/',views.show_orders,name="status"),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouse/<int:warehouse_id>/', views.warehouse_detail, name='warehouse_detail'),
    path('warehouse/create/', views.warehouse_create, name='warehouse_create'),
    #login
    path('registration',views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm ),name='login'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'), name="logout"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
