from django.urls import path, include

from . import views

urlpatterns = [

    path('tree/<int:person_id>/', views.view_family_tree, name='tree'),
]
