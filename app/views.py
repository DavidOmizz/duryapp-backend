from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Category, Video
from .serializers import CategorySerializer, VideoSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from .models import Category, Video, UserCategoryAccess, UserSession
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.views import View



# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            print(form.errors)  # Debugging line
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


# Custom Login View
# class SingleLoginView(LoginView):
#     def form_valid(self, form):
#         user = form.get_user()
#         session_key = self.request.session.session_key or self.request.session.create()

#         try:
#             existing = UserSession.objects.get(user=user)
#             if existing.session_key != self.request.session.session_key:
#                 logout(self.request)
#                 messages.error(self.request, "❌ You are already logged in on another device. Please log out from that device first.")
#                 return redirect('login')
#         except UserSession.DoesNotExist:
#             UserSession.objects.create(user=user, session_key=self.request.session.session_key)

#         return super().form_valid(form)

# class SingleLoginView(LoginView):
#     def form_valid(self, form):
#         user = form.get_user()

#         # 👇 Force session key to be created if not already
#         if not self.request.session.session_key:
#             self.request.session.create()

#         session_key = self.request.session.session_key

#         try:
#             existing = UserSession.objects.get(user=user)

#             # Check if the stored session still exists in DB
#             if existing.session_key != session_key:
#                 session_exists = Session.objects.filter(session_key=existing.session_key).exists()

#                 if session_exists:
#                     # Old session is still alive — block login
#                     logout(self.request)
#                     messages.error(self.request, "❌ You are already logged in on another device. Please log out there first.")
#                     return redirect('login')
#                 else:
#                     # Old session expired — update to new session
#                     existing.session_key = session_key
#                     existing.save()

#         except UserSession.DoesNotExist:
#             # ✅ Safe now — session_key is guaranteed
#             UserSession.objects.create(user=user, session_key=session_key)

#         return super().form_valid(form)


# class SingleLoginView(LoginView):
#     def form_valid(self, form):
#         user = form.get_user()

#         # Make sure session key exists
#         if not self.request.session.session_key:
#             self.request.session.create()

#         session_key = self.request.session.session_key

#         try:
#             existing = UserSession.objects.get(user=user)

#             # ✅ Check if old session is still active in the database
#             session_exists = Session.objects.filter(session_key=existing.session_key).exists()

#             if session_exists and existing.session_key != session_key:
#                 # Block login — another device is already logged in
#                 logout(self.request)
#                 messages.error(self.request, "🚫 You are already logged in on another device.")
#                 return redirect('login')
#             elif not session_exists:
#                 # Old session expired, allow login and update
#                 existing.session_key = session_key
#                 existing.save()

#         except UserSession.DoesNotExist:
#             # First login — create session record
#             UserSession.objects.create(user=user, session_key=session_key)

#         return super().form_valid(form)

class SingleLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            # ✅ Check if user already has an active session
            try:
                existing = UserSession.objects.get(user=user)
                session_exists = Session.objects.filter(session_key=existing.session_key).exists()

                if session_exists:
                    # 🚫 BLOCK login — someone is already logged in
                    messages.error(request, "🚫 You're already logged in on another device.")
                    return redirect('login')

                else:
                    # Old session is expired — delete and allow login
                    existing.delete()

            except UserSession.DoesNotExist:
                pass  # No existing session — proceed

            # 🔐 Manually log user in
            login(request, user)

            # 💾 Force session creation if missing
            if not request.session.session_key:
                request.session.create()

            # Save new session to UserSession
            UserSession.objects.update_or_create(user=user, defaults={
                'session_key': request.session.session_key
            })

            return redirect('dashboard')  # or your desired view

        else:
            return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        # Delete the stored session record
        UserSession.objects.filter(user=request.user).delete()

        # Log the user out
        logout(request)

        # Optional: success message
        messages.success(request, "✅ You have been logged out successfully.")
    
    return redirect('login')  # Redirect to login page


# Dashboard
def dashboard(request):
    categories = Category.objects.all()
    access_ids = UserCategoryAccess.objects.filter(user=request.user).values_list('category_id', flat=True)
    return render(request, 'dashboard.html', {'categories': categories, 'user_access': access_ids})

# Category Videos
def category_videos(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    has_access = UserCategoryAccess.objects.filter(user=request.user, category=category).exists()

    if has_access:
        videos = category.videos.all()
        return render(request, 'category_videos.html', {'category': category, 'videos': videos})
    else:
        messages.error(request, "Please contact the admin to request access to this category.")
        return redirect('dashboard')

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class VideoListView(APIView):
    def post(self, request, category_id):
        category = Category.objects.get(id=category_id)
        password = request.data.get('password')

        if category.password != password:
            raise AuthenticationFailed('Incorrect password')

        videos = Video.objects.filter(category=category)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

