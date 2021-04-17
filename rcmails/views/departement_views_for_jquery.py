from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
# class-based generic views
from django.views.generic import ListView, View
# import models
from django.contrib.auth.models import User
from ..models import Departement
from ..forms import DepartementForm # we'll use this form to create and update instance


"""
function based views (hardcoded) to perform crud operations for ajax requests
    1- departement_list (render departement list template)
    2- departement_detail (return departement detail template)
    3- departement_create (return departement create template && save new departement)
    4- departement_update (return departement update template && update departement)
    5- departement_delete (return departement delete template && delete departement)
"""


def departement_list(request): 
    """ render departement list template """

    template_list = 'rcmails/departement_for_jquery/departement_list.html'
    departement_list = Departement.objects.all()
    context = {'departement_list': departement_list, 'departement_form': DepartementForm()}
    return render(request, template_list, context)


def departement_detail(request, pk):
    """ return departement detail template """

    template_error = 'rcmails/departement_for_jquery/partial_error_msg.html'
    template_detail = 'rcmails/departement_for_jquery/partial_departement_detail.html'

    if not request.user.is_authenticated: # user should be logged in
        error_temp = render_to_string(template_error, request=request)
        return JsonResponse({'modal_temp': error_temp})
    else:
        try:
            # return partial_departement_detail template 
            instance = Departement.objects.get(pk=pk)
            context = { 'departement': instance }
            detail_temp = render_to_string(template_detail, context, request=request)
            return JsonResponse({'modal_temp': detail_temp})
        except: # propably departement not found
            error_temp = render_to_string(template_error, request=request)
            return JsonResponse({'modal_temp': error_temp})


def departement_create(request):
    """ return departement create template && save new departement """

    template_error = 'rcmails/departement_for_jquery/partial_error_msg.html'
    template_create = 'rcmails/departement_for_jquery/partial_departement_create.html'
    template_list = 'rcmails/departement_for_jquery/partial_departement_list.html'

    if not request.user.is_authenticated: # user should be logged in
        error_temp = render_to_string(template_error, request=request)
        return JsonResponse({'modal_temp': error_temp})
    else:
        if request.method == 'GET':
            # return partial_departement_create template with an empty form to create instance 
            context = {'form': DepartementForm()}
            create_temp = render_to_string(template_create, context, request=request)
            return JsonResponse({'modal_temp': create_temp})
        elif request.method == 'POST':
            form = DepartementForm(request.POST)
            if form.is_valid(): 
                # save the instance and return partial list template 
                form.instance.created_by = request.user
                form.save() 
                departement_list = Departement.objects.all()
                context = {'departement_list': departement_list}
                list_temp = render_to_string(template_list, context, request=request)
                return JsonResponse({'list_temp': list_temp, 'form_is_valid': True})
            else:
                # return partial create template with a form populated with the data previously submitted 
                context = {'form': form}
                create_temp = render_to_string(template_create, context, request=request)
                return JsonResponse({'modal_temp': create_temp, 'form_is_valid': False})


def departement_update(request, pk):
    """ return departement update template && update departement """

    template_error = 'rcmails/departement_for_jquery/partial_error_msg.html'
    template_update = 'rcmails/departement_for_jquery/partial_departement_update.html'
    template_list = 'rcmails/departement_for_jquery/partial_departement_list.html'

    if not request.user.is_authenticated: # user should be logged in
        error_temp = render_to_string(template_error, request=request)
        return JsonResponse({'modal_temp': error_temp})
    else:
        if request.method == 'GET':
            try:
                # return partial_departement_update template with bounded form 
                instance = Departement.objects.get(pk=pk)
                if request.user != instance.created_by: # the user should be the one who created the departement 
                    raise
                context = {'form': DepartementForm(instance=instance)}
                update_temp = render_to_string(template_update, context, request=request)
                return JsonResponse({'modal_temp': update_temp})
            except: # propably departement not found
                error_temp = render_to_string(template_error, request=request)
                return JsonResponse({'modal_temp': error_temp})
        elif request.method == 'POST':
            try:
                instance = Departement.objects.get(pk=pk)
                if request.user != instance.created_by: # the user should be the one who created the departement 
                    raise
                form = DepartementForm(request.POST, instance=instance)
                if form.is_valid(): 
                    # save the instance and return partial list template 
                    form.save() 
                    departement_list = Departement.objects.all()
                    context = {'departement_list': departement_list}
                    list_temp = render_to_string(template_list, context, request=request)
                    return JsonResponse({'list_temp': list_temp, 'form_is_valid': True})
                else:
                    # return partial update template with a form populated with the data previously submitted 
                    context = {'form': form}
                    update_temp = render_to_string(template_update, context, request=request)
                    return JsonResponse({'modal_temp': update_temp, 'form_is_valid': False})
            except: # propably departement not found
                error_temp = render_to_string(template_error, request=request)
                return JsonResponse({'modal_temp': error_temp})


def departement_delete(request, pk):
    """ return departement delete template && delete departement """

    template_error = 'rcmails/departement_for_jquery/partial_error_msg.html'
    template_delete = 'rcmails/departement_for_jquery/partial_departement_delete.html'
    template_list = 'rcmails/departement_for_jquery/partial_departement_list.html'

    if not request.user.is_authenticated: # user should be logged in
        error_temp = render_to_string(template_error, request=request)
        return JsonResponse({'modal_temp': error_temp})
    else:
        if request.method == 'GET':
            try:
                # return partial_departement_delete template with bounded form 
                instance = Departement.objects.get(pk=pk)
                if request.user != instance.created_by: # the user should be the one who created the departement 
                    raise
                context = {'form': DepartementForm(instance=instance)}
                delete_temp = render_to_string(template_delete, context, request=request)
                return JsonResponse({'modal_temp': delete_temp})
            except: # propably departement not found
                error_temp = render_to_string(template_error, request=request)
                return JsonResponse({'modal_temp': error_temp})
        elif request.method == 'POST':
            try:
                # delete the instance and return partial list template 
                instance = Departement.objects.get(pk=pk)
                if request.user != instance.created_by: # the user should be the one who created the departement 
                    raise
                instance.delete()
                departement_list = Departement.objects.all()
                context = {'departement_list': departement_list}
                list_temp = render_to_string(template_list, context, request=request)
                return JsonResponse({'list_temp': list_temp, 'form_is_valid': True})
            except: # propably departement not found
                error_temp = render_to_string(template_error, request=request)
                return JsonResponse({'modal_temp': error_temp})
 

