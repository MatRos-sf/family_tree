from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tree/<int:person_id>/', views.view_family_tree, name='tree'),
    path('check/', views.check_oldest_ancestor, name='check'),
    path('search/', views.SearchResultView.as_view() , name='search_results'),


    # CRUD
    path('create/', views.CreatePersonView.as_view(), name='create'),
    path('detail/<int:pk>/', views.DetailPersonView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.DeletePersonView.as_view(), name='delete'),
    path('update/<int:pk>/', views.UpdatePersonView.as_view(), name='update'),
]
