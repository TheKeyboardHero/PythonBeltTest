from django.conf.urls import include, url
from django.conf import settings
# from django.urls import url
from . import views
from django.contrib import admin

urlpatterns = [
	url(r'^$', views.index),
    # url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
    url(r'^landing/$', views.landing),
	url(r'^trips/$', views.trips),
	url(r'^createJoinTrip/$', views.createJoinTrip),
	url(r'^destroyJoinTrip/$', views.destroyJoinTrip),
	url(r'^about_trip/', views.about_trip),
]