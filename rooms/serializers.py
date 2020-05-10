from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room


#자동으로 만드는 과정
class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


class WriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ("user", "modified", "created")

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
        return data