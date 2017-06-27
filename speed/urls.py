from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from speed import views


urlpatterns = [
    url(
        r"^$",
        TemplateView.as_view(template_name="speed/home.html"),
        name="home"
    ),
    url(
        r"^tree1/$",
        views.TreeView1.as_view(template_name="speed/tree1.html"),
        name="tree1"
    ),
    url(
        r"^tree2/$",
        views.TreeView2.as_view(template_name="speed/tree2.html"),
        name="tree2"
    ),
    url(
        r"^tree3/$",
        views.TreeView3.as_view(template_name="speed/tree3.html"),
        name="tree3"
    ),
    url(
        r"^tree4/$",
        views.TreeView4.as_view(template_name="speed/tree4.html"),
        name="tree4"
    )
]
