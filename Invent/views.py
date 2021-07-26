from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Invent.models import Items, QR
from .serializer import ItemSerializer
from .serializer import UserSerializer, LoginSerializer, CreateItemSerializer, ListSerializer


class UserRegistration(APIView):
    # Class for user registration.
    def post(self, request):
        Serialized_data = UserSerializer(data=request.data)
        if Serialized_data.is_valid(raise_exception=True):
            Serialized_data.save()
            return Response(Serialized_data.data)


class Login(APIView):
    # class for user login
    def post(self, request, *args, **kwargs):
        my_data = request.data
        serialized_data = LoginSerializer(data=my_data)
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            data = serialized_data.data
            del data['password']
            return Response(data)


class ItemManager(APIView):
    # class for item  to create, update and get list(quantity=0) of items.

    permission_classes=[IsAuthenticated]
    def post(self, request):
        user = request.user.id
        Serialized_data = CreateItemSerializer(data=request.data, context=request)
        if Serialized_data.is_valid(raise_exception=True):
            Serialized_data.save()
            return Response(Serialized_data.data)

    def patch(self, request, id):
        item = Items.objects.filter(id=id)
        if not item.exists():
            return Response({"data": "Item doesn't exists."})
        serialized_data = CreateItemSerializer(data=request.data, instance=item[0])
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            return Response(serialized_data.data)

    def get(self, request, id):
        item = Items.objects.filter(user=id, quantity="0")
        serialized_data = ListSerializer(item, many=True)
        return Response(serialized_data.data)


class QR_Item(APIView):
    # class to create a QR code for already created Item.

    def get(self, request, id):
        qr_name = "Welcome to"
        qr_obj = QR.objects.filter(id=id)[0]
        context = {
            'name': qr_name,
            'obj': qr_obj,
        }
        return render(request, 'home.html', context)


class ItemViewSet(ModelViewSet):
    # class for CRUD operation on Item.

    serializer_class = ItemSerializer
    queryset = Items.objects.all()
