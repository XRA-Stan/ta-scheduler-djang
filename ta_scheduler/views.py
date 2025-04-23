from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ta_app.forms import CourseAdminForm


def HomePageTemplate(request):
    return render(request, 'HomePageTemplate.html')

def courses(request):
    return render(request, 'Courses.html')
@login_required
def home(request):
    return render(request, 'Home.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'Login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'Login.html', {'error': None})

@login_required
def course_creation_view(request):
    if request.method == 'POST':
        form = CourseAdminForm(request.POST)
        if form.is_valid():
            form.save()  # Save the course to the database
            return render(request, 'course_form.html', {'form': form})  # Show the form again after submission
    else:
        form = CourseAdminForm()

    return render(request, 'course_form.html', {'form': form})
