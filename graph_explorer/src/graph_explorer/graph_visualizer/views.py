from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.apps.registry import apps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .services import *
from .models import Workspace
from .module.content import ContentModule
from core.filters.search_filter import SearchFilter
from core.filters.operator_filter import OperatorFilter

content_module = ContentModule(
    apps.get_app_config("graph_visualizer").data_source_plugins,
    apps.get_app_config("graph_visualizer").visualizer_plugins,
)

app_config = apps.get_app_config("graph_visualizer")
content_module.workspaces = app_config.workspaces


def index(request):
    context = content_module.get_context()
    context["workspaces"] = [vars(ws) for ws in app_config.workspaces]
    context["tree_view_data"] = {}
    context["nodes_dict"] = {}

    if content_module.workspace_id != content_module.INVALID_WORKSPACE_ID:
        return HttpResponseRedirect(
            reverse("workspace", kwargs={"workspace_id": content_module.workspace_id})
        )

    return render(request, "index.html", context)


def select_visualizer(_, visualizer_name):
    content_module.select_visualizer(visualizer_name)
    return HttpResponseRedirect(reverse("index"))


def load_views(_):
    # TODO: Load main, bird and tree views
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


def provide_data(request):
    if request.method != "POST":
        return
    kwargs = request.body.decode("utf-8")
    content_module.provide_data(kwargs)
    return HttpResponseRedirect(reverse("index"))


def workspace(request, workspace_id):
    if workspace_id not in list(map(lambda ws: ws.id, app_config.workspaces)):
        return HttpResponseNotFound("Workspace with given id not found.")

    active_workspace: Workspace = list(
        filter(lambda ws: ws.id == workspace_id, app_config.workspaces)
    )[0]
    tree_view_data = get_tree_view_data(active_workspace.get_filtered_graph())
    nodes_dict = get_node_dict(active_workspace.get_filtered_graph())

    content_module.workspaces = app_config.workspaces
    content_module.workspace_id = workspace_id
    content_module.select_data_source(
        app_config.get_workspace(workspace_id).selected_datasource
    )
    content_module.set_graph(app_config.get_workspace(workspace_id).graph)

    context = content_module.get_context()
    context["tree_view_data"] = vars(tree_view_data)
    context["nodes_dict"] = nodes_dict
    context["workspaces"] = [vars(ws) for ws in app_config.workspaces]

    return render(request, "index.html", context)


def workspace_configuration(request, datasource_name=None):
    data_sources = get_datasource_names()
    if datasource_name is None:
        datasource_name = data_sources[0]
    datasource_config_params = get_datasource_configuration(datasource_name)

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

        new_workspace = Workspace(
            workspace_name, datasource_name, form_data, app_config
        )
        app_config.add_workspace(new_workspace)

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
            current_workspace.get_filter_chain().remove_filter(search_filter)
        elif filter_json["type"] == "OperatorFilter":
            operator_filter = OperatorFilter(filter_json["attribute"], filter_json["operator"], filter_json["value"])
            current_workspace.get_filter_chain().remove_filter(operator_filter)
    except KeyError:
        return

    return HttpResponse(200, content_type="application/json")

def add_filter(request):
    try:
        attribute: str = request.POST["attribute"]
        operator: str = request.POST["operator"]
        value: str = request.POST["value"]
        current_workspace = content_module.get_current_workspace()
        operator_filter: OperatorFilter = OperatorFilter(attribute, operator, value)
        current_workspace.add_filter(operator_filter)
    except (KeyError, ValueError):
        return

    return HttpResponseRedirect(reverse('index'))