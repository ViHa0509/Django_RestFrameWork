from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .clubserializers import ClubSerializer, ClubMemberSerializer, JoinClubMember
from members.serializers import CustomUserSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Club, ClubMember
from members.models import CustomUser

# Create your views here.
class ClubViewSet(viewsets.ModelViewSet):
    serializer_class = ClubSerializer
    authenticate = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Club.objects.all()

    @action(detail=False, methods=['get'], url_path='all')
    def get_club(self, request):
        queryset = Club.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='new-club')
    def create_club(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='<pk>')
    def update_club(self, request, pk=None):
        queryset = self.get_queryset()
        club = queryset.filter(pk=pk).first()
        if club:
            serializer = self.serializer_class(club, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='all-member')
    def member_group(self, request, pk):
        user_detail = request.query_params.get('user-detail', 'false').lower() == 'true'
        print(f"USER DETAIL PARAM: {user_detail}")
        club_member = ClubMember.objects.filter(club_id=pk)
        if user_detail:
            user_ids = club_member.values_list('user_id', flat=True)
            print(f"User-ids: {user_ids}")
            users = CustomUser.objects.filter(pk__in=user_ids)
            UserSerializer = CustomUserSerializer(users, many=True)
            return Response(UserSerializer.data, status=status.HTTP_200_OK)
        else:
            serializer = ClubMemberSerializer(club_member, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, method=['get'], url_path='all-member-details')
    # def list_club_members(self, request, pk):
    #     queryset = ClubMember.objects.filter(id=pk)
    #     print(queryset)

    #     return Response(status=status.HTTP_400_BAD_REQUEST)    

class ClubMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ClubMemberSerializer
    queryset = ClubMember.objects.all()
    authenticate = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='new-member')
    def add_member(self, request):
        serializer = JoinClubMember(data=request.data)
        if serializer.is_valid():
            user_id = request.data['user_id']
            club_id = request.data['club_id']
            role = request.data['role']
            try:
                user = CustomUser.objects.get(pk=user_id)
                club = Club.objects.get(pk=club_id)
            except user.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except club.DoesNotExist:
                return Response({'error': 'Club does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            if ClubMember.objects.filter(user=user, club=club).exists():
                return Response({"error": "User is already a member of the club"}, status=status.HTTP_400_BAD_REQUEST)
                
            club_member = ClubMember.objects.create(user=user, club=club, role=role)
            member_serializer=self.serializer_class(club_member)
            return Response(member_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    