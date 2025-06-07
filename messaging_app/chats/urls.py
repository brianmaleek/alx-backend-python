from django.urls import path, include
from rest_framework.routers import DefaultRouter, routers
from .views import ConversationViewSet, MessageViewSet, UserViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserViewSet, basename='user')

# Create regular router for user endpoints
auth_router = routers.DefaultRouter()
auth_router.register(r'users', UserViewSet, basename='user')

# main urlpatterns
main_urlpatterns = [
    path('', include(router.urls)),
]

# auth urlpatterns
auth_urlpatterns = [
    path('', include(auth_router.urls)),
]
