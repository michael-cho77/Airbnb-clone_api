from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


#자동으로 만드는 과정
class ReadRoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


# 수동으로 만드는 과정
class WriteRoomSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)


    #반드시 instance(이 경우는 Room)를 return해야함
    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    # 항상 data를 return해주어야함 
    def validate(self, data):
        # instance가 있으면 update 없으면 create check_in의경우 create, update 경우의수를 모두 고려
        if self.instance:
            #get()은 파이썬 고유 메소드 {}로 check_in key가 있다면 그 값을 가져옴, 값이 없다면 self.instance.check_in를 default로 함
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
        return data


    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.price = validated_data.get("price", instance.price)
        instance.beds = validated_data.get("beds", instance.beds)
        instance.lat = validated_data.get("lat", instance.lat)
        instance.lng = validated_data.get("lng", instance.lng)
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
        instance.check_in = validated_data.get("check_in", instance.check_in)
        instance.check_out = validated_data.get("check_out", instance.check_out)
        instance.instant_book = validated_data.get(
            "instant_book", instance.instant_book
        )
        instance.save()
        return instance