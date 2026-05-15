from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from apps.Accounts.api.views import router as accounts_router
from apps.Accounts.api.views import auth_router

from apps.Users.api.views import (
    router_student,
    router_coordinator,
    router_director,
)

api = NinjaAPI(title='EmpatIA', docs_url='/docs/')


@api.get('/health', tags=['Health'])
def check_health(request):
    return {'message': 'OK'}


api.add_router('/accounts', accounts_router, tags=['Accounts'])
api.add_router('/auth', auth_router, tags=['Auth'])

api.add_router('/student', router_student, tags=['Students'])

api.add_router('/coordinator', router_coordinator, tags=['Coordinator'])

api.add_router('/director', router_director, tags=['Director'])


urlpatterns = [path('admin/', admin.site.urls), path('api/v1/', api.urls)]
