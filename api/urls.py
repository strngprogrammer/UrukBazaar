from .views import DecreaseCartItemQuantity, LogoutView,SignUpView, CategoriesCreateView, CategoriesDeleteView, CategoriesDetailView, CategoriesListView, CategoriesUpdateView, LoginView,ProductCreate, ProductDelete, ProductDetail, ProductList, ProductUpdate,IsLoggedInAPI, AddToCart, get_cart, RemoveFromCart
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register/', SignUpView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/',LogoutView.as_view(),name='logout'),
    path('api/products/', ProductList.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('api/products/create/', ProductCreate.as_view(), name='product-create'),
    path('api/products/<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('api/products/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    path('api/isloggedin/', IsLoggedInAPI.as_view(), name='is-loggedin'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/categories/', CategoriesListView.as_view(), name='category_list'),
    path('api/categories/<int:pk>/', CategoriesDetailView.as_view(), name='category_detail'),
    path('api/categories/create/', CategoriesCreateView.as_view(), name='category_create'),
    path('api/categories/<int:pk>/update/', CategoriesUpdateView.as_view(), name='category_update'),
    path('api/categories/<int:pk>/delete/', CategoriesDeleteView.as_view(), name='category_delete'),
    path('api/cart/', get_cart.as_view(), name='get_cart'),
    path('api/cart/add/<int:item_id>/', AddToCart.as_view(), name='add_to_cart'),
    path('api/cart/remove/<int:item_id>/', DecreaseCartItemQuantity.as_view(), name='remove_from_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)