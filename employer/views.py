from django.shortcuts import render,redirect
from django.views.generic import View,ListView,CreateView,DetailView,UpdateView,DeleteView,FormView,TemplateView
from django.urls import reverse_lazy
from employer.forms import JobForm
from employer.models import Jobs,CompanyProfile
from employer.forms import SignUpForm,LoginForm,CompanyProfileForm
# from django.contrib.auth.models import User
from employer.models import User,Applications
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from employer.decorators import signin_required
from django.core.mail import send_mail

# Create your views here.
#create
#form_class
#model
#orm=Model.objects.create()

#list
#model
#form-modl.objects.all()
@method_decorator(signin_required,name='dispatch')#from request is coming to the url then the dispatch is necessary for where it to be passed to the get fn or post fn.
class EmployerHomeview (View):
    def get(self,request,*args,**kwargs):
        return render(request,"emp_home.html")

@method_decorator(signin_required,name='dispatch')
class AddJobView(CreateView):#forclass and successurl in post case..
    model=Jobs
    form_class=JobForm
    template_name = "emp_addjob.html"
    success_url=reverse_lazy("emp-alljobs")#successurl is used for post case after creating the jobs then click add button it go to list all jobs.
    #override the form_valid method
    #before saving the form we have to pass the company in model
    def form_valid(self, form):
        form.instance.company=self.request.user#assign the company is the user who is login.
        return super().form_valid(form)

    # def get(self,request):
    #     form=JobForm()
    #     return render(request,"emp_addjob.html",{"form":form})
    # def post(self,request):
    #     form=JobForm(request.POST)
    #     if form.is_valid():
    #         # # lefside models field names,right side-post value names
    #
    #        # jname=form.cleaned_data.get("job_title")
    #        # company=form.cleaned_data.get("company")
    #        # location=form.cleaned_data.get("location")
    #        # salary=form.cleaned_data.get("salary")
    #        # exp=form.cleaned_data.get("experience")
    #        # Jobs.objects.create(
    #        #    job_title=jname,
    #        #    company=company,
    #        #    location=location,
    #        #    salary=salary,
    #        #    experience=exp
    #        #
    #        # )
    #        form.save()
    #        return render(request,"emp_home.html")
    #     else:
    #       return render(request,"emp_addjob.html",{"form":form})

#create-form
#update-form
#list-
#delete

@method_decorator(signin_required,name='dispatch')
class ListJobView(ListView):
    # def get(self,request):
    #   qs= Jobs.objects.all()
    #   return render(request,"emp-listjob.html",{"jobs":qs})
    model=Jobs
    context_object_name="jobs"
    template_name="emp-listjob.html"
    def get_queryset(self):#overriding the get queryset because we have to change only orm query set otherwise we have to pass below all commands
        return Jobs.objects.filter(company=self.request.user)
    # def get(self,request):
    #   qs= Jobs.objects.filter(company=request.user)
    #   return render(request,self.template_name,{"jobs":qs})
@method_decorator(signin_required,name='dispatch')
class JobDetailsView(DetailView):
    # def get(self,request,id):  #id passing at the time of specific operation in an object
    #     qs=Jobs.objects.get(id=id)#eg,Edit,Delete,Uodate
    #     return render (request,"emp-jobdetails.html",{"job":qs})
   model=Jobs
   context_object_name="job"
   template_name = "emp-jobdetails.html"
   pk_url_kwarg="id"  #id is overriding the pk..


class JobEditView(UpdateView):
    model=Jobs
    form_class=JobForm
    template_name="emp-jobedit.html"
    success_url=reverse_lazy("emp-alljobs")
    pk_url_kwarg="id"
    # def get(self,request,id):
    #   qs=Jobs.objects.get(id=id)
    #   form=JobForm(instance=qs)#by using instance we get the form with filled data,othrwise blank form.
    #   return render(request,"emp-jobedit.html",{"form":form})
    # def post(self,request,id):
    #     qs=Jobs.objects.get(id=id)
    #     form=JobForm(request.POST,instance=qs)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("emp-alljobs")
    #     else:
    #         return render(request,"emp-jobedit.html",{"form":form})
@method_decorator(signin_required,name='dispatch')
class JobDeleteView(DeleteView):
    # def get(self,request,id):
    #    qs=Jobs.objects.get(id=id)
    #    qs.delete()
    #    return redirect("emp-alljobs")
    model=Jobs
    template_name = "jobconfirmdelete.html"
    success_url = reverse_lazy("emp-alljobs")
    pk_url_kwarg = "id"

#Listview
#model
#contex object name

class SignUpView(CreateView):
    model=User
    form_class=SignUpForm
    template_name = "usersignup.html"
    success_url=reverse_lazy("signin")

class SignInview(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)#auth app contains authenticate function..
            if user:
                login(request,user)#used for avoid reauthenticate in case of add job or listjob.
                if request.user.role=="employer":
                    return redirect("emp-alljobs")
                elif request.user.role=="candidate":
                    return redirect("cand-home")


            else:
                return render(request,"login.html",{"form":form})
@signin_required
def signout_view(request,*args,**kwargs):

    logout(request)
    return redirect("signin")

@method_decorator(signin_required,name='dispatch')
class ChangePasswordView(TemplateView):
    template_name = "changepassword.html"
    def post(self,request,*args,**kwargs):
        pwd=request.POST.get("pwd")
        uname=request.user
        user=authenticate(request,username=uname,password=pwd)
        if user:
            return redirect("reset-password")
        else:
            return render(request,self.template_name)

@method_decorator(signin_required,name='dispatch')
class PasswordResetView(TemplateView):
    template_name="passwordreset.html"
    def post(self,request,*args,**kwargs):
        pwd1=request.POST.get("pwd1")#pwd1 from name="pwd1" from passwordreset.html
        pwd2=request.POST.get("pwd2")
        if pwd1!=pwd2:
            return render(request,self.template_name,{"msg":"password mismatch"})
        else:
            u=User.objects.get(username=request.user)
            u.set_password(pwd1)
            u.save()
            return redirect("signin")

@method_decorator(signin_required,name='dispatch')
class CompanyProfileView(CreateView):
    model = CompanyProfile
    form_class = CompanyProfileForm
    template_name='emp-addprofile.html'
    success_url=reverse_lazy("emp-home")

    # def post(self, request, *args, **kwargs):
    #    form=CompanyProfileForm(request.POST,files=request.FILES)#request.Post only added the text format but incase image we have to add files
    #    if form.is_valid():                    #in the form user is excluded so we have to pass who is the user..
    #          form.instance.user = request.user#ie we have to pass the user as user who is logged in from the form.so the user from logged in added to user field
    #          form.save()
    #          return redirect("emp.home")
    #    else:
    #          return render(request,self.template_name,{"form":form})
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

@method_decorator(signin_required,name='dispatch')
class EmpViewProfileView(TemplateView):
        template_name = "emp-viewprofile.html"

@method_decorator(signin_required,name='dispatch')
class EmpEditProfileView(UpdateView):
    model=CompanyProfile
    form_class = CompanyProfileForm
    template_name = "emp-editprofile.html"
    success_url = reverse_lazy("emp-viewprofile")
    pk_url_kwarg = "id"

@method_decorator(signin_required,name='dispatch')
class EmployeeListApplications(ListView):
    model=Applications
    context_object_name = "applications"
    template_name = "empl-applist.html"
    #default query set is Applications.objects.all..so we filter and change the query so here queryset override.
    def get_queryset(self):
        return Applications.objects.filter(job=self.kwargs.get("id"),status="applied")#exclude the status=cancelled.

@method_decorator(signin_required,name='dispatch')
class EmployeeApplicationDetailView(DetailView):
    model=Applications
    context_object_name = "application"
    template_name = "emp-appdetail.html"
    pk_url_kwarg = "id"


@signin_required
def accept_application(request,*args,**kwargs):
    if request.method=="POST":
      app_id=kwargs.get("app_id")
      application=Applications.objects.get(id=app_id)#obtaining this id from model
      application.status="accepted"
      application.save()
      subject=request.POST.get("sub")
      message=request.POST.get("msg")
      email=request.POST.get("email")
      send_mail(
          subject,
          message,
          'snehasthomas2016@gmail.com',
          [email],
          fail_silently=False,
      )
      messages.success(request, "your application accepted")
      return redirect("emp-home")


@signin_required
def reject_application(request,*args,**kwargs):
    app_id=kwargs.get("id")
    application=Applications.objects.get(id=app_id)
    application.status="rejected"
    application.save()
    messages.success(request,"application is rejected")
    return redirect("cand-home")


















