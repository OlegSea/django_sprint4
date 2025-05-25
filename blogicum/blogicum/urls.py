from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from pages import views

urlpatterns = [
    path("", include("blog.urls", namespace="blog")),
    path("pages/", include("pages.urls", namespace="pages")),
    path("admin/", admin.site.urls),
    path(
        "auth/registration/", views.RegistationCreateView.as_view(), name="registration"
    ),
    path("auth/", include("django.contrib.auth.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"
