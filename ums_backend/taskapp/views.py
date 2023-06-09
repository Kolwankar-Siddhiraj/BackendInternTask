from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction

from datetime import datetime
from taskapp.models import Task
from taskapp.serializer import TaskSerializer


# support functions

def formatDate(sdate=None):

    if sdate == None:
        return sdate

    return datetime.strptime(sdate, "%Y-%m-%d").date()



# views

class TaskView(APIView):

    permission_classes = []
    authentication_classes = []


    @transaction.atomic
    def get(self, request, tid):

        data = None
        if tid == "all":
            task_obj = Task.objects.filter().order_by('id')
            data = TaskSerializer(task_obj, many=True).data

        else:
            task_obj = Task.objects.filter(id=tid).first()
            data = TaskSerializer(task_obj).data

        return Response({"success": True, "message": "New Task Added !", "data": data}, status=status.HTTP_200_OK)


    @transaction.atomic
    def post(self, request, action):

        rd = request.data
        print("rd :: ", rd)

        if action not in ["add", "update", "delete"]:
            return Response({"success": False, "message": "Something went wrong !"}, status=status.HTTP_404_NOT_FOUND)

        elif action == "add":
            data = None

            new_task = Task.objects.create(title=rd['title'], description=rd['description'], due_date=formatDate(rd['due_date']))
            data = TaskSerializer(new_task).data
            return Response({"success": True, "message": "New Task Added !", "data": data}, status=status.HTTP_200_OK)

        elif action == "update":
            task_obj = Task.objects.filter(id=rd['id']).first()
            if task_obj is not None:
                updated_task = TaskSerializer(instance=task_obj, data=rd)
                if updated_task.is_valid():
                    updated_task.save()
                    return Response({"success": True, "message": "New Task Added !", "data": updated_task.data}, status=status.HTTP_200_OK)

        elif action == "delete":
            task_obj = Task.objects.filter(id=rd['id']).first()
            if task_obj is not None:
                task_obj.delete()
                return Response({"success": True, "message": "New Task Added !", "data": data}, status=status.HTTP_200_OK)


