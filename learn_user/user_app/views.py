from django.shortcuts import render
from user_app.forms import UserForm,UserProfileInfoForm
#
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    return render(request,'user_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# YOU MUST BE LOGGED IN TO VIEW THIS 'SPECIAL PAGE'
@login_required
def special(request):
    return HttpResponse("Great Job! You are already logged in!")

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()


            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'user_app/registration.html',
                            {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered':registered})



def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else: return HttpResponse("Account NOT Active")

        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'user_app/login.html',{})



    #     if user:
    #         #Check it the account is active
    #         if user.is_active:
    #             # Log the user in.
    #             login(request,user)
    #             # Send the user back to some page.
    #             # In this case their homepage.
    #             return HttpResponseRedirect(reverse('index'))
    #         else:
    #             # If account is not active:
    #             return HttpResponse("Your account is not active.")
    #     else:
    #         print("Someone tried to login and failed.")
    #         print("They used username: {} and password: {}".format(username,password))
    #         return HttpResponse("Invalid login details supplied.")
    #
    # else:
    #     #Nothing has been provided for username or password.
    #     return render(request, 'user_app/login.html', {})
