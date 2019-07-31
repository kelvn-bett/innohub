from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from strathideasapp.tokens import account_activation_token
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView, TemplateView
from django.shortcuts import get_object_or_404
from .models import Ideas
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
# Create your views here.


def email(request):
    subject = 'Thank you for registering to Ideation'
    message = ' This is the beginning of sharing and incubation of your ideas'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['dennisndungu68@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('login')


def home(request):
    context = {
        'ideas': Ideas.objects.all()
    }
    return render(request, "strathideasapp/ideas_list.html", context)


class HomeView(TemplateView):
    template_name = 'strathideasapp/index.html'


class IdeaListView(ListView):
    model = Ideas
    template_name = 'strathideasapp/ideas_list.html'
    context_object_name = 'ideas'
    ordering = ['-date_posted']
    paginate_by = 3


class IdeaDetailView(DetailView):
    model = Ideas
    template_name = 'strathideasapp/ideas_detail.html'


class IdeaLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Ideas, idea=kwargs['pk'])
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            obj.likes.add(user)
        else:
            obj.likes.remove(user)
        return url_


class IdeaCreateView(LoginRequiredMixin, CreateView):
    model = Ideas
    fields = ['title', 'problem_statement', 'executive_summary', 'objectives', 'limitations']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IdeaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ideas
    fields = ['title', 'problem_statement', 'executive_summary', 'objectives', 'limitations']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):  # check is the user updating is the owner of the idea
        idea = self.get_object()
        if self.request.user == idea.user:
            return True
        return False


class IdeaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ideas
    template_name = 'strathideasapp/ideas_confirm_delete.html'

    def test_func(self):
        idea = self.get_object()
        if self.request.user == idea.user:
            return True
        return False


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your InnoHub account.'
            message = render_to_string('strathideasapp/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            # username = form.cleaned_data.get('username')
            # messages.success(request, f'Welcome {username}, your account has been created.
            # Please Login with your credentials')
            # return redirect('login')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}')
    else:
        form = UserRegistrationForm()
    return render(request, "strathideasapp/user_signup.html", context={"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def profile(request):
        if request.method == 'POST':
            user_update_form = UserUpdateForm(request.POST, instance=request.user)
            profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if user_update_form.is_valid() and profile_update_form.is_valid():
                user_update_form.save()
                profile_update_form.save()
                messages.success(request, f'Your account has been updated')
                return redirect('profile')
        else:
            user_update_form = UserUpdateForm(instance=request.user)
            profile_update_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_update_form': user_update_form,
            'profile_update_form': profile_update_form,
        }
        return render(request, 'strathideasapp/user_profile.html', context)
