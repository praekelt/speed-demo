from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

import rest_framework_extras
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers, serializers, viewsets
from formfactory import api as formfactory_api
from jmbo.admin import ModelBaseAdmin, ModelBaseAdminForm
from jmbo import api as jmbo_api
from listing import api as listing_api
from post import api as post_api


router = routers.DefaultRouter()

rest_framework_extras.discover(router)
rest_framework_extras.register(router)

# Register jmbo suite routers
formfactory_api.register(router)
jmbo_api.register(router)
listing_api.register(router)
post_api.register(router)

admin.autodiscover()

urlpatterns = [
    url(r"^", include("speed.urls", namespace="speed")),
    url(r"^mobius/", include("mobius.urls", namespace="mobius")),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^api/(?P<version>(v1))/", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^api-auth/$", obtain_jwt_token, name="obtain_token"),
    url(r"^auth/", include("django.contrib.auth.urls", namespace="auth")),
    url(
        r"^formfactory/",
        include("formfactory.urls", namespace="formfactory")
    ),
    url(r"^jmbo/", include("jmbo.urls", namespace="jmbo")),
    url(r"^link/", include("link.urls", namespace="link")),
    url(r"^listing/", include("listing.urls", namespace="listing")),
    url(r"^mote/", include("mote.urls", namespace="mote")),
    url(r"^navbuilder/", include("navbuilder.urls", namespace="navbuilder")),
    url(r"^post/", include("post.urls", namespace="post")),

    # Comments can't handle namespaces
    url(r"^comments/", include("django_comments.urls")),
    url(r"^nested_admin/", include("nested_admin.urls")),
]

if settings.DEBUG:
    # Host our own media
    urlpatterns += [
        url(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True}
        ),
    ]
    # Expose Django Debug Toolbar if we can import it
    try:
        import debug_toolbar
        urlpatterns += [
            url(r"^__debug__/", include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
