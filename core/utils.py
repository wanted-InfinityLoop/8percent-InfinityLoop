import jwt
import json

from django.http     import JsonResponse
from users.models    import User
from my_settings     import MY_SECRET_KEY
from core.validation import algorithm

def LoginDecorator(func):
      
      def wrapper(self, request, *arg, **kwargs):
          try:
              auth_header = request.headers.get("Authorization", None)
              
              if not auth_header:
                  return JsonResponse({'message' : 'NOT_ACCESS_TOKEN'}, status=400)
              
              if not auth_header.startswith("Bearer "):
                  return JsonResponse({"message" : "AUTH_ERROR"}, status=401)
              
              encoded_token = auth_header.split(" ")[1]
              data          = jwt.decode(encoded_token, MY_SECRET_KEY, algorithm)    
              user          = User.objects.get(id=data['user_id'])
              request.user  = user
              
          except jwt.DecodeError:
              return JsonResponse({'message' : 'INVALID_TOKEN'}, status=400)
          
          except User.DoesNotExist:
              return JsonResponse({'message' : 'INVALID_USER'}, status=400)
          
          return func(self, request, *arg, **kwargs)
      
      return wrapper
