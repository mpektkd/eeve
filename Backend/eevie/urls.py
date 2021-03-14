from eevie.models import Car
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from eevie import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views


router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')
# router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    #path('api/user/create/', views.UserViewSet.as_view(), name="create_user"),
    path('', include(router.urls)),
    path('current_user/', views.CurrentUser.as_view(), name='current_user'),
    path('login/', views.ObtainTokenPairWithUsernameView.as_view(), name='token_create'),
    path('logout/', views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='logout'),
    path('signup/', views.UserView.as_view(), name='signup'),
    path('refreshtoken/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('cars/',views.GetCars.as_view(), name='cars'),
    path('stations/', views.getStations.as_view(), name='stations'),
    path('user/monthpayoff/', views.MonthlyPayoff.as_view(), name='monthlypayoff'),
    path('user/mycars/',views.MyCars.as_view(), name='mycars'),
    path('user/mycars/chargingsession/', views.ChargingSession.as_view(),name='mychargingsession'),
    path('user/newcar/',views.InsertCar.as_view(), name='addcar'),
    path('user/mybills/', views.MyBills.as_view(), name='mybills'),
    path('user/mymonthbills/', views.MyMonthlyBills.as_view(), name='mymonthlybills'),
    path('user/deleteme/',views.DeleteMe.as_view(), name='deleteme'),
    path('admin/healthcheck/', views.HealthCheckView.as_view(), name='healthcheck'),
    path('admin/resetsessions/', views.ResetSessions.as_view(), name='resetsessions'),
    path('admin/refillsessions/', views.RefillSessions.as_view(), name='refillsessions'),
    path('admin/users/<str:username>/', views.InspectUser.as_view(), name='inspectuser'),
    path('admin/usermod/<str:username>/<str:password>/', views.UserMod.as_view(), name='usermod'),
    path('admin/system/sessionsupd/', views.SessionsUpd.as_view(), name='sessionsups'),
    re_path(r'^SessionsPerPoint/(?P<pk>\d+)/(?P<date_from>[0-9]{8})_from/(?P<date_to>[0-9]{8})_to/$', views.SessionsPerPoint, name='sessionsperpoint'),
    re_path(r'^SessionsPerStation/(?P<pk>\d+)/(?P<date_from>[0-9]{8})_from/(?P<date_to>[0-9]{8})_to/$', views.SessionsPerStation, name='sessionsperstation'),
    re_path(r'^SessionsPerEV/(?P<pk>\d+)/(?P<date_from>[0-9]{8})_from/(?P<date_to>[0-9]{8})_to/$', views.SessionsPerEV, name='sessionsperev'),
    re_path(r'^SessionsPerProvider/(?P<pk>\d+)/(?P<date_from>[0-9]{8})_from/(?P<date_to>[0-9]{8})_to/$', views.SessionsPerProvider, name='sessionsperprovider'),
    #path('users/', views.UserViewSet.as_view())/$
    # path('article/', views.ArticleList.as_view()), #URL ./article/ is will be called
    # path('detail/<int:pk>/', views.ArticleDetail.as_view()), #URL ./detail/ is will be called with a primary key (pk)
    # path('generic/article/<int:pk>/', views.GenericAPIView.as_view()), #URL ./detail/ is will be called with a primary key (pk)
]
#SessionsPerPoint/263271/20190901_from/20200803_to