from django.urls import path
from .views import(
    HomeView, RegistUserView, UserLoginView,     
    UserLogoutView, UserView,  AuthorityView,
    Use_MisoView, Used_MisoView,ProductListView, ProductRegistrationView,
    EditUseView, DeleteUseView, EditUsedView, DeleteUsedView, 
    MyPageView, CustomPasswordChangeView,   MyFavoriteView, ToggleFavoriteView,
    SaveAsUsedView
)

from . import views


app_name = 'accounts'
urlpatterns =[
    path('',UserLoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/', UserView.as_view(), name='user'),
    path('authority/', AuthorityView.as_view(), name='authority'),
    path('use_miso/', Use_MisoView.as_view(), name='use_miso'),
    path('used_miso/', Used_MisoView.as_view(), name='used_miso'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('product_registration/', ProductRegistrationView.as_view(), name='product_registration'),
    path('my_page/', MyPageView.as_view(), name='my_page'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('use_miso/<int:pk>/edit/', EditUseView.as_view(), name='edit_use'),
    path('use_miso/<int:pk>/delete/', DeleteUseView.as_view(), name='delete_use'),
    path('used_miso/<int:pk>/edit/', EditUsedView.as_view(), name='edit_used'),
    path('used_miso/<int:pk>/delete/', DeleteUsedView.as_view(), name='delete_used'),
    path('toggle_favorite/<int:pk>/', MyPageView.as_view(), name='toggle_favorite'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('toggle_favorite/<int:pk>/', ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('my_favorite/', MyFavoriteView.as_view(), name='my_favorite'),
    path('save_as_used/<int:pk>/', SaveAsUsedView.as_view(), name='save_as_used'),
#     path('add_to_favorites/<int:pk>/', ToggleFavoriteView.as_view(), name='add_to_favorites'),
 ]

    



