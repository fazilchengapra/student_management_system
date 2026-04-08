from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def course_list_view(req):
    print('called')
    if not req.user.is_staff:
        return redirect('login')
    
    return render(req, 'admin/course/course_list.html')