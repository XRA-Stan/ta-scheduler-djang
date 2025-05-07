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
from .models import Section, Course

from ta_app.forms import CourseForm
from ta_scheduler.models import Course


def HomePageTemplate(request):
    return render(request, 'HomePageTemplate.html')


def courseDeletion(course_id):
    Course.objects.filter(id=course_id).delete()

def courseCreation(request):
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
    instructors = User.objects.all()
    allcourses = Course.objects.all()


    return render(request, 'Courses.html', {
        'sections': sections,
        'instructors': instructors,
        'courses': allcourses,
        'SEMESTER_CHOICES': Course.SEMESTER_CHOICES,


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
