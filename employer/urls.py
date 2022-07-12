from django.urls import path
from employer import views
urlpatterns=[
  path('home',views.EmployerHomeview.as_view(),name="emp-home"),
  path('jobs/add',views.AddJobView.as_view(),name="emp-addjob"),
  path("jobs/all",views.ListJobView.as_view(),name="emp-alljobs"),
  path("jobs/details/<int:id>",views.JobDetailsView.as_view(),name="emp-jobdetails"),
  path("jobs/edit/<int:id>",views.JobEditView.as_view(),name="emp-jobedit"),
  path("jobs/remove/<int:id>",views.JobDeleteView.as_view(),name="emp-jobdelete"),
  path("users/accounts/signup",views.SignUpView.as_view(),name="signup"),
  path("users/accounts/signin",views.SignInview.as_view(),name="signin"),
  path("users/accounts/signout",views.signout_view,name="signout"),
  path("users/accounts/passwordchange",views.ChangePasswordView.as_view(),name="change-password"),
  path("users/accounts/passwordreset",views.PasswordResetView.as_view(),name="reset-password"),
  path("profile/add",views.CompanyProfileView.as_view(),name="emp-addprofile"),
  path("profile/detail",views.EmpViewProfileView.as_view(),name="emp-viewprofile"),# here the id is not necessary because models related name=employer has given.so
  path("profile/edit/<int:id>",views.EmpEditProfileView.as_view(),name="emp-editprofile"),
  path("applications/all/<int:id>",views.EmployeeListApplications.as_view(),name="emp-appjoblist"),
  path("applications/details/<int:id>",views.EmployeeApplicationDetailView.as_view(),name="emplyee-detailapp"),
  path("job/applications/status/change/<int:id>",views.reject_application,name="reject-application"),
  path("application/accept/<int:app_id>",views.accept_application,name="accept-application")


]
#safe operation-get,list
#unsafe-put,patch,delete,create