from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, action, throttle_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Snippet
from .serializers import (
    SnippetSerializer, SnippetBase, SerializerList, SnippetSerializerHyperlink, UserSerializer)
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .filter import CostomFilter
from django.conf import settings


# Create your views here.

@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """

    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, )

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """

    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotEXist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet, )
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""<------------------------------BaseSerializer View---------------------------------------->"""


@api_view(['GET'])
def snippetbaseserializer(request, pk):
    instance = Snippet.objects.get(pk=pk)
    serializer = SnippetBase(instance)
    return Response(serializer.data)


"""<------------------------------ListSerializer View---------------------------------------->"""


@api_view(['GET', 'POST'])
def snippetlistserializer(request):
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, )

    elif request.method == "POST":
        serializer = SerializerList(data=request.data, many=True)
        import pdb
        pdb.set_trace()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""<------------------------------HyperlinkedModelSerializer View ---------------------------------------->"""


@api_view(['GET', 'POST'])
def snippetlisthyperlink(request, ):
    """
    List all code snippets, or create a new snippet.
    """

    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializerHyperlink(snippets, context={'request': request}, many=True)
        return Response(serializer.data, )

    elif request.method == 'POST':
        serializer = SnippetSerializerHyperlink(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippetdetailhyperlink(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """

    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotEXist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = SnippetSerializerHyperlink(snippet, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializerHyperlink(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""<------------------------------ClassBase APIView ---------------------------------------->"""


# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#
#     def get(self, request):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SnippetDetail(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request, pk):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Using mixins:
# class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiRoot(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get(self, request, format=None):
        # import pdb
        # pdb.set_trace()
        return Response({
            'users': reverse('user-list', request=request),
            'snippets': reverse('snippet-list', request=request)
        })


# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#
#     if username is None or password is None:
#         return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
#
#     user = authenticate(username=username, password=password)
#
#     if not user:
#         return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
#
#     token, _ = Token.objects.get_or_create(user=user)
#     return Response({'token': token.key}, status=status.HTTP_200_OK)


class Login(APIView):
    """
    This is login for Token Authentication.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class Logout(APIView):
    """
    This is logout for Token Authentication.
    """

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # pagination_class = MyCustomPagination
    # permission_classes = [permissions.IsAuthenticated]
    # http_method_names = ['PUT']

    @action(detail=False, methods=['GET'])
    def my_filter(self, request):
        snippet_all = Snippet.objects.all().order_by('-id')
        serializer = SnippetSerializer(snippet_all, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def get_costom(self, request, pk):
        snippet = Snippet.objects.get(pk=pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetPermissionView(viewsets.ModelViewSet):
    """
    This is use for permissions
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListSnippet(generics.ListAPIView):
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Snippet.objects.filter(owner=user)


class ListDjangoFilter(generics.ListAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'code']


class ListCustomFilter(generics.ListAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [CostomFilter]


@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def example_view(request):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)


from rest_framework.schemas.openapi import AutoSchema
from rest_framework.exceptions import APIException