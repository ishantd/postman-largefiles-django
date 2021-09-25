from django.http import JsonResponse

from rest_framework.views import APIView

from upload.utils import the_file_is_csv
from data.utils import start_csv_processing, start_thread_process

from upload.models import FileItem
from braces.views import CsrfExemptMixin

import threading

class Files(CsrfExemptMixin, APIView):
    
    def get(self, request, *args, **kwargs):
        files = list(FileItem.objects.all().values())
        return JsonResponse({"status": "ok", "files": files}, status=200)
    
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files[]')
        for file in files:
            if the_file_is_csv(file.name):
                f, file_uploaded = FileItem.objects.get_or_create(
                    name=file.name,
                    file=file,
                    file_type='csv'
                )
                if file_uploaded:
                    f.uploaded = True
                    f.save()
        start_thread_process(start_csv_processing)
        return JsonResponse({"status": "ok"}, status=200)