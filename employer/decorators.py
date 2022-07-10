from django.contrib import messages
from django.shortcuts import redirect
def signin_required(fn):
    def wrapper(request,*args,**kwargs):   #innerfunction
             if request.user.is_authenticated:
                 return fn(request,*args,**kwargs)
             else:
                 messages.error(request,"you must login")
                 return redirect("signin")
    return wrapper #calling innerfn