from rest_framework.serializers import ModelSerializer
from taskapp.models import *



# CustomUser model serializer
class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


