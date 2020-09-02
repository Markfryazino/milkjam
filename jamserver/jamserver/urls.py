"""jamserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from datacatcher import views as catcher
from api import views as api
from tester import views as tester

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catcher/', catcher.index),
    path('api/v1/start-run', api.start_run),
    path('api/v1/get-snapshot', api.get_snapshot),
    path('api/v1/make-action', api.make_action),
    path('api/v1/end-run', api.end_run),
    path('run/', tester.index)
]
