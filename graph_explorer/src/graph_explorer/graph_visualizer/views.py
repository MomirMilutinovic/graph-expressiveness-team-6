from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {
        "workspaces": [
            {
                "name": "Workspace 1",
                "id": 1
            },
            {
                "name": "Workspace 2",
                "id": 2
            }
        ]
    })


def workspace(request, workspace_id):
    return render(request, 'index.html', {
        "workspaces": [
            {
                "name": "Workspace 1",
                "id": 1
            },
            {
                "name": "Workspace 2",
                "id": 2
            }
        ]

    })
