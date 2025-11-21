from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile 
from .serializers import UserProfileSerializer
from rest_framework import status

class UserProfileAPI(APIView):
    def get(self,request):
        users = UserProfile.objects.all()
      
        # search
        search = request.GET.get("search")
        if search:
         users = users.filter(name__icontains=search)

         # Order By 
         order_by = request.GET.get("order_by")
         if order_by:
             users = users.order_by(order_by)

        #pagination
        page = request.GET.get("page",1)
        page_size = request.GET.get("page_size",10)
        try:
            page = int(page)
            page_size = int(page_size)
        except:
            return Response({"message":"page not found"},status=404)

        start = (page-1) * page_size
        end = start + page_size
        total_count = users.count()            
        serializer = UserProfileSerializer(users[start:end], many=True)
        return Response({
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "serializer" : serializer.data
        })
    
    def post(self,request):
        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)
        


from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileAPIView(APIView):

    
    def get_object(self,pk):
        try:
           return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return None
        
    # data get
    def get(self,request,pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"message": "User not found"},status = status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    # data update
    def put(self,request,pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"message","User not found"},status = status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response("Error","Does not found",status= status.HTTP_400_BAD_REQUEST)
    
    #patch is use partial update
    def patch(self,request,pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"Error","User not found"},status = status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user, data = request.data, partial = True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"Error":"User not found"},status = status.HTTP_400_BAD_REQUEST)
    
    # Delete data 
    def delete(self,request,pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"Message":"User not found"},status = status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "User deleted successfully"},status= status.HTTP_400_BAD_REQUEST)
    