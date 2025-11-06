from .models import GoalSteps, Goals, TelexAgent
import random
from .serializers import GoalSerializer, TelexAgentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


def generate_steps(message):
    topic = message.lower()
    if "learn" in topic:
        topic = topic.split("learn")[-1].strip()
    elif "want to" in topic:
        topic = topic.split("want to")[-1].strip()
    else:
        topic = message
    ideas = [
        f"Research and understand the basics of {topic}.",
        f"Get all the materials you need for {topic}.",
        f"Watch YouTube videos or read guides about {topic}.",
        f"Practice {topic} for at least 30 minutes daily.",
        f"Ask a friend or mentor to review your progress in {topic}.",
        f"Join a community or group that focuses on {topic}.",
        f"Try creating a small project related to {topic}.",
        f"Track your progress weekly and note what you’ve learned about {topic}.",
    ]
    random.shuffle(ideas)
    return ideas[:5]


def random_position():
    return [random.randint(100, 1000), random.randint(100, 600)]

class TelexAgentAPIView(APIView):
    def get(self, request):
        agent, _ = TelexAgent.objects.get_or_create(
            agent_id="goal_agent_001",
            defaults={
                "name": "goal_mind",
                "active": True,
                "category": "productivity",
                "description": "A goal assistant that helps users create and track goals.",
                "short_description": "Breaks goals into actionable steps",
                "long_description": "I am a helpful goal-setting assistant. My primary function is to help users set and track personal goals by breaking them into achievable steps. Always respond with encouragement and clarity."
            }
        )
        serializer = TelexAgentSerializer(agent)
        node_position = random_position()
        workflow_json = {
            "active": agent.active,
            "category": agent.category,
            "description": agent.description,
            "id": agent.agent_id,
            "long_description": agent.long_description,
            "name": agent.name,
            "nodes": [
                {
                    "id": "goal_node",
                    "name": "Goal Agent",
                    "parameters": {},
                    "position": node_position,
                    "type": "a2a/mastra-a2a-node",
                    "typeVersion": 1,
                    "url": "http://127.0.0.1:8000/a2a/agent/goal"
                }
            ],
            "pinData": {},
            "settings": {"executionOrder": "v1"},
            "short_description": agent.short_description
        }
        return Response({"agent": serializer.data, "workflow": workflow_json}, status=status.HTTP_200_OK)
    
    
class GoalAgentAPIView(APIView):
    def post(self, request):
        # Handle A2A protocol format
        data = request.data
        
        # Extract message from A2A format
        if 'input' in data and 'message' in data['input']:
            message = data['input']['message']
            user_id = data.get('userId', 'anonymous')
        else:
            # Fallback for direct API calls
            user_id = data.get("user_id", "anonymous")
            message = data.get("message")

        if not message:
            return Response({
                "type": "message",
                "text": "Please provide a goal you'd like to work on!"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if user is completing a step
        if "completed step" in message.lower() or "done with step" in message.lower():
            words = message.lower().split()
            step_number = None
            for i, word in enumerate(words):
                if word == "step" and i + 1 < len(words) and words[i + 1].isdigit():
                    step_number = int(words[i + 1])
                    break
            
            if step_number:
                user_goal = Goals.objects.filter(telex_user_id=user_id).last()
                if user_goal:
                    step = user_goal.steps.filter(order=step_number).first()
                    if step:
                        step.is_completed = True
                        step.save()
                        user_goal.completed_steps = user_goal.steps.filter(is_completed=True).count()
                        user_goal.save()
                        return Response({
                            "type": "message",
                            "text": f" Step {step_number} completed! Progress: {user_goal.progress()}%"
                        })
            user_goal = Goals.objects.filter(telex_user_id=user_id).last()
            if user_goal:
                return Response({
                    "type": "message",
                    "text": f"Say 'completed step 1' for your goal: '{user_goal.goal_title}'"
                })
            return Response({
                "type": "message",
                "text": "You don't have any active goals yet!"
            })

        # Check for existing goal to prevent duplicates
        existing_goal = Goals.objects.filter(
            telex_user_id=user_id,
            goal_title=message
        ).first()
        
        if existing_goal:
            serializer = GoalSerializer(existing_goal)
            existing_steps = list(existing_goal.steps.values_list('step_title', flat=True))
            steps_list = [f"{i+1}. {step}" for i, step in enumerate(existing_steps)]
            
            return Response({
                "type": "message",
                "text": f"You already have this goal! Here are your steps for '{existing_goal.goal_title}':",
                "steps": steps_list,
                "footer": "Keep working on these steps!",
                "goal": serializer.data
            }, status=status.HTTP_200_OK)

        steps = generate_steps(message)
        agent = TelexAgent.objects.filter(agent_id="goal_agent_001").first()

        # Extract topic for description
        topic = message.lower()
        if "learn" in topic:
            topic = topic.split("learn")[-1].strip()
        elif "want to" in topic:
            topic = topic.split("want to")[-1].strip()
        else:
            topic = message
            
        goal = Goals.objects.create(
            telex_user_id=user_id,
            goal_title=message,
            goal_description=f"Goal created to help with {topic}",
            total_steps=len(steps),
            agent=agent
        )
        
        for order, step in enumerate(steps, start=1):
            GoalSteps.objects.create(goal=goal, step_title=step, order=order)
            
        serializer = GoalSerializer(goal)
        created_steps = goal.steps.all().order_by('order')
        steps_list = [f"{i+1}. {step.step_title}" for i, step in enumerate(created_steps)]
        
        return Response({
            "type": "message",
            "text": f"Great! I've broken down your goal '{goal.goal_title}' into actionable steps:",
            "steps": steps_list,
            "footer": "You can start with step 1 and work your way through. Good luck!",
            "goal": serializer.data
        }, status=status.HTTP_200_OK)


class CompleteStepAPIView(APIView):
    def post(self, request, step_id):
        try:
            step = GoalSteps.objects.get(id=step_id)
            step.is_completed = True
            step.save()
            
            goal = step.goal
            goal.completed_steps = goal.steps.filter(is_completed=True).count()
            goal.save()
            
            return Response({
                "type": "message",
                "text": f"Step completed! Progress: {goal.progress()}%"
            })
        except GoalSteps.DoesNotExist:
            return Response({"error": "Step not found"}, status=404)


class UserGoalsAPIView(APIView):
    def get(self, request, user_id):
        goals = Goals.objects.filter(telex_user_id=user_id)
        result = []
        for goal in goals:
            steps = [{"id": step.id, "title": step.step_title, "order": step.order, "completed": step.is_completed} 
                    for step in goal.steps.all().order_by('order')]
            result.append({
                "goal_id": goal.id,
                "title": goal.goal_title,
                "progress": goal.progress(),
                "steps": steps
            })
        return Response(result)


class AllUsersAPIView(APIView):
    def get(self, request):
        users = Goals.objects.values_list('telex_user_id', flat=True).distinct()
        return Response(list(users))

