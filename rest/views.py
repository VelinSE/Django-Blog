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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

