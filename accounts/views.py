from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from social_django.models import UserSocialAuth

from .forms import SignUpForm, UserInformationUpdateForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('catalog')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(SuccessMessageMixin, UpdateView):
    form_class = UserInformationUpdateForm
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('my_account')
    success_message = 'Account updated'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            github_login = self.request.user.social_auth.get(provider='github')
        except UserSocialAuth.DoesNotExist:
            github_login = None
        context['github_login'] = github_login
        return context
