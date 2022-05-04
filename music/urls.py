from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.Song_player, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('Albums/', views.Albums, name='Albums'),
    path('Albums_songs/<name>/', views.Albums_songs, name='AlbumsSongs'),
    path('Artist/', views.Artists, name='Artist'),
    path('Artist_songs/<name>/', views.Artist_songs, name='ArtistSongs'),
    path('search/', views.search, name='search'),
    path('edit/', views.update_profile, name='edit'),
    path('profile/', views.profile, name='profile'),
    path('songs/', views.songs, name='songs')

]