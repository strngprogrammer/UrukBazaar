from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from .serializers import CategoriesSerializer, RegisterSerializer , ProductSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import Product , Categories
from .serializers import ProductSerializer
# Register API
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from rest_framework.request import Request
from .tokens import create_jwt_pair_for_user


class SignUpView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid username or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProductList(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreate(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDelete(generics.DestroyAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdate(generics.UpdateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class IsLoggedInAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_superuser:

            return Response({"is_authenticated": True,"admin":True}, status=status.HTTP_200_OK)
        
        return Response({"is_authenticated": True}, status=status.HTTP_200_OK)
    
class CategoriesListView(APIView):
    """
    List all categories, or create a new Categories.
    """
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriesDetailView(APIView):
    authentication_classes = []
    permission_classes = []
    """
    Retrieve, update or delete a Categories instance.
    """
    def get_object(self, pk):
        return get_object_or_404(Categories, pk=pk)

    def get(self, request, pk, format=None):
        Categories = self.get_object(pk)
        serializer = CategoriesSerializer(Categories)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Categories = self.get_object(pk)
        serializer = CategoriesSerializer(Categories, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Categories = self.get_object(pk)
        Categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoriesCreateView(generics.CreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

class CategoriesUpdateView(APIView):
    """
    Update a Categories instance.
    """
    def get_object(self, pk):
        return get_object_or_404(Categories, pk=pk)

    def put(self, request, pk, format=None):
        Categories = self.get_object(pk)
        serializer = CategoriesSerializer(Categories, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriesDeleteView(APIView):
    """
    Delete a Categories instance.
    """
    def get_object(self, pk):
        return get_object_or_404(Categories, pk=pk)

    def delete(self, request, pk, format=None):
        Categories = self.get_object(pk)
        Categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer



class get_cart(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart = Cart.objects.filter(user=request.user).order_by('-id').first()

        if cart is None:

            cart = Cart(user=request.user)

            cart.save()


       
        cart_items = cart.items.all()


       
        cart_data = {
            'cart_id': cart.id,
            'total_price': cart.total_price,
            'items': [
                {
                    'item_id': item.item.id,
                    'item_name': item.item.name,
                    'quantity': item.quantity,
                    'price': item.item.price,
                }
                for item in cart_items
            ]
        }
        return JsonResponse(cart_data)


class AddToCart(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        cart = Cart.objects.filter(user=request.user).order_by('-id').first()
        product = get_object_or_404(Product, id=item_id)

        # Check if the item already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=product)

        if not created:
            # If the item already exists, increment its quantity
            cart_item.quantity += 1
            cart_item.save()

        # Recalculate the total price of the cart
        cart.total_price = sum(item.item.price * item.quantity for item in cart.items.all())
        cart_items = cart.items.all()
        cart.save()
        cart_data = {
            'cart_id': cart.id,
            'total_price': cart.total_price,
            'items': [
                {
                    'item_id': item.item.id,
                    'item_name': item.item.name,
                    'quantity': item.quantity,
                    'price': item.item.price,
                }
                for item in cart_items
            ]
        }
        return JsonResponse(cart_data)
        



class RemoveFromCart(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        cart = Cart.objects.filter(user=request.user).order_by('-id').first()
        product = get_object_or_404(Product, id=item_id)

        # Remove the item from the cart
        CartItem.objects.filter(cart=cart, item=product).delete()

        # Recalculate the total price of the cart
        cart.total_price = sum(item.item.price * item.quantity for item in cart.items.all())
        cart.save()

        return Response({'message': 'Item removed from cart successfully'})
    
class DecreaseCartItemQuantity(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        cart = Cart.objects.filter(user=request.user).order_by('-id').first()
        product = get_object_or_404(Product, id=item_id)

        try:
            cart_item = CartItem.objects.get(cart=cart, item=product)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()

                # Recalculate the total price of the cart
                cart.total_price = sum(item.item.price * item.quantity for item in cart.items.all())
                cart.save()
                cart_items = cart.items.all()
                cart_data = {
                    'cart_id': cart.id,
                    'total_price': cart.total_price,
                    'items': [
                        {
                            'item_id': item.item.id,
                            'item_name': item.item.name,
                            'quantity': item.quantity,
                            'price': item.item.price,
                        }
                        for item in cart_items
                    ]
                }
                return JsonResponse(cart_data)
            else:
                cart_item.delete()
                cart.save()
                cart_items = cart.items.all()
                cart_data = {
                    'cart_id': cart.id,
                    'total_price': cart.total_price,
                    'items': [
                        {
                            'item_id': item.item.id,
                            'item_name': item.item.name,
                            'quantity': item.quantity,
                            'price': item.item.price,
                        }
                        for item in cart_items
                    ]
                }
                return JsonResponse(cart_data)
        except CartItem.DoesNotExist:
            return Response({'message': 'Item not found in the cart'})