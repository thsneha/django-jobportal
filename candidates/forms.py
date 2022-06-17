from django import forms
from candidates.models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model=CandidateProfile
        exclude=("user",)
        widgets={
            "profile_pic":forms.FileInput(attrs={"class":"form-control rounded-pill"}),
            "qualification":forms.TextInput(attrs={"class":"form-control rounded-pill"}),
            "skills":forms.TextInput(attrs={"class":"form-control rounded-pill"}),
            "experience":forms.NumberInput(attrs={"class":"form-control rounded-pill"}),
        }

class CandidateProfileUpdateForm(forms.ModelForm):
    first_name=forms.CharField()
    last_name=forms.CharField()
    phone=forms.CharField()
    class Meta:
        model=CandidateProfile
        #these fields we are adding here.because the firstname,lastname,phone not included in model.
        fields=[
            "first_name",
            "last_name",
            "phone",
            "profile_pic",
            "resume",
            "qualification",
            "skills",
            "experience",

        ]
