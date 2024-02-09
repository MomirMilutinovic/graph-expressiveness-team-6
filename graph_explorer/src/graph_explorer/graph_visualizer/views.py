import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from typing import Any

from core.filters.search_filter import SearchFilter
from core.models import Workspace
from core.filters.operator_filter import OperatorFilter
from core.content import ContentModule
from core.services import coerce_filter_value

from .services import *

content_module: ContentModule = apps.get_app_config(
    "graph_visualizer"
).get_content_module()


def index(request):
    context = content_module.get_context()
    context["tree_view_data"] = {}
    context["nodes_dict"] = {}

    active_workspace_id = content_module.get_active_workspace_id()
    if active_workspace_id != content_module.INVALID_WORKSPACE_ID:
        return HttpResponseRedirect(
            reverse("workspace", kwargs={"workspace_id": active_workspace_id})
        )

    return render(request, "index.html", context)


def select_visualizer(_, visualizer_name):
    content_module.select_visualizer(visualizer_name)
    return HttpResponseRedirect(reverse("index"))


def search(request):
    try:
        query: str = request.POST["query"]
        current_workspace = content_module.get_current_workspace()
        search_filter: SearchFilter = SearchFilter(query)
        current_workspace.add_filter(search_filter)
    except (KeyError, ValueError):
        return

    return HttpResponseRedirect(reverse("index"))


def workspace(request, workspace_id):
    if workspace_id not in list(map(lambda ws: ws.id, content_module.workspaces)):
        return HttpResponseNotFound("Workspace with given id not found.")

    active_workspace: Workspace = content_module.get_workspace(workspace_id)

    tree_view_data = get_tree_view_data(active_workspace.get_filtered_graph())
    nodes_dict = get_node_dict(active_workspace.get_filtered_graph())

    content_module.set_active_workspace_id(workspace_id)
    content_module.select_data_source(
        content_module.get_workspace(workspace_id).selected_datasource
    )
    content_module.set_graph(content_module.get_workspace(workspace_id).graph)

    context = content_module.get_context()
    context["tree_view_data"] = tree_view_data
    context["nodes_dict"] = nodes_dict

    return render(request, "index.html", context)


def workspace_configuration(request, datasource_name=None):
    data_sources = get_datasource_names()
    if datasource_name is None:
        datasource_name = data_sources[0]

    datasource_config_params = content_module.get_datasource_configuration(
        datasource_name
    )

    if request.method == "GET":
        return render(
            request,
            "workspace_config.html",
            {
                "parameters": datasource_config_params.items(),
                "data_sources": data_sources,
                "selected_ds": datasource_name,
            },
        )
    elif request.method == "POST":
        form_data = request.POST.dict()
        workspace_name = form_data.get("workspace-name")
        del form_data["workspace-name"]
        del form_data["csrfmiddlewaretoken"]

        try:
            new_workspace = Workspace(
                workspace_name, datasource_name, form_data, content_module
            )
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=400)

        content_module.add_workspace(new_workspace)

        return HttpResponseRedirect(
            reverse("workspace", kwargs={"workspace_id": new_workspace.id})
        )


@csrf_exempt
def delete_filter(request):
    try:
        current_workspace = content_module.get_current_workspace()
        filter_json = json.loads(request.body)
        if filter_json["type"] == "SearchFilter":
            search_filter = SearchFilter(filter_json["search_term"])
            current_workspace.remove_filter(search_filter)
        elif filter_json["type"] == "OperatorFilter":
            operator_filter = OperatorFilter(
                filter_json["attribute"], filter_json["operator"], filter_json["value"]
            )
            current_workspace.remove_filter(operator_filter)
    except KeyError:
        return

    return HttpResponse(200, content_type="application/json")


def edit_workspace(request, id, datasource_name=None):
    data_sources = get_datasource_names()
    ws: Workspace = content_module.get_workspace(id)
    if ws is None:
        return HttpResponseNotFound("Workspace with given id not found.")
    datasource_name = (
        ws.selected_datasource if datasource_name is None else datasource_name
    )

    datasource_config_params = content_module.get_datasource_configuration(
        datasource_name
    )
    ds_config_params = datasource_config_params.items()
    ds_config_params_with_values = []
    for key, key_type in ds_config_params:
        value = ""
        if datasource_name == ws.selected_datasource:
            value = ws.datasource_config[key]
        ds_config_params_with_values.append((key, key_type, value))

    if request.method == "GET":
        return render(
            request,
            "workspace_edit.html",
            {
                "parameters": ds_config_params_with_values,
                "data_sources": data_sources,
                "selected_ds": datasource_name,
                "workspace": ws,
            },
        )
    elif request.method == "POST":
        form_data = request.POST.dict()
        workspace_name = form_data.get("workspace-name")
        del form_data["workspace-name"]
        del form_data["csrfmiddlewaretoken"]

        try:
            ws.set_data_source(datasource_name, form_data, content_module)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=400)
        ws.name = workspace_name
        return HttpResponseRedirect(
            reverse("workspace", kwargs={"workspace_id": content_module.workspace_id})
        )
    else:
        return HttpResponse(404, content_type="application/json")


def delete_workspace(request, id):
    global content_module
    try:
        is_active_workspace = content_module.get_active_workspace_id() == id

        content_module.delete_workspace(id)
        if content_module.get_number_of_workspaces() == 0:
            content_module = apps.get_app_config(
                "graph_visualizer"
            ).get_content_module()
            return HttpResponseRedirect(reverse("index"))
        elif is_active_workspace:
            return HttpResponseRedirect(
                reverse(
                    "workspace",
                    kwargs={"workspace_id": content_module.workspaces[0].id},
                )
            )
        else:
            referer_url = request.META.get("HTTP_REFERER", reverse("index"))
            return HttpResponseRedirect(referer_url)
    except Exception as e:
        return HttpResponse("An error occurred during workspace deletion.", status=500)


def add_filter(request):
    try:
        attribute: str = request.POST["attribute"]
        operator: str = request.POST["operator"]
        unfiltered_graph = content_module.get_current_workspace().get_unfiltered_graph()
        value: Any = coerce_filter_value(
            request.POST["value"], attribute, unfiltered_graph, operator
        )
        current_workspace = content_module.get_current_workspace()
        operator_filter: OperatorFilter = OperatorFilter(attribute, operator, value)
        current_workspace.add_filter(operator_filter)
    except (KeyError, ValueError, TypeError) as e:
        return HttpResponse(str(e), content_type="text/plain", status=400)

    return HttpResponseRedirect(
        reverse("workspace", kwargs={"workspace_id": current_workspace.id})
    )
