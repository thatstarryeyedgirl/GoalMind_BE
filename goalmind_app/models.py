from django.db import models

# Create your models here.

class Goals(models.Model):
    telex_user_id = models.CharField(max_length=100, db_index=True)
    goal_title = models.CharField(max_length=150)
    goal_description = models.TextField()
    total_steps = models.IntegerField(default=0)
    completed_steps = models.IntegerField(default=0)
    agent = models.ForeignKey('TelexAgent', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def progress(self):
        if self.total_steps == 0:
            return 0
        return round((self.completed_steps / self.total_steps) * 100, 2)
    
    def __str__(self):
        return f"{self.goal_title} ({self.telex_user_id})"
    
    
class GoalSteps(models.Model):
    goal = models.ForeignKey(Goals, related_name='steps', on_delete=models.CASCADE)
    step_title = models.CharField(max_length=150)
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.step_title} - {'Completed' if self.is_completed else 'Pending'}"
    
    
class TelexAgent(models.Model):
    name = models.CharField(max_length=100, default="goal_mind")
    agent_id = models.CharField(max_length=50, unique=True, default="goal_agent_001")
    description = models.TextField(default="A goal assistant that helps users create and track goals.")
    category = models.CharField(max_length=50, default="productivity")
    active = models.BooleanField(default=False)
    short_description = models.CharField(max_length=150, default="Breaks goals into actionable steps")
    long_description = models.TextField(default="I am a helpful goal-setting assistant. My primary function is to help users set and track personal goals by breaking them into achievable steps. Always respond with encouragement and clarity.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({'Active' if self.active else 'Inactive'})"   
     
    
    