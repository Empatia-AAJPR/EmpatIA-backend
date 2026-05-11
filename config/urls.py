from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from apps.Accounts.api.views import router as accounts_router
from apps.Accounts.api.views import auth_router

api = NinjaAPI(
    title='EmpatIA',
    docs_url='/docs/'
)


@api.get('/health', tags=['Health'])
def check_health(request):
    return {'message': 'OK'}


api.add_router('/accounts', accounts_router, tags=['Accounts'])
api.add_router('/auth', auth_router, tags=['Auth'])


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls)
]
