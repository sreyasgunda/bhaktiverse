from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
        
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Ensure a profile exists for the user
                if not hasattr(user, 'profile'):
                    from .models import Profile
                    role_map = {
                        'Devotee': 'devotee',
                        'Temple Leader': 'leader',
                        'devotee': 'devotee',
                        'leader': 'leader',
                    }
                    db_role = role_map.get(user.role, 'devotee')
                    Profile.objects.create(user=user, role=db_role)
                
                if user.profile.role == 'leader':
                    return redirect('dashboard:leader_dashboard')
                else:
                    return redirect('dashboard:devotee_dashboard')
            else:
                error_message = "Invalid email or password."
        else:
            error_message = "Invalid email or password."
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')
