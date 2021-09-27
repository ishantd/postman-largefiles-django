from django.http import JsonResponse

from rest_framework.views import APIView

from upload.utils import the_file_is_csv
from data.utils import modify_db_status, start_csv_processing, start_db_action, start_thread_process, time_this_function

from upload.models import FileItem
from braces.views import CsrfExemptMixin

import timeit

class Files(CsrfExemptMixin, APIView):
    
    def get(self, request, *args, **kwargs):
        files = list(FileItem.objects.all().values())
        return JsonResponse({"status": "ok", "files": files}, status=200)
    
    def post(self, request, *args, **kwargs):
        start, stop = None, None
        db_action = start_db_action("Product File Upload", "In Progress")
        start = timeit.default_timer()
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
                    db_action = modify_db_status(db_action.id, "Completed")
                stop = timeit.default_timer()
        if start and stop:
            time_this_function(start, stop, db_action.id)
        return JsonResponse({"status": "ok"}, status=200)
    
    def put(self, request, *args, **kwargs):
        start_csv_processing()
        return JsonResponse({"status": "ok"}, status=200)