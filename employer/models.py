from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
#previous user model contains firstname,lastname,username,email,pwd.
# so we have to customize the user.
#customizing authentication in django for adding the role in user.eg.employer or candidate
class User(AbstractUser):
    options=(
             ("employer","employer"),
             ("candidate","candidate")
             )
    role=models.CharField(max_length=120,choices=options,default="candidate")
    phone=models.CharField(max_length=12,null=True)



class Jobs(models.Model):#mapping to table in db
    job_title=models.CharField(max_length=150)
    company=models.ForeignKey(User,on_delete=models.CASCADE,related_name="company")#company is adding the job so it is foreign key-one to many
    location=models.CharField(max_length=150)
    salary=models.PositiveIntegerField(null=True)#if the field is not added it will be added to db
    experience=models.PositiveIntegerField(default=0)#if the person has no experence then it will default as zero but if we added the experience it will change..
    created_date=models.DateField(auto_now_add=True)#obtain automatically current date and time
    last_date=models.DateField(null=True)
    active_status=models.BooleanField(default=True)#

#python manage.py makemigrations
#python manage.py migrate
#to print the objects name and details in shell we are overriding the string method(tostring):

    def __str__(self):
        return self.job_title
class CompanyProfile(models.Model):
    company_name=models.CharField(max_length=150)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="employer")#related name for parent child referencing..request.user.employer.logo(it will points to companyprofile logo)
    logo=models.ImageField(upload_to="companyprofile",null=True)
    location=models.CharField(max_length=120)
    services=models.CharField(max_length=120)

    description=models.CharField(max_length=200)

class Applications(models.Model):
        applicant = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_name="applicant")  # no of applicants can apply an applications ie  many to one-foreignkey
        job = models.ForeignKey(Jobs, on_delete=models.CASCADE)  # many job can apply  a candidate
        options = (
            ("applied", "applied"),  # (values in backend, display)
            ("accepted", "accepted"),
            ("rejected", "rejected"),
            ("pending", "pending"),
            ("cancelled", "cancelled")
        )
        status = models.CharField(max_length=120, choices=options, default="applied")
        date = models.DateTimeField(auto_now_add=True)

        class Meta:
            unique_together=("applicant","job")#befor thie its stop only apply job via client if we apply the job through the url it is posted again and again
                                               #so the applicant and job unique together

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