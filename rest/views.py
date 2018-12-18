from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse


from rest.serializers import PostSerializer, UserSerializer
from rest.permissions import IsOwnerOrReadOnly
from blog.models import Post

#Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('Users', request=request, format=format),
        'posts': reverse('Posts', request=request, format=format)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# def UsersView(request):
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, context={'request': request}, many=True)
        
#         return JsonResponse(serializer.data, safe=False)
    
    

# def UserDetails(request, post_id):
#     if request.method == 'GET':
#         posts = Post.objects.get(pk=post_id)
#         serializer = PostSerializer(posts, context={'request': request})
        
#         return JsonResponse(serializer.data, safe=False)

  ########################
# USING api_view DECORATOR #
  ########################

# @api_view(['GET', 'POST'])
# def posts_list(request, format=None):
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
        
#         return Response(serializer.data)

#     elif request.method == 'POST':
        # serializer = PostSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def post_details(request, post_id, format=None):
#     try:
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = PostSerializer(post)

#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = PostSerializer(post, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         post.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)

  ########################
# USING api_view DECORATOR #
#           END            #
  ########################

  ##############################
# USING APIView Class-based View #
  ##############################

# class PostsList(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
        
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PostDetails(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
#     def get(self, request, post_id, format=None):
#         serializer = PostSerializer(self.get_object(post_id))

#         return Response(serializer.data)

#     def put(self, request, post_id, format=None):
#         serializer = PostSerializer(self.get_object(post_id), data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

#     def delete(self, request, post_id, format=None):
#         self.get_object(post_id).delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)

  ##############################
# USING APIView Class-based View #
#               END              #
  ##############################

  ############
# USING mixins #
  ############

# class PostsList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class PostDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

    
  ############
# USING mixins #
#     END      #
  ############



# class PostsList(generics.ListCreateAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class PostDetails(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class UsersList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetails(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



