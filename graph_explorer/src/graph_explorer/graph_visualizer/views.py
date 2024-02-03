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
        ],
        "visualizers": [
            {
                "name": "Simple visualizer",
                "id": 1
            },
            {
                "name": "Block visualizer",
                "id": 2
            }
        ],
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
            },
        ],
        "visualizers": [
            {
                "name": "Simple visualizer",
                "id": 1
            },
            {
                "name": "Block visualizer",
                "id": 2
            }
        ],
        "main_views": [
            {
                "visualizer_id": 2,
                "html": "<h2>Visualizer 2</h2>",
            },
            {
                "visualizer_id": 1,
                "html": "<h2>Visualizer 1</h2>",
            }
        ],
        "bird_views": [
            {
                "visualizer_id": 2,
                "html": "<h2>Bird view 2</h2>",
            },
            {
                "visualizer_id": 1,
                "html": "<h2>Bird view 1</h2>",
            }
        ]

    })
