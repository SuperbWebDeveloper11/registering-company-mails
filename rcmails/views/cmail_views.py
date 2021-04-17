from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.core.mail import send_mail
# messages framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# class-based generic views
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# import models
from django.contrib.auth.models import User
from ..models import Cmail
from ..forms import CmailForm


################## views for cmail crud operations ################## 

class CmailList(ListView): # retrieve all cmails
    model = Cmail
    template_name = 'rcmails/cmail/cmail_list.html'
    context_object_name = 'cmail_list'
    paginate_by = 5


class CmailDetail(DetailView): # retrieve cmail detail
    model = Cmail
    template_name = 'rcmails/cmail/cmail_detail.html'
    context_object_name = 'cmail'


class CmailCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create new cmail 
    model = Cmail
    template_name = 'rcmails/cmail/cmail_form_create.html' 
    form_class = CmailForm
    success_message = "cmail was created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user # add cmail created_by manually
        return super().form_valid(form)


class CmailUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update cmail 
    model = Cmail
    template_name = 'rcmails/cmail/cmail_form_update.html' 
    form_class = CmailForm
    success_message = "cmail was updated successfully"

    def form_valid(self, form):
        if form.instance.created_by == self.request.user: # user should be the one who create cmail 
            return super().form_valid(form)
        else:
            return HttpResponse("You couldn't perform this opertaion ")

class CmailDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView): # delete cmail 
    model = Cmail
    template_name = 'rcmails/cmail/cmail_confirm_delete.html' 
    success_message = "cmail was deleted successfully"
    success_url = reverse_lazy('rcmails:cmail_list')

    def form_valid(self, form):
        if form.instance.publisher == self.request.user: # user should be the one who create cmail 
            return super().form_valid(form)
        else:
            return HttpResponse("You couldn't perform this opertaion ")


