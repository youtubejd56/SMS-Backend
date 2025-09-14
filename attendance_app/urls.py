from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    admin_forgot_password,
    AttendanceViewSet,
    ShortsViewSet,
    ai_chat,
    attendance_summary,
    StudentMarkViewSet,
    clear_division_marks,
    clear_all_marks,
    EventPostViewSet,
    AdmissionView,
    AdmissionListView,
    save_attendance,
    get_attendance,
    AdminLoginView,
    AdminDashboardView
)

router = DefaultRouter()
router.register(r'marks', StudentMarkViewSet, basename='marks')
router.register(r'posts', EventPostViewSet, basename='posts')
router.register(r'shorts', ShortsViewSet, basename='shortvideo')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),

    # AI Chat
    path("ai-chat/", ai_chat, name="ai_chat"),

    # Admin Authentication
    path("admin-login/", AdminLoginView.as_view(), name="admin-login"),
    path("admin-dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("admin-forgot-password/", admin_forgot_password, name="admin-forgot-password"),

    # Admission
    path("admission/", AdmissionView.as_view(), name="admission-post"),             # POST
    path("admissions/", AdmissionListView.as_view(), name="admissions-list"),      # GET all
    path("admissiondata/", AdmissionListView.as_view(), name="admissions-alias"),  # Alias for frontend

    # Marks clear
    path("marks/clear_division/<str:division>/", clear_division_marks, name="clear-division-marks"),
    path("marks/clear_all/", clear_all_marks, name="clear-all-marks"),

    # Attendance
    path("attendance/save/", save_attendance, name="save-attendance"),
    path("attendance/list/", get_attendance, name="get-attendance"),
    path("attendance-summary/", attendance_summary, name="attendance-summary"),
]
