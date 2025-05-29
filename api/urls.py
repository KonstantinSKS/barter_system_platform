from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdViewSet, CategoryViewSet, ExchangeProposalViewSet,
                    LoginView, LogoutView, MeView, RegistrationView)

app_name = 'api'


router_v1 = DefaultRouter()

router_v1.register('ads', AdViewSet, basename='ads')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('proposals', ExchangeProposalViewSet, basename='proposals')

urlpatterns = [
    path('', include(router_v1.urls)),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
