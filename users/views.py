from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth import get_user_model
from .forms import UserForm
from django.views.generic.detail import DetailView
from .models import User


User = get_user_model()
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    ordering = ['full_name']

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

def user_delete(request, pk):
    u = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        u.delete()
    return redirect('user-list')

class UserDetailView(DetailView):
    model = User
    template_name = 'users/view_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.path.endswith('confirm_delete/'):
            context['delete_mode'] = True
        return context

