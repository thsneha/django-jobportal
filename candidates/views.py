from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView,ListView,DetailView
from candidates.models import CandidateProfile
from candidates.forms import CandidateProfileForm,CandidateProfileUpdateForm
from django.urls import reverse_lazy
from employer.models import User,Jobs,Applications
from django.contrib import messages
# Create your views here.
class CandidateHomeView(TemplateView):
    template_name = "candidate/can-home.html"

class CandidateProfileView(CreateView):
    model=CandidateProfile
    form_class=CandidateProfileForm
    template_name = "candidate/can-profile.html"
    success_url = reverse_lazy("cand-home")

    def form_valid(self,form):
        form.instance.user=self.request.user
        messages.success(self.request,"your profiles has been added")
        return super().form_valid(form)

class CandidateProfileDetailView(TemplateView):
     template_name="candidate/can-profiledetail.html"


class CandidateProfileEditView(FormView):
    template_name = "candidate/can-editprof.html"
    form_class = CandidateProfileUpdateForm

    def get(self,request,*args,**kwargs):
        #obtain the profdetails of login user
        prodetails=CandidateProfile.objects.get(user=request.user)

        #loading the CandidateProfileUpdateForm but the firstname,last_name and phone in employer models so it is initialize by the login users details.5
        form=self.form_class(instance=prodetails,initial={"first_name":request.user.first_name,
                                                          "last_name":request.user.last_name,
                                                          "phone":request.user.phone})
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        prodetails=CandidateProfile.objects.get(user=request.user)
        form = self.form_class(instance=prodetails,data=request.POST,files=request.FILES)
        if form.is_valid():
            #separating the user model details data and profile model details data otherwise it can't be save ..
            firstname=form.cleaned_data.pop("first_name")
            lastname=form.cleaned_data.pop("last_name")
            phone=form.cleaned_data.pop("phone")
            form.save()#now it contains profile data in form exclude firstname,lastname,phone
            user=User.objects.get(id=request.user.id)
            user.first_name=firstname
            user.last_name=lastname
            user.phone=phone
            user.save()
            messages.success(request,"your profile has been updated")
            return redirect("cand-home")
        else:
            messages.error(request,"error occur while updating profile")
            return render(request,self.template_name,{"form":form})
class CandidateJobListView(ListView):
    model=Jobs
    context_object_name = "jobs"
    template_name = "candidate/joblist.html"

    def get_queryset(self):#changing the query set
        return self.model.objects.filter(active_status=True).order_by("-created_date")#currently active jobsobtaining the jobs by descending order of date,so latest will come first.

class CandidateJobDetailView(DetailView):
    model=Jobs
    context_object_name = "job"
    template_name = "candidate/jobdetail.html"
    pk_url_kwarg ="id"

#check whether the login candidate has applied the job or not.so we need particular jobdetail + applied job or not.
#job=self.object means particular job object
#contextdata overide- if we need the alreadydata+additional data
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        is_applied=Applications.objects.filter(applicant=self.request.user,job=self.object)
        context["is_applied"]=is_applied
        return context

def apply_now(request,*args,**kwargs):
    user=request.user
    job_id=kwargs.get("id")
    job=Jobs.objects.get(id=job_id)
    Applications.objects.create(applicant=user,job=job)
    messages.success(request,"your application has been posted successfully")

    return redirect("cand-home")

class ApplicationListView(ListView):
    model= Applications
    template_name="candidate/cand-applications.html"
    context_object_name = "applications"

    def get_queryset(self):
        return Applications.objects.filter(applicant=self.request.user).exclude(status="cancelled")#to remove the cancelled application status

def cancel_applicaton(request,*args,**kwargs):
    app_id=kwargs.get("id")
    application=Applications.objects.get(id=app_id)
    application.status="cancelled"
    application.save()
    messages.success(request,"your application cancelled")
    return redirect("cand-home")



