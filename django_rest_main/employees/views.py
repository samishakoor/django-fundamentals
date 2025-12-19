from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status, mixins, generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import EmployeeSerializer
from api.paginations import CustomPagination
from employees.models import Employee


# Create your class based views here.
class EmployeeList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        employees = Employee.objects.all()
        # Instantiate your custom paginator (in class based views(using with APIView), we can't directly implement custom pagination like in generics/mixins/ModalViewSets etc.)
        paginator = CustomPagination()
        # Paginate the queryset
        page = paginator.paginate_queryset(employees, request, view=self)
        # Return paginated response
        serializer = EmployeeSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(APIView):
    permission_classes = [AllowAny]

    def findEmployeeById(self, id):
        try:
            return Employee.objects.get(pk=id)
        except Employee.DoesNotExist:
            raise Http404("Employee not found")

    def get(self, request, id):
        employee = self.findEmployeeById(id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        employee = self.findEmployeeById(id)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        employee = self.findEmployeeById(id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Mixins
"""
class EmployeeList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)



class EmployeeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id)
    
    def put(self, request, id):
        return self.update(request, id)
    
    def delete(self, request, id):
        return self.destroy(request, id)
"""

# Generics
"""
class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'
"""

# Viewsets
"""
class EmployeeViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        # Instantiate your custom paginator (in class based views(using with viewsets.ViewSet), we can't directly implement custom pagination like in generics/mixins/ModalViewSets etc.)
        paginator = CustomPagination()
        # Paginate the queryset
        page = paginator.paginate_queryset(queryset, request, view=self)
        # Serialize paginated data
        serializer = EmployeeSerializer(page, many=True)
        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
    
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        
"""


# ModelViewSet
class EmployeeViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["emp_name", "designation"]
    ordering_fields = ["id", "emp_name"]
