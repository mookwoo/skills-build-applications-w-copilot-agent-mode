from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return ObjectId(data)

class UserSerializer(serializers.ModelSerializer):
    _id = ObjectIdField()
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Password hashing now happens in the model's save method
        return User.objects.create(**validated_data)

class TeamSerializer(serializers.ModelSerializer):
    _id = ObjectIdField()
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Team
        fields = '__all__'
    
    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        team = Team.objects.create(**validated_data)
        
        # Add members to the team
        for member_id in member_ids:
            try:
                user = User.objects.get(_id=ObjectId(member_id))
                team.members.add(user)
            except User.DoesNotExist:
                pass
        
        return team
    
    def update(self, instance, validated_data):
        member_ids = validated_data.pop('member_ids', None)
        
        # Update basic team info
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update members if provided
        if member_ids is not None:
            instance.members.clear()
            for member_id in member_ids:
                try:
                    user = User.objects.get(_id=ObjectId(member_id))
                    instance.members.add(user)
                except User.DoesNotExist:
                    pass
        
        instance.save()
        return instance

class ActivitySerializer(serializers.ModelSerializer):
    _id = ObjectIdField()
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Activity
        fields = '__all__'
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        try:
            user = User.objects.get(_id=ObjectId(user_id))
            return Activity.objects.create(user=user, **validated_data)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

class LeaderboardSerializer(serializers.ModelSerializer):
    _id = ObjectIdField()
    user = UserSerializer()  # Expand the user object
    user_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Leaderboard
        fields = '__all__'
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        try:
            user = User.objects.get(_id=ObjectId(user_id))
            return Leaderboard.objects.create(user=user, **validated_data)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

class WorkoutSerializer(serializers.ModelSerializer):
    _id = ObjectIdField()

    class Meta:
        model = Workout
        fields = '__all__'