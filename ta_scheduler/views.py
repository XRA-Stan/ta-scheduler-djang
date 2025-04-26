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
    
def courseDeletion(course_id):
    Course.objects.filter(id=course_id).delete()

@login_required
def courses(request, course=None):
    if request.method == 'POST':
            if 'delete_course_id' in request.POST:
            course_id = request.POST.get('delete_course_id')
            courseDeletion(course_id)
        #if the request post is to add it will do this
        else:
            courseCreation(request)
        course_name = request.POST.get('course_name')
        section_id = request.POST.get('course_section')
        instructor_id = request.POST.get('course_instructor')

        section = Section.objects.get(id=section_id) if section_id else None
        instructor = User.objects.get(id=instructor_id) if instructor_id else None

        new_course = Course.objects.create(
            courseName=course_name,
        )
        if section:
            section.course = new_course  # Using new_course instead of course
            section.save()

        if instructor and section:
            section.instructor = instructor
            section.save()

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
    sections = course.sections.all()
    print(f"DEBUG: Found {sections.count()} sections for course {course.courseName}")
    for section in sections:
        print(f"DEBUG: Section {section.sectionName}, Day: {section.get_dayOfWeek_display()}")

    return render(request, 'course_detail.html', {'course': course})
