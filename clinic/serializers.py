from rest_framework import serializers
from clinic.models import doctor,Appointments
import datetime
from django.utils import timezone

class doctor_serializer(serializers.ModelSerializer):
    class Meta:
        model = doctor
        fields= "__all__"
        read_only_fields=["id"]



class appointment_serializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields= "__all__"
        read_only_fields=["id"]
    def validate(self, validated_data):
        phone=validated_data.get("phone")
        appointment_date=validated_data.get("appointment_date")

        # if appointment_date < datetime.date.today():
        #     raise serializers.ValidationError("Previous Dates not allowed")

        if appointment_date < timezone.localdate():
            raise serializers.ValidationError("Invalid Date")


        if Appointments.objects.filter(
            phone = phone,appointment_date=appointment_date).exists():
            raise serializers.ValidationError("already booked")
        
        else:
            return validated_data

        
    

        