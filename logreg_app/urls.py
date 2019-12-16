from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('users/register', views.register),
    path('users/success', views.success),
    path('users/login', views.login),
    path('users/logout', views.logout),

    path('users/new_job', views.new_job),
    path('users/add_job', views.add_job),
    path('users/cancel', views.cancel),
    path('users/<int:job_id>/remove_job', views.remove_job),
    path('users/<int:job_id>/view_job', views.view_job),
    path('users/<int:job_id>/edit_job', views.edit_job),
    path('users/<int:job_id>/update', views.update),
]