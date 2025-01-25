from ninja import NinjaAPI
from ninja.security import django_auth

api = NinjaAPI()

@api.get("/",auth=django_auth)
def hello(request):
    return "Hello world"