from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views


app_name = "books"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name="landing_page"),
    path('home/', views.HomePageView.as_view(), name="home_page"),
    path('users/', include("auusers.urls")),
    path('books/', include("books.urls")),


    path('api/', include("api.urls")),  # api app
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
