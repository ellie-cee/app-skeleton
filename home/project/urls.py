from django.urls import path
from . import views as projectViews

class ProjectUrls:
    urlpatterns = [
        path("webhooks-subscription-handler",projectViews.subscriptionsHandler,name="subscriptions")
    ]