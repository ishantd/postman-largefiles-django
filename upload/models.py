from django.db import models

class FileItem(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    path = models.TextField(blank=True, null=True)
    size = models.BigIntegerField(default=0)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    processed = models.BooleanField(default=False)
    processing_time = models.CharField(max_length=120, null=True, blank=True)

    @property
    def title(self):
        return str(self.name)