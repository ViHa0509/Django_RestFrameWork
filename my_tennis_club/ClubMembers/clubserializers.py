from rest_framework import serializers
from .models import Club, ClubMember
from members.models import CustomUser
class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ["id","name", "description", "location", "contact_phone"]

    def create(self, validated_data):
        club = Club(**validated_data)
        club.save()
        return club
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class JoinClubMember(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    club_id = serializers.IntegerField(required=True)
    role = serializers.ChoiceField(choices=ClubMember.ROLE_CHOICES)

class ClubMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    club_name = serializers.SerializerMethodField()
    class Meta:
        model = ClubMember
        fields = ['id', 'club', 'club_name', 'user', 'user_name', 'role']

    def get_user_name(self, instance):
        user = CustomUser.objects.get(pk=instance.user_id)
        name = f"{user.first_name} {user.last_name}"
        return name

    def get_club_name(self, instance):
        club = Club.objects.get(pk=instance.club_id)
        return club.name