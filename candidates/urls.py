from django.urls import path
from candidates import views

urlpatterns=[
    path("home",views.CandidateHomeView.as_view(),name="cand-home")
]