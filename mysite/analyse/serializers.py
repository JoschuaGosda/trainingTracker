from rest_framework import serializers
from users.models import CustomUser
from trainingdata.models import Deadhang_max, Deadhang_endurance, Pullup_max, Pullup_endurance, Training

class DeadhangMaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadhang_max
        fields = ['additional_weight','body_weight','date','crimp_size','hand_position','hands']

class DeadhangEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadhang_endurance
        fields = '__all__'

class PullupMaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pullup_max
        fields = '__all__'

class PullupEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pullup_endurance
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    deadhang_max = serializers.PrimaryKeyRelatedField(many=True, queryset=Deadhang_max.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id', 'username','deadhang_max']
