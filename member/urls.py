from django.urls import path, include

from . import views

urlpatterns = [

    path('tree/<int:person_id>/', views.view_family_tree, name='tree'),
    path('check/', views.check_oldest_ancestor, name='check'),

    # CRUD
    path('create/', views.CreatePersonView.as_view(), name='create'),
    path('detail/<int:pk>/', views.DetailPersonView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.DetailPersonView.as_view(), name='delete')

]
