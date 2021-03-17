from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import userform
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def createuser(request):
    form = createUser(request.POST or None)
    if form.is_valid():
        form.save()
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
        qs = userform.objects.filter(user=request.user)
        qs = qs.first()
        obj = None
        if qs is None:
            obj = userform.objects.create(user=user)
            obj.save()

        if userform.objects.get(user=request.user).firstName is None:
            context = {}
            template_name = "updateprofile.html"
            form = profileform()
            context["form"] = form
            return render(request, template_name, context)
        return redirect('/all')
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
        context['profile'] = obj
        context['req'] = user
        context['username'] = username
        context['followers'] = followerslst
        context['following'] = followinglst
        context['followersCount'] = len(followerslst)
        context['followingCount'] = len(followinglst)
        context['bio'] = bio
    else:
        context['username'] = user
    return render(request, template_name, context)


def allusers(request):
    obj = userform.objects.all()
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

def whotofollow(request):
    users = userform.objects.all()
    famoususers = {}
    for x in users:
        name = x.user.username
        followersCount = x.followers.all().count()
        famoususers[name] = followersCount
    newlist = sorted(famoususers.items(), key = lambda kv:(kv[1], kv[0]))
    famoususers = []
    top5 = len(newlist)
    for var in range(top5-3,top5):
        famoususers.append(newlist[var])
    return redirect('/')

def updateprofile(request):
    obj = userform.objects.get(user=request.user)
    form = profileform(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        print(obj)
        print(form.cleaned_data)
        obj.firstName = form.cleaned_data['firstName']
        obj.lastName = form.cleaned_data['lastName']
        obj.gender = form.cleaned_data['gender']
        obj.profileImage = form.cleaned_data['profileImage']
        obj.contactNumber = form.cleaned_data['contactNumber']
        obj.address = form.cleaned_data['address']
        obj.bio = form.cleaned_data['bio']
        obj.save()
        form.save()
        return redirect('/detailuser/'+str(request.user.id))
    template_name = "updateprofile.html"
    context = {"form":form}
    return render(request, template_name, context)

@csrf_exempt
def search(request):
    q = request.GET.get('q', None)
    context = {}
    try:
        user = User.objects.get(username__iexact=q)
        obj = userform.objects.get(user=user)
        if obj is not None:
            context['obj'] = obj
            context['found'] = True
    except:
        context['found'] = False
    template_name = "search.html"
    return render(request, template_name, context)

@login_required
def viewfollowing(request, pk):
    obj = userform.objects.get(user=request.user)
    f = obj.following.all()
    users = []
    for x in f:
        users.append(userform.objects.get(user=x))
    template_name = "viewfollowing.html"
    context = {"following":users}
    if request.method == "POST":
        unfollow_user = userform.objects.get(id=pk)
        unfollow_user.followers.remove(request.user)
        unfollow_user = User.objects.get(username=unfollow_user.user)
        curr = userform.objects.get(user=request.user)
        curr.following.remove(unfollow_user)

        obj = userform.objects.get(user=request.user)
        f = obj.following.all()
        users = []
        for x in f:
            users.append(userform.objects.get(user=x))
        template_name = "viewfollowing.html"
        context = {"following":users}

        return render(request, template_name, context)
    return render(request, template_name, context)

@login_required
def viewfollowers(request):
    obj = userform.objects.get(user=request.user)
    f = obj.followers.all()
    users = []
    for x in f:
        users.append(userform.objects.get(user=x))
    template_name = "viewfollowers.html"
    context = {"followers":users}
    return render(request, template_name, context)