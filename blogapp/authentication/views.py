from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import BlogPost, Comment, CommentReply, Report, make_user_moderator
from .forms import CommentForm
from .models import make_user_moderator

from django.contrib.auth.models import User
from .models import Like
# Create your views here.

@login_required(login_url='Signin')
def home(request):
    return render(request, "authentication/home.html")
from .forms import CustomUserCreationForm

def Signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['is_moderator']:
                make_user_moderator(user)  # Create a moderator user if one doesn't exist
            messages.success(request, "Your Account is Successfully created")
            return redirect('Signin')
        else:
            messages.error(request, "An error occurred during registration")
    else:
        form = CustomUserCreationForm()

    return render(request, "authentication/Signup.html", {'form': form})




# def Signup(request):
#     if request.method == "POST":
#         try:
#             username = request.POST['username']
#             fname = request.POST['firstname']
#             lname = request.POST['lastname']
#             email = request.POST['email']
#             pass1 = request.POST['password']
#             pass2 = request.POST['confirm_password']
            
#             if pass1 == pass2:
#                 myuser = User.objects.create_user(username, email, pass1)
#                 myuser.first_name = fname
#                 myuser.last_name = lname
#                 myuser.save()
#                 messages.success(request, "Your Account is Successfully created")
#                 return redirect('Signin')  # Make sure 'Signin' is a valid URL name
#             else:
#                 messages.error(request, "Passwords do not match")
#                 return redirect('Signup')  # Redirect back to signup page on error
#         except Exception as e:
#             print(e)
#             messages.error(request, "An error occurred during registration")
#             return redirect('Signup')  # Redirect back to signup page on error

#     return render(request, "authentication/Signup.html")

from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate
from django.shortcuts import render

def Signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user is restricted and restriction duration has passed
        if 'restriction_start_timestamp' in request.session:
            restriction_duration = timedelta(minutes=3)  # Adjust as needed
            restriction_start_timestamp = request.session['restriction_start_timestamp']
            restriction_end_timestamp = restriction_start_timestamp + restriction_duration.total_seconds()
            current_timestamp = datetime.now().timestamp()

            if current_timestamp < restriction_end_timestamp:
                remaining_time = int(restriction_end_timestamp - current_timestamp)
                return render(request, "authentication/Signin.html", {'user_under_restriction': True, 'remaining_time_in_seconds': remaining_time})

            # If the restriction duration has passed, remove the session variable
            del request.session['restriction_start_timestamp']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session.pop('failed_attempts', None)  # Reset failed attempts upon successful login
            return render(request, "authentication/home.html")
        else:
            if 'failed_attempts' not in request.session:
                request.session['failed_attempts'] = 0

            request.session['failed_attempts'] += 1

            if request.session['failed_attempts'] >= 5:
                request.session['restriction_start_timestamp'] = datetime.now().timestamp()  # Store restriction start timestamp
                messages.error(request, "You have attempted wrong credentials multiple times. You are now restricted from entering credentials for 3 minutes.")
                return render(request, "authentication/Signin.html", {'user_under_restriction': True, 'remaining_time_in_seconds': 180})  # 180 seconds = 3 minutes

            messages.error(request, "Invalid username or password")
            return redirect('Signin')

    return render(request, "authentication/Signin.html", {'user_under_restriction': False})

def SignOut(request):
    logout(request)
    return redirect('Signin')

# @login_required(login_url='Signin')
# def create_blog(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         image = request.FILES.get('image')
        
#         blog_post = BlogPost(user=request.user, title=title, content=content, image=image)
#         blog_post.save()

#         return redirect('Signin')

#     return render(request, 'authentication/create.html')

# @login_required(login_url='Signin')
# def blog_list(request):
#     blog_posts = BlogPost.objects.all()  # Fetch all blog posts from the database
#     context = {'blog_posts': blog_posts}
#     return render(request, 'authentication/showblog.html', context)
@login_required(login_url='Signin')
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        blog_post = BlogPost(user=request.user, title=title, content=content, image=image)
        blog_post.save()

        return redirect('blog_list')  # Redirect to the appropriate page

    return render(request, 'authentication/create.html')







@login_required(login_url='Signin')
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('blog_list')  # Redirect to the blog list page after adding a comment
    else:
        form = CommentForm()

    context = {'post': post, 'form': form}
    return render(request, 'authentication/showblog.html', context)  # Render the same page with updated comments

from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment

@login_required(login_url='Signin')
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.liked_by.all():
        comment.liked_by.remove(user)
    else:
        comment.liked_by.add(user)

    # Redirect to the 'blog_list' URL pattern
    return redirect('blog_list')



#@login_required
# def like_post(request, post_id):
#     post = BlogPost.objects.get(id=post_id)
#     user = request.user

#     try:
#         like = Like.objects.get(user=user, post=post)
#         like.delete()  # Unlike the post
#         liked = False
#     except Like.DoesNotExist:
#         Like.objects.create(user=user, post=post)
#         liked = True

#     likes_count = post.like_set.count()  # Get the count of likes for the post

#     return JsonResponse({'likes_count': likes_count, 'liked': liked})#


from django.shortcuts import get_object_or_404

from django.views import View
from .models import BlogPost

from django.http import HttpResponseForbidden, JsonResponse


from .models import BlogPost, Like


from django.shortcuts import get_object_or_404

from django.views import View

from django.http import JsonResponse


class LikeView(View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(BlogPost, id=post_id)
        if request.user in post.liked.all():
            post.liked.remove(request.user)
        else:
            post.liked.add(request.user)
        return JsonResponse({'like_count': post.liked.count()})



class CheckLikeView(View):
    def get(self, request, post_id):
        user_liked = False
        # Assuming Like model has a field 'user' for the user who liked the post
        if request.user.is_authenticated:
            user_liked = Like.objects.filter(user=request.user, post_id=post_id).exists()
        return JsonResponse({'user_liked': user_liked})
    
    
    
@login_required(login_url='Signin')
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        text = request.POST.get('reply_text')
        if text:
            CommentReply.objects.create(user=request.user, comment=comment, text=text)
    
    return redirect('blog_list')  # Redirect back to the blog list after adding a reply

def get_replies(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    replies = comment.replies.all()

    serialized_replies = []
    for reply in replies:
        serialized_replies.append({
            'user': reply.user.username,
            'text': reply.text,
            'liked_by_count': reply.liked_by.count(),
        })

    return JsonResponse({'replies': serialized_replies})

@login_required(login_url='Signin')
def blog_list(request):
    blog_posts = BlogPost.objects.filter(approved=True)
    return render(request, 'authentication/showblog.html', {'blog_posts': blog_posts})


# @login_required(login_url='Signin')
# def blog_list(request):
#     if request.user.is_authenticated:
#         if Moderator.objects.filter(user=request.user).exists():
#             pending_blogs = BlogPost.objects.filter(approved=False)
#             return render(request, 'moderator_dashboard', {'pending_blogs': pending_blogs})
#     blogs = BlogPost.objects.filter(approved=True)
#     return render(request, 'authentication/showblog.html', {'blog_posts': blogs})

def approve_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    blog.approved = True
    blog.save()
    return redirect('moderator_dashboard')

def reject_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    blog.delete()
    return redirect('moderator_dashboard')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponseForbidden
from .models import Moderator

# def moderator_dashboard(request):
#     if Moderator.objects.filter(user=request.user).exists():
#         pending_blogs = BlogPost.objects.filter(approved=False)
#         return render(request, 'authentication/moderator_dashboard.html', {'pending_blogs': pending_blogs})
#     else:
#         return HttpResponseForbidden("You don't have permission to access this page.")

from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import Moderator

def moderator_dashboard(request):
    if Moderator.objects.filter(user=request.user).exists():
        pending_blogs = BlogPost.objects.filter(approved=False)
        reported_posts = Report.objects.select_related('post__user').all()
        return render(request, 'authentication/moderator_dashboard.html', {'pending_blogs': pending_blogs, 'reported_posts': reported_posts})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")


from django.shortcuts import redirect

# ... other imports ...

@login_required(login_url='Signin')
def report_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    Report.objects.create(user=request.user, post=post)
    return redirect('blog_list')

@login_required(login_url='Signin')
def handle_reports(request):
    if request.user.is_moderator:
        reported_posts = BlogPost.objects.filter(reports__gt=0)
        if request.method == 'POST':
            action = request.POST.get('action')
            post_id = request.POST.get('post_id')
            if action == 'ignore':
                reported_post = get_object_or_404(BlogPost, id=post_id)
                reported_post.reports = 0
                reported_post.save()
            elif action == 'delete':
                BlogPost.objects.filter(id=post_id).delete()
        # Retrieve pending blogs for display
        pending_blogs = BlogPost.objects.filter(approved=False)
        return render(request, 'moderator_dashboard.html', {'pending_blogs': pending_blogs, 'reported_posts': reported_posts})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")
