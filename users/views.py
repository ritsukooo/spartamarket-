from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# # Create your views here.
# def users(request):
#     return render(request, "users/users.html")
 

@login_required
def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    context = {
        "member": member,
        "username":username
    }
    return render(request, "users/profile.html", context)





@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_pk)
        if request.user != member:
            if member in request.user.following.all():
                request.user.following.remove(member)
            else:
                request.user.following.add(member) 
        return redirect("users:profile",username=member.username)
    return redirect("accounts:login")

