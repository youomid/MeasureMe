"""mm_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

# standard library imports

# third party imports
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

# local imports
from mm_api.views import (
        DashboardView,
    )
from mm_api.viewsets import SimulationViewSet


router = DefaultRouter()
router.register(r'simulations', SimulationViewSet, 'simulations')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', DashboardView.as_view()),
]

