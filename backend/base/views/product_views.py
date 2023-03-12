from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Product, Review
from base.serializer import ProductSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
import requests
<<<<<<< HEAD
import pickle
=======
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

>>>>>>> 8f970115364797f34fc4d9ac477f0e7293e5980f

@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    products = Product.objects.filter(name__icontains=query)
    page = request.query_params.get('page')
<<<<<<< HEAD
    paginator = Paginator(products,16)
=======
    paginator = Paginator(products, 8)
>>>>>>> 8f970115364797f34fc4d9ac477f0e7293e5980f

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
    page = int(page)

    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getTopProducts(request):
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProduct(request):
    user = request.user
    if request.user.is_staff == False and request.user.is_superuser == False:
        message = {'detail': 'Vendor account can only access'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    product = Product.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description=''
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProduct(request, pk):
    data = request.data
    # print(request.user.is_staff)
    loginId = request.user.id
    response = requests.get(f"http://127.0.0.1:8000/api/products/{pk}/")
    productUserId = response.json()['user']
    # print(response.json()['user'])
    if (loginId != productUserId and request.user.is_superuser == False):
        message = {'detail': 'Vendor account can only access'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    product = Product.objects.get(_id=pk)
    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProduct(request, pk):
    loginId = request.user.id
    response = requests.get(f"http://127.0.0.1:8000/api/products/{pk}/")
    productUserId = response.json()['user']
    print(productUserId)
    print(loginId)
    if (loginId != productUserId and request.user.is_superuser == False):
        message = {'detail': 'You cannot delete this product'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Product Deleted')


@api_view(['POST'])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data

    # 1 - Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review Added')
<<<<<<< HEAD
    
similarity = pickle.load(open('similarity.pkl', 'rb'))


@api_view(['GET'])
def recommend(request,pk):
    product = Product.objects.get(_id=pk)
    distances = similarity[product._id-1]
    product_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]
    productList = Product.objects.none()
    for i in product_list:
        products = Product.objects.filter(_id=(i[0]+1))
        print(products)
        productList |= products
    

    serializer = ProductSerializer(productList, many = True)
    return Response(serializer.data)
=======


class API(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # filterset_fields = ['category']

    def get_queryset(self):
        return Product.objects.order_by('?').all()[:10]
>>>>>>> 8f970115364797f34fc4d9ac477f0e7293e5980f
