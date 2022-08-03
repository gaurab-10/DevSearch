from email.policy import default
import uuid
from django.db import models

from users.models import Profile


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True,  blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    
    owner = models.ForeignKey(Profile, null= True, blank = True, on_delete = models.SET_NULL)
    title = models.CharField(max_length=200)
    # null is for database i.e. in database it can accept null vlaue
    # blank(~ validation in spring boot) is for when we want to pass data using post methods or render
    # the value it specifies us that we can take or pass blank value
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank = True, default = "default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField(Tag, through="ProjectTag")
    vote_total = models.IntegerField(default=0,  blank=True)
    vote_ratio = models.IntegerField(default=0,  blank=True)
    created = models.DateTimeField(auto_now_add=True,  blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title
    # to load the project in order according to the certain attribute.
    class Meta:
        # it loads the project in descending order  acc to the created date
       #ordering = ['created']
          # it loads the project in ascending order acc to the created date
        ordering = ['-created']


class ProjectTag(models.Model):
    project = models.ForeignKey(to=Project, null=True, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,  on_delete=models.CASCADE)

    def __str__(self):
        return self.project.title




class Review(models.Model):

    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    # many to one (foreign key in djano)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
                          
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE,  default=None)
    created = models.DateTimeField(auto_now_add=True,  blank=True)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.value
    
    class Meta:
        ordering = ['value']
        
