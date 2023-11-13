from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login, logout
from rest_framework import status

from django.middleware.csrf import get_token

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
# authentication

class CSRF(APIView):

    """
    In the CSRF class, the get method creates and sends a csrftoken to the client by calling 
    get_token(request). This token is then added to the HTTP response header as X-CSRFToken.
    
    The CSRF view responds to a GET request by generating a CSRF token using Django's get_token method.
    """
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, format=None):
        response = Response({'detail': 'CSRF cookie set'})
        response['X-CSRFToken'] = get_token(request)
        # response['Access-Control-Allow-Origin'] = '*'
        return response
    
    def post(request, format=None):
        return Response({'detail': 'There is no POST here.'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']

        if username is None or password is None:
            return Response({'detail': 'Please provide username and password.'}, status = status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'detail': 'Invalid credentials.'}, status = status.HTTP_401_UNAUTHORIZED)
        
        """ 
        When a user logs in successfully, the login(request, user) call in the LoginView class will initiate a session for the user. 
        Django's SessionMiddleware automatically manages the sessionid cookie, which is sent back to the client in the HTTP response.
        """
        login(request, user)
        return Response({'detail': 'Successfully logged in.'}, status = status.HTTP_200_OK)
    
    def get(self, request, format=None):
        return Response({'detail': 'There is no GET here.'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, format = None):
        # Handle when not logged in
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'You\'re not logged in.'}, status = status.HTTP_200_OK)
        
        # Handle when logged in
        logout(request)
        return JsonResponse({'detail': 'Successfully logged out.'}, status = status.HTTP_200_OK)
    
    def post (self, request, format=None):
         return Response({'detail': 'There is no POST here.'}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
class SessionView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, format=None):
        if request.user.is_authenticated:
            return Response({'isAuthenticated': True}, status = status.HTTP_200_OK)
        else:
            return Response({'isAuthenticated': False}, status = status.HTTP_200_OK)


class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return Response({ request.user })