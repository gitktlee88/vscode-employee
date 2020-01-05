from rest_framework import generics, mixins
from django.db.models import Q

from pages.models import BlogPost
from .permission import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer
# serializer = BlogPostSerializer()
# print(repr(serializer))

# Create & List & Search
class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field      = 'pk' # slug, id # (?p<pk>\d+)
    serializer_class  = BlogPostSerializer

    # "detail": "Authentication credentials were not provided."
    # permission_classes = []  # open to all users

    # search function like
    # http://localhost:8000/api/pages/?q=pages post
    def get_queryset(self, **kwargs):  # can be used in ListView
        # original qs
        qs = BlogPost.objects.all()
        # print(qs.filter(name__startswith=self.kwargs['hello']))
        query = self.request.GET.get("q")
        # print(query)
        if query is not None:   # then, do filtering with query
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)
                ).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create( request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk=pk)

# Retrieve Update Delete
class BlogPostRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field      = 'pk' # slug, id # (?p<pk>\d+)
    #queryset                = BlogPost.objects.all()
    serializer_class  = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]


    def get_queryset(self):
        return BlogPost.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk=pk)



from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

class CreateUserView(CreateModelMixin, GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
