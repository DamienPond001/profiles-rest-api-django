from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles_api import serializers


class HelloAPIView(APIView):
    """Test APIView"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features
        request: object of rest framework containing details of request beng made to API
        format: adds a format suffix the the endpoint url
        
        """

        an_apiview = [
            'Uses HTTP methods as function',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLS'
        ]

        return Response({'message': 'Hello', 'an_apiview' : an_apiview})

    def post(self, request):
        """Create a hello messaage with our name"""

        #serializer_class() function comes with APIView that configures the serializer_class object for our view
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = 'Hello {}'.format(name)

            return Response({'message': message})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        """Handle updating an object"""

        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of object"""

        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""

        return Response({'method': 'DELETE'})