from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from clinic.models import doctor,Appointments
from clinic.serializers import doctor_serializer,appointment_serializer
from datetime import time,datetime,timedelta

# Create your views here.
class DoctorListCreateView(APIView):
    def get(self,request):
        qs=doctor.objects.all()
        serializer_instance=doctor_serializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        from_data=request.data
        serializer_instance=doctor_serializer(data=from_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class DoctorRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        data = get_object_or_404(doctor, id=pk)
        serializer_instance = doctor_serializer(data)
        return Response(data=serializer_instance.data)

    def put(self,request,pk):
        form_data=request.data
        doctor_object=get_object_or_404(doctor,id=pk)
        serializer_instance=doctor_serializer(data=form_data,instance=doctor_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk):
        doctor_obj=get_object_or_404(doctor,id=pk)
        doctor_obj.delete()
        return Response(data={"Message":"Deleted...!"})

class AppointmentListCreateView(APIView):
    def get(self,request):
        qs=Appointments.objects.all()
        serializer_instance=appointment_serializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=appointment_serializer(data=form_data)
        if serializer_instance.is_valid():
            appointment_date=serializer_instance.validated_data.get('appointment_date')
            doctor_id=serializer_instance.validated_data.get('doctor_id')

            last_appointment=Appointments.objects.filter(
                appointment_date=appointment_date,
                doctor_id=doctor_id
            ).order_by("-token_number").first()

            if last_appointment is None:
                form_data["token_number"] = 1
                form_data["appointment_time"] = time(10,0)

            else:
                form_data["token_number"]=last_appointment.token_number + 1
                current_time=datetime.combine(appointment_date,last_appointment.appointment_time)
                next_time=current_time+timedelta(minutes=15)

                if next_time.time()==time(10,30):
                    next_time= datetime.combine(appointment_date,time(13,30))

                if next_time.time()>=time(17,0):
                    return Response(data={
                                    "message":"Todays Booking Ended.....!",
                    })

                form_data["appointment_time"]=next_time

            qs=Appointments.objects.create(**form_data)
            serializer_instance=appointment_serializer(qs)
            return Response(data={
                "message":"Booked sucessfully",
                "token number is":form_data["token_number"]
            })
        else:
            return Response(data=serializer_instance.errors)

