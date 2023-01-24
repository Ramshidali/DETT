import datetime
import json
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from delivery_agents.forms import AgentForm
from delivery_agents.models import DeliveryAgent
from general.decorators import check_mode


@check_mode
@login_required
def delivery_agents(request):
    instances = DeliveryAgent.objects.filter(is_deleted=False)
    query = request.GET.get('q')
    if query:
        instances = instances.filter(
            Q(name__icontains=query))
    context = {
        "title": "Agents",
        "instances": instances,
        "is_da": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'agents/agents/agents.html', context)


@login_required
def create_agent(request):
    if request.method == "POST":
        form = AgentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Created',
                'message': 'Agent Sucessfully Created',
                "redirect": 'true',
                "redirect_url": reverse('delivery_agents:agent', kwargs={"pk": data.pk})
            })
        else:

            return JsonResponse({'error': True, 'errors': form.errors})

    else:
        form = AgentForm()
        context = {
            "form": form,
            "title": "Create agent",
            "redirect": True,
            "url": reverse("delivery_agents:create_agent"),
            "is_da": True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'agents/agents/entry.html', context)


@login_required
def agent(request, pk):
    instance = get_object_or_404(DeliveryAgent.objects.filter(pk=pk))
    context = {
        "title": "Agent : " + instance.name,
        "instance": instance,
        "is_da": True,

        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }

    return render(request, 'agents/agents/agent.html', context)


@login_required
def edit_agent(request, pk):
    instance = get_object_or_404(DeliveryAgent.objects.filter(pk=pk))
    if request.method == "POST":
        form = AgentForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            pk = data.pk

            return JsonResponse({
                "status": "true",
                'error': False,
                'title': 'Successfully Updated',
                'message': 'Agent Sucessfully Updated',
                "redirect": 'true',
                "redirect_url": reverse('delivery_agents:agent', kwargs={"pk": pk})
            })

        else:
            print("errorrs====>>",form._errors)
            print(form)
            return JsonResponse({'error': True, 'errors': form, })

    else:
        form = AgentForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Agent",
            "redirect": True,
            "url": reverse("delivery_agents:edit_agent", kwargs={"pk": pk}),
            "pk": pk,
            "is_da": True,

            "edit":True,

            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, 'agents/agents/entry.html', context)


# @login_required
# def edit_agent(request, pk):
#     instance = get_object_or_404(DeliveryAgent.objects.filter(pk=pk))
#     if request.method == "POST":
#         form = AgentForm(request.POST, instance=instance)
#         if form.is_valid():
#             data = form.save(commit=False)
#             pk = data.pk
#
#             return JsonResponse({
#                 "status": "true",
#                 'error': False,
#                 'message': 'Agent Updated',
#                 "redirect": 'true',
#                 "redirect_url": reverse('delivery_agents:agent', kwargs={"pk": pk})
#             })
#
#         else:
#
#             return JsonResponse({'error': True, 'errors': form, })
#
#     else:
#         form = AgentForm(instance=instance)
#         context = {
#             "form": form,
#             "title": "Edit Agent",
#             "redirect": True,
#             "url": reverse("delivery_agents:edit_agent", kwargs={"pk": pk}),
#             "pk": pk,
#             "is_da": True,
#             "is_product": True,
#
#             "is_need_select_picker": True,
#             "is_need_popup_box": True,
#             "is_need_custom_scroll_bar": True,
#             "is_need_wave_effect": True,
#             "is_need_bootstrap_growl": True,
#             "is_need_chosen_select": True,
#             "is_need_grid_system": True,
#             "is_need_datetime_picker": True,
#             "is_need_animations": True,
#         }
#
#         return render(request, 'agents/agents/entry.html', context)


@login_required
def delete_agent(request, pk):
    DeliveryAgent.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Agent Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('delivery_agents:delivery_agents')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')