from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Jobs(models.Model):#mapping to table in db
    job_title=models.CharField(max_length=150)
    company=models.CharField(max_length=150)
    location=models.CharField(max_length=150)
    salary=models.PositiveIntegerField(null=True)#if the field is not added it will be added to db
    experience=models.PositiveIntegerField(default=0)#if the person has no experence then it will default as zero but if we added the experience it will change..

#python manage.py makemigrations
#python manage.py migrate
#to print the objects name and details in shell we are overriding the string method(tostring):

    def __str__(self):
        return self.job_title
class CompanyProfile(models.Model):
    company_name=models.CharField(max_length=150)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="employer")
    logo=models.ImageField(upload_to="companyprofile",null=True)
    location=models.CharField(max_length=120)
    services=models.CharField(max_length=120)
    description=models.CharField(max_length=200)


#create the objects in model
# orm query
#Modelname.objects.create(field=value,field=value....)
#eg.."Jobs.objects.create(job_title="front end developer",company="tcs",location="kakkanad",salary="40000",experience="2")


#create an app in mathoperations employees

        #Employees(cname,salary,dept,exp)
        #emp create
        #fetch all employees
        #filter
# to fetch a specific object
#qs=Jobs.objects.get(id=5)
# print(qs)
#update
 #1.qs.Jobs.objects.get(id=3)
 #qs
 #qs.experience=2
 #qs.save()
#create
#list
#Details
#update
#delete