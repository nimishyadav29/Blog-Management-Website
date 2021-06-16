from django.shortcuts import render,redirect
from .models import Post,BlogComment
from django.contrib import messages

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'bloghome.html',context)

def blogPost(request, id):
    post = Post.objects.filter(sno=id).first()
    comments = BlogComment.objects.filter(post=post)
    context = {"post": post,'comments': comments, 'user': request.user}
    return render(request, 'blogpost.html',context)


def dashboard(request):

    if request.user.is_authenticated:
        post = Post.objects.filter(user_name=request.user.username)
        print(post)

        return render(request, 'dashboard.html', {'post': post})

def add(request):
    if request.method == "POST":
        title = request.POST['tit']
        content= request.POST['cont']


        blogging =Post(title=title, content=content,user_name=request.user.username,author=request.user.first_name)
        blogging.save()
        messages.success(request, "Your post has been added")
        return redirect("dash")

    else:
        return render(request, 'addpost.html')

def update(request,id):
    if request.method == "POST":
        title = request.POST['tit']
        content = request.POST['cont']
        a=Post.objects.get(sno=id)
        a.title=title
        a.content=content


        a.save()
        messages.success(request, "Your post has been updated")
        return redirect("dash")

    else:
        updatepost = Post.objects.filter(sno=id)
        return render(request, 'updatepost.html', {'updatepost': updatepost})


def delete(request,id):
    b=Post.objects.get(sno=id)
    b.delete()
    messages.success(request, "Your post has been deleted!!")
    return redirect("dash")


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        comment = BlogComment(comment=comment, user=user, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")

    return redirect(f"/blog/{post.sno}")