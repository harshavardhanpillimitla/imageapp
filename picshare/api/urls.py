from rest_framework.routers import DefaultRouter

from .views import PostViewSet, TagViewSet, ImageAPIView, ImageRotateView

from django.urls import path, include



app_name = 'photon_api'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = router.urls
urlpatterns += [
path('postimages/', ImageAPIView.as_view()),
path('rotated/', ImageRotateView.as_view()),

]