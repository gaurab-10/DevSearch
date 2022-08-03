
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from users.models import Profile


# Receiver decorator can be used instead of the post_save(delete).connect(------)
# @receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    # created will be true if the new user is created
    print("Create Profile Signal called")
    if created:
        user = instance
        print(user)
        profile = Profile(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name)
        profile.save()
        print("profile made::",profile)



# here instance is the profile of one user
def deleteUser(sender, instance, **kwargs):
    print("Delteting user!!! ")
    user = instance.user
    user.delete()




def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()








# Here the User model will send the signal to the method createProfile whenever we save or updated the user details.
post_save.connect(createProfile, sender=User)
# Whenever the profile is deleted from the Profile model then it tiggers the deleteUser function.
post_delete.connect(deleteUser, sender=Profile)
post_save.connect(updateUser, sender =Profile)