from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from users.models import Profile, Skill

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # here fields are those attributes of the User model that we want to ask user
        # to insert the values.
        fields = ['first_name', 'email', 'username', 'password1','password2']
       # we can also modify the labels 
       # key ---> present label
       # value ---> the label name that we want to change to 


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirm Password'
        self.fields['first_name'].label = 'Name'

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
       # fields= "__all__"
        fields = ["name", "username", "email",  
        "location", "short_intro", "bio" ,
        "profile_image",
         "social_linkedin", "social_twitter", "social_github"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class SkillForm(ModelForm):
    class Meta:
        model=Skill
        fields = ["name", "description"]

        def __init__(self, *args, **kwargs):
            super(SkillForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class':'input'})