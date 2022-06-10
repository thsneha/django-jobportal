from django import forms
# from django.contrib.auth.models import User
from employer.models import  User
from django.contrib.auth.forms import UserCreationForm
from employer.models import Jobs,CompanyProfile


# class JobForm(forms.Form):
    # job_title=forms.CharField()
    # company=forms.CharField()
    # location=forms.CharField()
    # salary=forms.IntegerField()
    # experience=forms.IntegerField()

    #MODELFORM is inherited and USING FOR CREATING FORM CORRESPONDING DATABASE.


class JobForm(forms.ModelForm):
    class Meta:
        model=Jobs
        exclude=("company","created_data","active_status")
        widgets={
            "last_date":forms.DateInput(attrs={"class":"form-control",
                                               "type":"date"})

                }

class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2","role","phone"]


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())



class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model=CompanyProfile
        exclude=("user",)
    



