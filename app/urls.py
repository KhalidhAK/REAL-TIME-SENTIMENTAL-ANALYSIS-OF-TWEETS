from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^result/(?P<data>[a-z]+)/',views.main ),
    url(r'^input/',views.getInput)
]