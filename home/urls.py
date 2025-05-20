from django.urls import path

from . import views
from .esc.urls import SrDUrls
from .project.urls import ProjectUrls

urlpatterns = [
    path('webhooks/reinstall',views.reinstall,name="webhooks_orders"),
    path('install',views.install,name="install")
]+SrDUrls.urlpatterns+ProjectUrls.urlpatterns
