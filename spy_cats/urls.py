from django.urls import path

from . import views

urlpatterns = [
    path('', views.SpyCatListCreateAPIView.as_view(), name='list-spy-cats'),
    path('<int:pk>/', views.SpyCatRetrieveUpdateDestroyAPIView.as_view(), name='spy-cat-detail'),
]
