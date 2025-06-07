from django.urls import path, include
from rest_framework.routers import DefaultRouter, routers
from rest_framework_nested import routers as nested_routers
from .views import ConversationViewSet, MessageViewSet, UserViewSet

# Create main router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'users', UserViewSet, basename='user')

# Create nested router for messages under conversations
conversations_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Create regular router for user endpoints
auth_router = routers.DefaultRouter()
auth_router.register(r'users', UserViewSet, basename='user')

# main urlpatterns
main_urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]

# auth urlpatterns
auth_urlpatterns = [
    path('', include(auth_router.urls)),
]
