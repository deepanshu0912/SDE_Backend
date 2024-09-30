from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .models import User

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "user not found"} , status=status.HTTP_404_NOT_FOUND)
            
            if not user.check_password(password):
                return Response({"detail": "invalid password"} , status=status.HTTP_401_UNAUTHORIZED)
            

            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.exceptions import PermissionDenied

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a product to delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # Save the product with the current authenticated user as the owner
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def user_products(self, request):
        # Retrieve the products of the currently authenticated user
        user_products = Product.objects.filter(user=request.user)
        serializer = self.get_serializer(user_products, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Override the destroy method to check if the user is the owner of the product
        product = self.get_object()
        if product.user != request.user:
            raise PermissionDenied("You do not have permission to delete this product.")
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Allow any user to view the product list and product details
            permission_classes = [permissions.AllowAny]
        elif self.action == 'destroy':
            # Only the owner can delete the product
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:
            # For create, update, etc., require authentication
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
