"""
URL configuration for graph_explorer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("workspace/<str:workspace_id>", views.workspace, name="workspace"),
    path(
        "workspace-config",
        views.workspace_configuration,
        name="workspace_config",
    ),
    path(
        "workspace-config/<str:id_>",
        views.workspace_configuration,
        name="workspace_edit",
    ),
    path(
        "workspace-config/<str:datasource_name>",
        views.workspace_configuration,
    ),
    path("", views.index, name="index"),
    path(
        "select-visualizer/<str:visualizer_name>",
        views.select_visualizer,
        name="select_visualizer",
    ),
    path("load-views", views.load_views, name="load_views"),
    path("provide-data", views.provide_data, name="provide_data"),
    path("search", views.search, name="search"),
    path("delete-filter", views.delete_filter, name="delete_filter"),
    path('workspace-edit/<str:id>/', views.edit_workspace, name='edit_workspace'),
    path('workspace-delete/<str:id>/', views.delete_workspace, name='delete_workspace'),
]
