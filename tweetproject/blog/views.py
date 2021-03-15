from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect, reverse, redirect
from .models import Blog, BlogComment
from .forms import postform, commentform
from user.models import userform
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    template_name = "home.html"
    context = {}
    return render(request, template_name, context)

@login_required
def bloglist(request):
    posts = Blog.objects.filter(user=request.user)
    if userform.objects.filter(user=request.user).exists():
        obj = userform.objects.get(user=request.user)
        following = obj.following.all()
        print(following)
        for x in following:
            posts = posts | Blog.objects.filter(user=x)
    
    # comments = BlogComment.objects.filter(post=)

    template_name = "allposts.html"
    context = {"posts":posts}
    return render(request, template_name, context)

@login_required
def blogdetail(request, pk):
    post = get_object_or_404(Blog, id=pk)
    form = commentform(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.post = post
        obj.user = request.user
        obj.save()
    
    comments = BlogComment.objects.filter(post=post)
    total_likes = post.total_likes()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = False
    else:
        liked = True
    form = commentform()
    template_name = "postdetail.html"
    context = {"liked":liked, "post":post, "total_likes":total_likes, "comments":comments, "form":form}
    return render(request, template_name, context)

@login_required
def postlike(request, pk):
    post = get_object_or_404(Blog,id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blogdetail', args=[str(pk)]))

@login_required
def postcreate(request):
    form = postform(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('/detail/'+str(obj.id))

    form = postform()
    template_name = "postcreate.html"
    context = {'form':form}
    return render(request, template_name, context)

@login_required
def postdelete(request, pk):
    post = Blog.objects.filter(id=pk)
    if post is not None:
        post.delete()
        return redirect('/all')
    template_name = "postdelete.html"
    context = {}
    return render(request, template_name, context)

@login_required
def postupdate(request, pk):
    obj = get_object_or_404(Blog, id=pk)
    form = postform(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/detail/"+str(pk))
    context = {"form":form,"update":True}
    template_name = "postupdate.html"
    return render(request, template_name, context)

@login_required
def deletecomment(request, pk):
    obj = BlogComment.objects.get(id=pk)
    post = obj.post
    print(post)
    obj.delete()
    return redirect('/detail/'+str(post.id))