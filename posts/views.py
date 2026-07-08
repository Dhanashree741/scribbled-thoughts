from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Post, Category, Comment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index (request):
    post = Post.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html',{
        'posts':post,
        'categories':categories
        })

def post(request,pk):
    post = Post.objects.get(id=pk)
    comments = post.comments.all().order_by('-created_at')
    return render(request,'post.html',{
        'post':post,
        'comments':comments,
        })

def category_posts(request, id):
    post = Post.objects.filter(category_id = id)
    categories = Category.objects.all()
    selected_category = Category.objects.filter(id=id)
    return render(request, 'index.html', {
        'posts':post,
        'categories':categories,
        'selected_category':selected_category,
    })
    
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('confirm_password')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('index')

        # Check if passwords match
        if password != password1:
            messages.error(request, "Passwords do not match")
            return redirect('index')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('home')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('index')  # or 'login'

    return redirect('index')  

def user_login(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request,"Account logged in succesfully.")
        else:
            messages.error(request,"Invalid crendentials")
    return redirect('index')

def user_logout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('index')

@login_required
def add_comment(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        text = request.POST.get('text')

        Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )

        messages.success(request, "Comment added successfully")

    return redirect(f'/post/{id}/')

@login_required
def like_post(request, id):
    post = Post.objects.get(id=id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)   
    else:
        post.likes.add(request.user)      

    return redirect('post',pk=id)