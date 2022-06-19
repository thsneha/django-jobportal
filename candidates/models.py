from django.db import models
from employer.models import User,Jobs
# Create your models here.
class CandidateProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="candidate")
    profile_pic=models.ImageField(upload_to="candprofiles")
    resume=models.FileField(upload_to="cvs",null=True)
    qualification=models.CharField(max_length=120)
    skills=models.CharField(max_length=120)
    experience=models.PositiveIntegerField(default=0)

class Applications(models.Model):
    applicant=models.ForeignKey(User,on_delete=models.CASCADE,related_name="applicant")#no of applicants can apply an applications ie  many to one-foreignkey
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)#many job can apply  a candidate
    options=(
        ("applied","applied"),#(values in backend, display)
        ("accepted","accepted"),
        ("rejected","rejected"),
        ("pending","pending"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=120,choices=options,default="applied")
    date=models.DateTimeField(auto_now_add=True)



