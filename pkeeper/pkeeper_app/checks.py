from .models import *
from django.http import HttpResponse, JsonResponse

def temp_del(request):
	obj1=Reg_Requests.objects.all().delete()
	obj2=Hospital.objects.all().delete()
	obj3=Records.objects.all().delete()

	return HttpResponse("<script>alert('Data Deleted Successfully');window.location.href='/show_home_admin/'</script>")