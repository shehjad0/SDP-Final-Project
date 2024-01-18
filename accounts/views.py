from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self,form):
        user = form.save()
        
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f'http://{current_site.domain}/accounts/activate/{uid}/{token}'
        
        message = render_to_string("accounts/confirmation_mail.html", { 'user' : user, 'confirm_link': confirm_link })
        send_email = EmailMultiAlternatives("Confirm your email", '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        response = super().form_valid(form)
        messages.success(
                self.request,
                f"Your Password Successfully Changed")
        
        message = render_to_string("accounts/change_password_email.html", { 'user' : self.request.user })
        send_email = EmailMultiAlternatives("Change Password", '', to=[self.request.user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        
        return super().form_valid(form)
    
class ActivateAccountView(View):
    def get(self, request, uid64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request, "Account activated. Please login.")
            return redirect('login')
        else:
            messages.error(request, "Invalid activation link.")
            return redirect('register')