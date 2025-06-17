from rest_framework import viewsets, permissions
from .models import Candidature
from .serializers import CandidatureSerializer

class CandidatureViewSet(viewsets.ModelViewSet):
    queryset = Candidature.objects.all()  
    serializer_class = CandidatureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Candidature.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
