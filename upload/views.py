from django.http import JsonResponse

from rest_framework.views import APIView

from braces.views import CsrfExemptMixin

class Files(CsrfExemptMixin, APIView):
    
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files[]')
        print(files, type(files))
        
        return JsonResponse({"status": "ok"}, status=200)