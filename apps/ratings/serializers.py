from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.SerializerMethodField(read_only=True)
    agent = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Rating
        exclude = ['pkid', 'updated_at']
        
    def get_rater(self, obj):
        return obj.rater.username if obj.rater else None

    def get_agent(self, obj):
        return obj.agent.user.username if obj.agent else None