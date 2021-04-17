from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
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

"""
This view consist 4 classes and 4 mixins

    CmailList: # main view render cmail_list.html 

    RenderListTempMixin: # mixin to render list_temp on get request
    RenderDetailTempMixin: # mixin to render detail_temp on get request
    RenderCreateTempMixin: # mixin to render create_temp on get request
    RenderUpdateTempMixin: # mixin to render update_temp on get request
    RenderDeleteTempMixin: # mixin to render delete_temp on get request

    CmailDetail: # render detail_temp on get request 
    CmailCreate: # render create_temp on get request , create new instance on post request
    CmailUpdate: # render update_temp on get request , update instance on post request
    CmailDelete: # render delete_temp on get request , delete instance on post request
"""


# main view render cmail_list.html 
class CmailList(ListView): 
    model = Cmail
    template_name = 'rcmails/cmail_for_jquery/cmail_list.html'
    context_object_name = 'cmail_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cmail_form'] = CmailForm()
        return context


# mixin to render list_temp on get request
class RenderListTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        data['form_is_valid'] = True
        cmail_list = Cmail.objects.all()
        context = {'cmail_list': cmail_list}
        data['list_temp'] = render_to_string('rcmails/cmail_for_jquery/partial_cmail_list.html', context, request=request)
        return JsonResponse(data)
 

# mixin to render create_temp on get request
class RenderCreateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        if self.badform: # when the user submit a bad form we need to return it back with errors
            data['form_is_valid'] = False
            cmail_form = self.badform
        cmail_form = CmailForm()
        context = {'form': cmail_form}
        data['create_temp'] = render_to_string('rcmails/cmail_for_jquery/partial_cmail_create.html', context, request=request)
        return JsonResponse(data)


# mixin to render update_temp on get request
class RenderUpdateTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        cmail_instance = get_object_or_404(Cmail, pk=kwargs['pk'])
        if self.badform: # when the user submit a bad form we need to return it back with errors
            cmail_form = self.badform
        cmail_form = CmailForm(instance=cmail_instance)
        context = {'form': cmail_form}
        data['update_temp'] = render_to_string('rcmails/cmail_for_jquery/partial_cmail_update.html', context, request=request)
        return JsonResponse(data)


# mixin to render delete_temp on get request
class RenderDeleteTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        cmail_instance = get_object_or_404(Cmail, pk=kwargs['pk'])
        cmail_form = CmailForm(instance=cmail_instance)
        context = {'form': cmail_form}
        data['delete_temp'] = render_to_string('rcmails/cmail_for_jquery/partial_cmail_delete.html', context, request=request)
        return JsonResponse(data)


# mixin to render detail_temp on get request
class RenderDetailTempMixin: 
    def get(self, request, *args, **kwargs): 
        data = dict()
        cmail_instance = get_object_or_404(Cmail, pk=kwargs['pk'])
        context = { 'cmail': cmail_instance }
        data['detail_temp'] = render_to_string(
                'rcmails/cmail_for_jquery/partial_cmail_detail.html', context, request=request
                )
        return JsonResponse(data)


# render detail_temp on get request 
class CmailDetail(RenderDetailTempMixin, View):
    pass


# render create_temp on get request , create new instance on post request
class CmailCreate(LoginRequiredMixin, RenderCreateTempMixin, RenderListTempMixin, View):
    badform = None
    
    def post(self, request, *args, **kwargs):
        form = CmailForm(request.POST)
        if form.is_valid(): 
            form.instance.created_by = request.user
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render update_temp on get request , update instance on post request
class CmailUpdate(LoginRequiredMixin, RenderUpdateTempMixin, RenderListTempMixin, View):
    badform = None

    def post(self, request, *args, **kwargs):
        cmail_instance = Cmail.objects.get(pk=kwargs['pk'])
        form = CmailForm(request.POST, instance=cmail_instance)
        if form.is_valid():
            if not request.user == cmail_instance.created_by:
                return HttpResponse('You can not edit this cmail')
            form.save()
            return RenderListTempMixin().get(request, *args, **kwargs)
        else:
            self.badform = form
            return super().get(request, *args, **kwargs)


# render delete_temp on get request , delete instance on post request
class CmailDelete(LoginRequiredMixin, RenderDeleteTempMixin, RenderListTempMixin, View):

    def post(self, request, *args, **kwargs):
        cmail_instance = get_object_or_404(Cmail, pk=kwargs['pk'])
        if not request.user == cmail_instance.created_by:
            return HttpResponse('You can not delete this cmail')
        cmail_instance.delete()
        return RenderListTempMixin().get(request, *args, **kwargs)

