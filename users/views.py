from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from users.forms import CustomUserCreationForm, ProfileForm, SkillForm
from users.models import Profile, Skill
from django.contrib.auth.decorators import login_required

from users.utils import  searchProfiles
# Create your views here.


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("profiles")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            # if username and password is valid
            if user is not None:
                # login function gonna create the session in the users table
                # and takes that session and add that in the browser cookies.
                login(request, user)
                return redirect('profiles')
            # If the user doesnot exist then its value will be None.
            else:
                print("user", user)
                messages.error(request, "Username and password mismatched")
        except Exception as e:
            print(e)
            messages.error(request, e)
    return render(request, 'users/login_register.html', {"page": page})


def registerUser(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Here commit = False will hold the user from being saved
            # so that we can perform certain modification to the user data
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "An error has occured during registration")
    context = {'page': 'register', 'form': form}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    # This logout function will delete the session of the user
    logout(request)
    messages.error(request, "User was logged out")
    return redirect('login')


def showProfilePage(request):
    userProfiles, search_query = searchProfiles(request)
    print("User profiles:: ",userProfiles)
    return render(request, 'users/profiles.html', {"profiles": userProfiles, "search_query":search_query})


def userProfile(request, pk):
    userProfileDetails = Profile.objects.get(id=pk)
    topSkills = userProfileDetails.skill_set.exclude(description__exact="")
    otherSkills = userProfileDetails.skill_set.filter(description="")
    context = {'profile': userProfileDetails,
               'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    # Getting the logged in user profile.
    profile = request.user.profile
    projects = profile.project_set.all()
    context = {'profile': profile, "projects":projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method =="POST":
        newForm = ProfileForm(request.POST, request.FILES, instance = profile)
        if newForm.is_valid():
            newForm.save()
            return redirect('account')
    context = {"form":form}
    return render(request, 'users/profile_form.html', context)




@login_required(login_url='login')
def addSkill(request):
    form = SkillForm()
    if request.method == "POST":
        newForm = SkillForm(request.POST)
        if newForm.is_valid():
            addedSkill = newForm.save(commit=False)
            addedSkill.owner = request.user.profile
            addedSkill.save()
            return redirect('account')
    context = {"form":form}
    return render(request, 'users/skill-form.html', context)




@login_required(login_url='login')
def updateSkill(request, pk):
    skill = Skill.objects.get(id =pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        newForm = SkillForm(request.POST, instance=skill )
        if newForm.is_valid():
            addedSkill = newForm.save(commit=False)
            addedSkill.owner = request.user.profile
            addedSkill.save()
            return redirect('account')
    context = {"form":form}
    return render(request, 'users/skill-form.html', context)




@login_required(login_url='login')
def deleteSKill(request, pk):
    skill = Skill.objects.get(id =pk)
    if request.method == "POST":
        print("Printing something:::",request.POST)
        skill.delete()
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)