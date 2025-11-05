from rest_framework import serializers
from .models import Goals, GoalSteps, TelexAgent

class GoalStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalSteps
        fields = ['step_title', 'is_completed', 'order']
        
        
class GoalSerializer(serializers.ModelSerializer):
    steps = GoalStepsSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Goals
        fields = ['telex_user_id', 'goal_title', 'goal_description', 'total_steps', 'completed_steps', 'progress', 'created_at', 'updated_at', 'steps']
        read_only_fields = ['telex_user_id', 'created_at', 'updated_at', 'steps']
        
    def get_progress(self, obj):
        return obj.progress()
    
    
class TelexAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelexAgent
        fields = ['agent_id', 'name', 'description', 'short_description', 'long_description', 'category', 'active']
        

    