from rest_framework import routers
from .api import ProjectViewSet
router = routers.DefaultRouter()

router.register('api/projects', ProjectViewSet, 'prpjects')

urlpatterns = router.urls



#models -> serializers -> api.py -> urls.py