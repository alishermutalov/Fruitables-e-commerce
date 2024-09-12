from django.shortcuts import redirect
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from home.models import Order
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from .models import Profile
from django.contrib.auth.views import LoginView
from .forms import LoginForm, RegisterForm, EditProfileForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')  # Redirect after successful registration

    def form_valid(self, form):
        # Save the user form but don’t save it again explicitly
        response = super().form_valid(form)
        # Log the user in immediately after registering
        # login(self.request, self.object)  # self.object refers to the saved user
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)  # Log the user in
        return redirect('home')

    



def custom_logout_view(request):
    logout(request)  # This will log out the user
    return redirect(reverse('home')) 




class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Get the profile for the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get orders for the logged-in user
        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-created_at')
        return context
    

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile_detail')  # Redirects to profile view after successful update

    def get_object(self, queryset=None):
        # Get the profile object for the logged-in user
        return self.request.user.profile

    def form_valid(self, form):
        # Save the user information along with the profile
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        return super().form_valid(form)