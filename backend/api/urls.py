from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ResumeListCreateView, ResumeDetailView
from uuid import UUID

urlpatterns = [
    path('resumes/', ResumeListCreateView.as_view(), name='resume-list-create'),
    path('resumes/<uuid:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
]

# # Serve media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)