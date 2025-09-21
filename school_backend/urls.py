from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse

# Simple root view to avoid 404 at "/"
def root_view(request):
    return JsonResponse({"message": "Backend is running"})

urlpatterns = [
    # Root URL
    path("", root_view, name="root"),

    # Django admin panel
    path("admin/", admin.site.urls),

    # All API routes from attendance_app (marks, attendance, admissions, posts, admin login/dashboard)
    path("api/", include("attendance_app.urls")),

    # JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
