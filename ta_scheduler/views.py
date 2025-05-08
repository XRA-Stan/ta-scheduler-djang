from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from ta_app.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from ta_app.forms import CourseAdminForm
from .models import Section, Course, DAYS_OF_WEEK

from ta_app.forms import CourseForm
from ta_scheduler.models import Course


def HomePageTemplate(request):
    return render(request, 'HomePageTemplate.html')


def courseDeletion(course_id):
    Course.objects.filter(id=course_id).delete()

def courseCreation(request):
    course_name = request.POST.get('course_name')
    semester_choice = request.POST.get('semester')
    course_year = request.POST.get('year')



    Course.objects.create(
        courseName=course_name,
        semester=semester_choice,
        year=course_year,
    )



@login_required
def courses(request):
    if request.method == 'POST':
        #if the request post is delete it will do this
        if 'delete_course_id' in request.POST:
            course_id = request.POST.get('delete_course_id')
            courseDeletion(course_id)
        #if the request post is to add it will do this
        else:
            courseCreation(request)


        return redirect('courses')

    sections = Section.objects.all()
    allcourses = Course.objects.all()
    users = User.objects.filter(role__in=['ta', 'instructor'])

    return render(request, 'Courses.html', {
        'sections': sections,
        'courses': allcourses,
        'SEMESTER_CHOICES': Course.SEMESTER_CHOICES,
        'users': users,


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


def redirectToCourse():
    return redirect('courses')


def sectionCreation(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        section_name = request.POST.get('section_name')
        day_of_week = request.POST.get('day1')
        day_of_week_optional = request.POST.get('day2')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        teacher_id = request.POST.get('teacher')

        teacher = User.objects.filter(id=teacher_id).first()

        if teacher.role == 'instructor':
            instructor = teacher
            ta = None
        elif teacher.role == 'ta':
            instructor = None
            ta = teacher
        else:
            instructor = None
            ta = None

        Section.objects.create(
            course=course,
            sectionName=section_name,
            dayOfWeek=day_of_week,
            dayOfWeek2 = day_of_week_optional,
            timeOfDay=start_time,
            endOfDay=end_time,
            instructor=instructor,
            teaching_assistant=ta,

        )
    return redirect('course_detail', course_id=course_id)

@login_required()
def course_detail(request, course_id):
    # either you find the course or you dont
    course = get_object_or_404(Course, id=course_id)
    users = User.objects.filter(role__in=['ta', 'instructor'])
    if request.method == 'POST':
        if 'back-button' in request.POST:
            return redirectToCourse()
        else:
            return sectionCreation(request, course_id)

    sections = Section.objects.filter(course=course)
    # Renders the html for the course that is clicked
    return render(request, 'course_detail.html', {
        'course': course,
        'users': users,
        'DAYS_OF_WEEK': DAYS_OF_WEEK,
        'sections': sections,


    })



User = get_user_model()

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'admin'

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    ordering = ['full_name']

class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user-list')

class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user-list')

class UserDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = 'view_profile.html'
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['delete_mode'] = self.request.path.endswith('confirm_delete/')
        return ctx

def user_delete(request, pk):
    if request.method == 'POST' and request.user.role == 'admin':
        get_object_or_404(User, pk=pk).delete()
    return redirect('user-list')
