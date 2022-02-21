from http import server
from os import stat
from shutil import move
from django.forms import ValidationError
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from watchlist_app.models import Reviews, WatchList, StreamPlatForm
from watchlist_app.api.serializers import WatchListSerializers, StreamPlatformSerializers, ReviewSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Using concrete view classes


class UserReview(generics.ListAPIView):
    #queryset = Reviews.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializers
    #throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Reviews.objects.filter(review_user__username=username)

    # Filters
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Reviews.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):

    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Reviews.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Reviews.objects.filter(
            watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed the movie!")

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    #queryset = Reviews.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializers
    #throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    #throttle_scope = 'review-detail'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


# Using mixins
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializers

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args ,**kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):

#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializers

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


#Creating generics watchlist class for testing purpose
#Searching api
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializers
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']



class WatchListAV(APIView):

    def get(self, request):
        movies = WatchList.objects.all()
        serializers = WatchListSerializers(movies, many=True)
        return Response(serializers.data)

    def post(self, request):
        movie = WatchList.objects.all()
        serializers = WatchListSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


class WatchDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"Error": "Movie not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializers = WatchListSerializers(movie)
        return Response(serializers.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializers = WatchListSerializers(movie, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors())

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformListAV(APIView):

    def get(self, request):
        platforms = StreamPlatForm.objects.all()
        serializers = StreamPlatformSerializers(
            platforms, many=True, context={'request': request})
        return Response(serializers.data)

    def post(self, request):
        platforms = StreamPlatForm.objects.all()
        serializers = StreamPlatformSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)


class StreamPlatformDetailAV(APIView):

    def get(self, request, pk):
        try:
            platform = StreamPlatForm.objects.get(pk=pk)
        except StreamPlatForm.DoesNotExist:
            return Response({"Error": "Platform not found"}, status=status.HTTP_204_NO_CONTENT)

        serializers = StreamPlatformSerializers(platform)
        return Response(serializers.data)

    def put(self, request, pk):
        platform = StreamPlatForm.objects.get(pk=pk)
        serializers = StreamPlatformSerializers(platform, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)

    def delete(self, request, pk):
        platform = StreamPlatForm.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Function based views

# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializers = MovieSerializers(movies, many=True)
#         return Response(serializers.data)

#     if request.method == 'POST':
#         serializers = MovieSerializers(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)

#         else:
#             return Response(serializers.errors)

# @api_view(['GET','PUT','DELETE'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:

#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializers = MovieSerializers(movie)
#         return Response(serializers.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializers = MovieSerializers(movie, data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         else:
#             return Response(serializers.errors(), status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
