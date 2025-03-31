from django.urls import path
from . import views
urlpatterns = [
    path('',views.home_view,name='home'),
    path('main/',views.main_view,name='main'),
    path('addmenu/',views.add_menu,name='addmenu'),
    path('signup/',views.signupview,name='signup'),
    path('login/',views.signinview,name='login'),
    path('menu/',views.menulist,name='menulist'),
    path('signout/', views.signoutview, name='signout'),
    path('delete/<int:id>', views.menu_delete, name='delete'),
    path('edit/<int:id>/', views.menu_edit, name='edit'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    
]
