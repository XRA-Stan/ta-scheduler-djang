from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from ta_app.forms import CourseAdminForm
from .models import Section, Course

from ta_app.forms import CourseForm
from ta_scheduler.models import Course


def HomePageTemplate(request):
    return render(request, 'HomePageTemplate.html')


@login_required
def courses(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        section_id = request.POST.get('course_section')
        instructor_id = request.POST.get('course_instructor')

        section = Section.objects.get(id=section_id) if section_id else None
        instructor = User.objects.get(id=instructor_id) if instructor_id else None

        Course.objects.create(
            courseName=course_name,
            sections=section,
            instructor=instructor
        )

        return redirect('courses')

    sections = Section.objects.all()
    instructors = User.objects.all()
    allcourses = Course.objects.all()

    return render(request, 'Courses.html', {
        'sections': sections,
        'instructors': instructors,
        'courses': allcourses,
    })


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


@login_required()
def course_detail(request, course_id):
    # either you find the course or you dont
    course = get_object_or_404(Course, id=course_id)
    # Renders the html for the course that is clicked
    return render(request, 'course_detail.html', {'course': course})
