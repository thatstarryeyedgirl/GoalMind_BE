from django.urls import path
from .views import TelexAgentAPIView, GoalAgentAPIView, CompleteStepAPIView, UserGoalsAPIView

urlpatterns = [
    path('goal/', GoalAgentAPIView.as_view(), name='goal'),
    path('agent/', TelexAgentAPIView.as_view(), name='telex_workflow'),
    path('complete/<int:step_id>/', CompleteStepAPIView.as_view(), name='complete_step'),
    path('goals/<str:user_id>/', UserGoalsAPIView.as_view(), name='user_goals'),
]