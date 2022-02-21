# import json
# from shutil import move
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
# from watchlist_app.models import Movie
# # Create your views here.


# #return all movies in json format
# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {
#         'movies' : list(movies.values())
#     }
#     return JsonResponse(data)

# #return specific movie from a list of all the movies
# def movie_detail(request, pk):
#     try:

#         movie = Movie.objects.get(pk=pk)
#     #print(movie)
#     except Movie.DoesNotExist:
#         return HttpResponse("Error")

#     data = {
#         'name' : movie.name,
#         'description' : movie.description,
#         'is_active' : movie.is_active,
#     }

#     return JsonResponse(data)
