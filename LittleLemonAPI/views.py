from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from .models import Category
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer


# Create your views here.

'''
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
'''


@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response({'data':serialized_item.data}, template_name='menu-items.html')


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)

@api_view(['GET', 'POST'])
def menu_items(request):
    if(request.method == "GET"):
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        search = request.query_params.get('search')
        to_price = request.query_params.get('to_price')
        if(category_name):
            items = items.filter(category__title=category_name)
        if(to_price):
            items = items.filter(price__lte=to_price)
        if(search):
            items = items.filter(title__icontains=search)
        serialized_item = MenuItemSerializer(items, many=True, context={'request': request})
        return Response(serialized_item.data)
    if(request.method == "POST"):
        serialized_item = MenuItemSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
@api_view()
def single_item(request, id):
    menu_item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(menu_item)
    return Response(serialized_item.data)