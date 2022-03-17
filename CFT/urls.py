from django.contrib import admin
from django.urls import path, include
from notes.views import index, add_note, edit, delete, registration
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('add_note/', add_note, name='add_note'),
    path('note/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('registration/', registration, name='registration'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
