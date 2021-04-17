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
from ..models import Departement
from ..forms import DepartementForm


################## views for departement crud operations ################## 

class DepartementList(ListView): # retrieve all departements
    model = Departement
    template_name = 'rcmails/departement/departement_list.html'
    context_object_name = 'departement_list'
    paginate_by = 5


class DepartementDetail(DetailView): # retrieve departement detail
    model = Departement
    template_name = 'rcmails/departement/departement_detail.html'
    context_object_name = 'departement'


class DepartementCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create new departement 
    model = Departement
    template_name = 'rcmails/departement/departement_form_create.html' 
    form_class = DepartementForm
    success_message = "departement was created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user # add departement created_by manually
        return super().form_valid(form)


class DepartementUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update departement 
    model = Departement
    template_name = 'rcmails/departement/departement_form_update.html' 
    form_class = DepartementForm
    success_message = "departement was updated successfully"

    def form_valid(self, form):
        if form.instance.created_by == self.request.user: # user should be the one who create departement 
            return super().form_valid(form)
        else:
            return HttpResponse("You couldn't perform this opertaion ")

class DepartementDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView): # delete departement 
    model = Departement
    template_name = 'rcmails/departement/departement_confirm_delete.html' 
    success_message = "departement was deleted successfully"
    success_url = reverse_lazy('rcmails:departement_list')

    def form_valid(self, form):
        if form.instance.publisher == self.request.user: # user should be the one who create departement 
            return super().form_valid(form)
        else:
            return HttpResponse("You couldn't perform this opertaion ")


