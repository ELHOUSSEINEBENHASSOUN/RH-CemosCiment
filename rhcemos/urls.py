from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("signin/", signin, name="signin"),
    path('signout/', signout, name='signout'),
    path("dashboard/", dashboard, name="dashboard"),
    path("contact/", contact, name="contact"),
    path("profile/", profile, name="profile"),
    path("update_status/", update_status, name="update_status"),
    path("users/", users, name="users"),
    path("attestation/", demande_attestation, name="attestation"),
    path('approve_attestation/<int:demande_id>/',
         approve_attestation, name='approve_attestation'),
    path('reject_attestation/<int:demande_id>/',
         reject_attestation, name='reject_attestation'),


    path("stagiaire/", stagiaire, name="stagiaire"),


    path("absence/", demande_absence, name="absence"),
    path('approve_chef/<int:pk>/', approve_chef, name='approve_chef'),
    path('reject_chef/<int:pk>/', reject_chef, name='reject_chef'),
    path('approve_rh/<int:pk>/', approve_rh, name='approve_rh'),
    path('reject_rh/<int:pk>/', reject_rh, name='reject_rh'),


    path("heuresupplementaire/", demande_hs, name="heuresupplementaire"),
    path('approve_hs/<int:demande_id>/', approve_hs, name='approve_hs'),
    path('reject_hs/<int:demande_id>/', reject_hs, name='reject_hs'),


    path("mouvement/", mouvement, name="mouvement"),
    path("evenement/", evenement, name="evenement"),
]
