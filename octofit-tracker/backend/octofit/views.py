from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, LeaderboardSerializer, WorkoutSerializer
from .models import User, Team, Activity, Leaderboard, Workout

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

@api_view(['GET'])
def api_root(request, format=None):
    # Get the codespace URL or use localhost in debug mode
    codespace_url = 'https://shiny-funicular-8000.app.github.dev/'
    if settings.DEBUG:
        base_url = request.build_absolute_uri('/')[:-1]  # Dynamically get the base URL
    else:
        base_url = codespace_url
    
    # Add the API endpoint suffix
    api_url = f"{base_url}/api"
    
    return Response({
        'users': f"{api_url}/users/",
        'teams': f"{api_url}/teams/",
        'activities': f"{api_url}/activities/",
        'leaderboard': f"{api_url}/leaderboard/",
        'workouts': f"{api_url}/workouts/",
    })