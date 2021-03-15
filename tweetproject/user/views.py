from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import userform
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def createuser(request):
    form = createUser(request.POST or None)
    if form.is_valid():
        form.save(commit=False)
        return redirect('loginuser')
    template_name = "createuser.html"
    context = {"form":form}
    return render(request, template_name, context)

def loginuser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        messages.info(request,"Username or password incorrect")
    template_name = "loginuser.html"
    context = {}
    return render(request, template_name, context)

@login_required
def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def detailuser(request, pk):
    template_name = "detailuser.html"
    context = {}
    user = User.objects.get(id=pk)
    if userform.objects.filter(user=user).exists():
        obj = userform.objects.get(user=user)
        username = obj.user
        followers = obj.followers.all()
        followerslst = []
        for x in followers:
            followerslst.append(x)
        following = obj.following.all()
        followinglst = []
        for x in following:
            followinglst.append(x)
        bio = obj.bio
        print(followerslst,followinglst)
        context['username'] = username
        context['followers'] = followerslst
        context['following'] = followinglst
        context['bio'] = bio
    else:
        context['username'] = user
    return render(request, template_name, context)


def allusers(request):
    obj = User.objects.all()
    template_name = "allusers.html"
    context = {"users":obj}
    return render(request, template_name, context)

@login_required
def followuser(request, pk):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        print(user)
        if userform.objects.filter(user=user).exists():
            followUser = User.objects.get(id=pk)
            obj = userform.objects.get(user=followUser)
            obj2 = userform.objects.get(user=user)
            print(obj.followers.all())
            if user not in obj.followers.all():
                obj.followers.add(user)
                obj2.following.add(followUser)
                return HttpResponseRedirect(reverse('detailuser', args=[str(pk)]))
            else:
                obj.followers.remove(user)
                obj2.following.remove(followUser)
                return HttpResponseRedirect(reverse('detailuser', args=[str(pk)]))
        else:
            obj = userform.objects.create(user=user)
            obj.followers.add(request.user)
            return HttpResponseRedirect(reverse('detailuser', args=[str(pk)]))
    return redirect('/')

                
