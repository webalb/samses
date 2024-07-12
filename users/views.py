from django.shortcuts import render, redirect
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object without saving the user
            new_user = user_form.save(commit=False)
            # set the choosen password
            new_user.set_password(user_form.cleaned_data['password'])

            # now save the user object in database
            new_user.save()
            # create a new user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
        

    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            return redirect('users:password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {
        'form': form
    })

@login_required
def password_change_done(request):
    return render(request, 'registration/password_change_done.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'section': dashboard})

def logout_view(request):
    logout(request)
    context = {'message': 'You have successfully logged out.'}
    return render(request, 'registration/logged_out.html', context)