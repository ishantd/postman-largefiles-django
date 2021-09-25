from django.urls import path

from upload import views

app_name = 'upload'

urlpatterns = [
    path('files/',  views.NewUpload.as_view(), name='files'),
]