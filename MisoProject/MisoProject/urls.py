from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', RedirectView.as_view(url='accounts/')),  # デフォルトで/accounts/にリダイレクト
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 開発中にstaticファイルを提供する設定
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)