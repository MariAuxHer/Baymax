from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login, logout

from django.middleware.csrf import get_token

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
# authentication
class csrfView(APIView):
    permission_classes = [AllowAny]
    
    @staticmethod
    def get(request):
        response = Response({'detail': 'CSRF cookie set'})
        response['X-CSRFToken'] = get_token(request)
        return response 

class LogoutView(APIView):
    permission_classes = [AllowAny]
    
    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response({'detail': 'You\'re not logged in.'}, status=400)

        logout(request)
        return Response({'detail': 'Successfully logged out.'})

class LoginView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        username = request.data['username']
        password = request.data['password']

        if username is None or password is None:
            return Response({'detail': 'Please provide username and password.'}, status=400)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'detail': 'Invalid credentials.'}, status=400)

        login(request, user)
        return Response({'detail': 'Successfully logged in.'})
    
class SessionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return Response({'isAuthenticated': True})


class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return Response({'username': request.user.username})