from email.headerregistry import Address
from django.shortcuts import render, redirect
from .models import Song, Album, Artist, Profile
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .forms import ProfileForm, UserForm
from django.db import transaction
from django.contrib import messages

# Create your views here.
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form = user_form.save()
            profile_form = profile_form.save()
            return redirect('home')
        else:
            return redirect('edit')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': ProfileForm
    }
    return render(request, 'create.html', context)


def search(request):
    songs = Song.objects.all()
    query = request.GET.get("search")
    if query is not None:
        songs = songs.filter(song__icontains=query)
        if songs:
            return render(request, 'search_view.html', {'songs': songs})
        elif songs:
            songs = songs.filter(artist__name__icontains=query)
            return render(request, 'home.html', {'songs': songs})
        elif songs:
            songs = songs.filter(album__album_title=query)
            return render(request, 'home.html', {'songs': songs})
        else:
            messages.error(request,"entered info not valid !")
            return redirect('home')
    else:
        return redirect('home')


def signup(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST.get('username')
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error': 'Username  has already been taken'})
            elif User.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error': 'email has already been taken'})
            
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                return redirect('login')
        else:
            return render(request, 'signup.html', {'error': 'Password does not match'})
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['login_username'], password=request.POST['password1'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Password or username  not match'})
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
    return render(request, 'home.html')


def Albums(request):
    albums = Album.objects.all()
    return render(request, 'Albums.html', {'Albums': albums})


def Albums_songs(request, name):
    musics = Song.objects.filter(album__album_title=name)
    return render(request, 'Albums_songs.html', {'Musics': musics})


def Song_player(request):
    songs = Song.objects.all()
    return render(request, 'home.html', {'songs': songs})


def Artists(request):
    artists = Artist.objects
    return render(request, 'Artist.html', {'Artists': artists})


def Artist_songs(request, name):
    artist = Song.objects.filter(artist__name=name)
    return render(request, 'Artist_songs.html', {'Artist': artist})

def profile(request):
    return render(request,'profile.html')

def songs(request):
    songs=Song.objects.all()
    return render(request,'songs.html',{'songs':songs})
@property
def full_name(self):
    return "%s %s" % (self.user.first_name, self.user.last_name)