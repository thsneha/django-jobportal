from django.urls import path
from candidates import views

urlpatterns=[
    path("home",views.CandidateHomeView.as_view(),name="cand-home"),
    path("profile/add",views.CandidateProfileView.as_view(),name="cand-addprofile"),
    path("profile/details",views.CandidateProfileDetailView.as_view(),name="cand-profdetatil"),
    path("profile/edit",views.CandidateProfileEditView.as_view(),name="cand-editview"),
    path("jobs/all",views.CandidateJobListView.as_view(),name="cand-joblist"),
    path("job.detail/<int:id>",views.CandidateJobDetailView.as_view(),name="cand-detailjob"),
    path("jobs/apply-now/<int:id>",views.apply_now,name="applynow")
]