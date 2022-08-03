from django import forms
from django.forms import ModelForm
from projects.models import Project


class ProjectForm(ModelForm):
    # So, here django is going to create a form based on the model Project attributes.
    class Meta:
        model = Project
        # to display out all the model(Project) details
       # fields = '__all__'
        fields = ["title", "image", "description", "demo_link","tags"]
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }
 
# to add css to the form fields
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args,  **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
            
        # --------------------> We can also do it manually ----------------------->
        # self.fields['title'].widget.attrs.update( {'class':'input', 'placeholder':'Add title'})
        # self.fields['description'].widget.attrs.update( {'class':'input', 'placeholder':'Add Description'})
         