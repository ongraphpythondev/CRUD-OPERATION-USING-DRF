from django.urls import path
from watchlist_app.api import views
urlpatterns = [
    # function based views
    # path('list/', views.movie_list, name='movie-list'),
    # path('<int:pk>', views.movie_detail, name='movie-detail'),
    path('list/', views.WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>', views.WatchDetailAV.as_view(), name='watch-detail'),
    path('list2/', views.WatchListGV.as_view(), name='watch-list'),
    path('platform/', views.StreamPlatformListAV.as_view(), name='platform-list'),
    path('platform/<int:pk>', views.StreamPlatformDetailAV.as_view(),
         name='platform-detail'),

    # path('review/', views.ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),

    path('stream/<int:pk>/review-create/',
         views.ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/review/', views.ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>/',
         views.ReviewDetail.as_view(), name='review-detail'),
     path('reviews/', views.UserReview.as_view(), name='user_reviewDetail'),
]
