from django.urls import path
from .views import TelexAgentAPIView, GoalAgentAPIView

urlpatterns = [
    path('goal/', GoalAgentAPIView.as_view(), name='goal_agent'),
    path('agent/', TelexAgentAPIView.as_view(), name='telex_workflow'),
]