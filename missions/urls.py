from django.urls import path

from . import views

urlpatterns = [
    path('', views.MissionListCreateAPIView.as_view(), name='mission-list'),
    path('<int:pk>/', views.MissionRetrieveUpdateDestroyAPIView.as_view(), name='mission-detail'),
    path('targets/<int:pk>/', views.TargetUpdateAPIView.as_view(), name='target-detail'),
]
