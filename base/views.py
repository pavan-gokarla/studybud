from django.shortcuts import redirect, render
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from base.models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login,logout
from django.http  import HttpResponse
from django.contrib.auth.forms import  UserCreationForm

def home(request):

    q = request.GET.get('q') if  request.GET.get('q') else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q)  |  Q(name__icontains=q) |  Q(description__icontains=q) | Q(host__username__contains=q) )

    room_count = rooms.count()
    topic = Topic.objects.all();
    context = {"rooms":rooms,"topics":topic,"room_count":room_count}
    print
    return render(request,'base/home.html',context)

def room(request,pk):

    room = Room.objects.get(id=pk)
    context =  {"room":room}



    return render(request,'base/room.html',context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    context = {'page'  : page }

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request,'base/login_register.html',context)

def  logoutUser(request):
    logout(request)
    return  redirect('home')

def  registerUser(request):
    form = UserCreationForm()
    context = {'form':form }
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
    return  render(request,'base/login_register.html',context)




@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form":form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def  updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user !=  room.host:
        return HttpResponse("You are not the host of this room")


    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {"form":form}
    return render(request,'base/room_form.html',context)
    

def  deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user !=  room.host:
        return HttpResponse("You are not the host of this room")
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})
