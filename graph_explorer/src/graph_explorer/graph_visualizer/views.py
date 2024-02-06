from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse

from .services import *
from .models import Workspace
from .module.content import ContentModule

content_module = ContentModule(
    apps.get_app_config("graph_visualizer").data_source_plugins,
    apps.get_app_config("graph_visualizer").visualizer_plugins,
)

app_config = apps.get_app_config("graph_visualizer")


def index(request):
    context = content_module.get_context()
    context["workspaces"] = [vars(ws) for ws in app_config.workspaces]

    return render(request, "index.html", context)


def select_visualizer(_, visualizer_name):
    content_module.select_visualizer(visualizer_name)
    return HttpResponseRedirect(reverse("index"))


def load_views(_):
    # TODO: Load main, bird and tree views
    return HttpResponseRedirect(reverse('index'))


def search(_, query):
    content_module.search(query)
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

    content_module.workspaces = [vars(ws) for ws in app_config.workspaces]
    content_module.workspace_id = workspace_id
    content_module.select_data_source(app_config.get_workspace(workspace_id).selected_datasource)
    content_module.set_graph(app_config.get_workspace(workspace_id).graph)

    context = content_module.get_context()

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
