from zzz_lib.zzz_log import zzz_print
import json
from uuid import uuid4
from django.shortcuts import render
from base64 import b64decode, b64encode
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import connection
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.utils import timezone
from django.views.generic.edit import FormView
from django.contrib import messages

from django.views.generic import (
    ListView,
    UpdateView,
    DetailView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import (
    AccDeactivateForm,
    PasswordUpdateForm,
)
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from prof_candidate.models import (DeactivatedAccount,)
from django.contrib.auth import update_session_auth_hash

from commonroom.myfunctions.send_email import send_email_customized
import datetime

TEMPLATE_DIR = "prof_candidate/layout/acct_settings/"




##***************************************************
class AcctSettingsHomeView(LoginRequiredMixin, TemplateView):
    template_name = TEMPLATE_DIR + "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['section_header_1'] = 'Your Basic Information'
        context['section_header_2'] = 'Account Deactivation Form'
        return context




# password change form
##***************************************************
class UpdatePassView(LoginRequiredMixin, PasswordChangeView):
    template_name = TEMPLATE_DIR + "update_pass.html"
    success_url = reverse_lazy('prof_candidate:update_password')
    form_class = PasswordUpdateForm

    def form_valid(self, form):
        messages.success(self.request, "Password Updated Successfully")
        form.save()
        form.user = self.request.user
        subject = "Password Updated Successfully"
        email_body = "You have successfully updated Your password"        
        time = datetime.datetime.now()
        send_email_customized(self.request.user.email,subject,email_body,time)
        update_session_auth_hash(self.request, form.user)
        return super(UpdatePassView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['section_header_1'] = 'Update Your Password'
        context['section_header_2'] = 'Account Deactivation Form'
        return context




# Deactivation form submission
##***************************************************
class AccountDeactivationView(LoginRequiredMixin, CreateView):
    template_name = TEMPLATE_DIR+"acct_deactivate.html"
    form_class = AccDeactivateForm
    success_url = "deactivate_account_done"
    model = DeactivatedAccount      
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.email = self.request.user.email

        # save the form 
        self.object.save()

        subject = "Account Deactivation"
        email_body = "You have deactivated your account"   
        time = datetime.datetime.now()     
        send_email_customized(self.request.user,subject,email_body,time)
        logout(self.request)

        return render(self.request,  TEMPLATE_DIR+"acct_deactivate_done.html")


    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AccountDeactivationView, self).get_form_kwargs(*args, **kwargs)
        kwargs['email'] = self.request.user.email
        return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['section_header_1'] = 'Deactivate Your Account'
        context['section_header_2'] = 'Account Deactivation Form'
        return context




# Confirm Deactivation View
##***************************************************
class AccDeactivateConfirmView(LoginRequiredMixin, TemplateView):
    template_name = TEMPLATE_DIR+"acct_deactivate_done.html"

