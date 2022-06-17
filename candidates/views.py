from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView
from candidates.models import CandidateProfile
from candidates.forms import CandidateProfileForm,CandidateProfileUpdateForm
from django.urls import reverse_lazy
from employer.models import User
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
            return redirect("cand-home")
        else:
            return render(request,self.template_name,{"form":form})

