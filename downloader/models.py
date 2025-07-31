from django.db import models

# Create your models here.
class DownloadHistory(models.Model):
    PLATFORM_CHOICES = (
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
    )

    video_url = models.URLField()
    platform = models.CharField(max_length = 566, choices=PLATFORM_CHOICES)
    resolution = models.CharField(max_length=30)
    ip_address = models.GenericIPAddressField()
    download_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} - {self.video_url[:30]}..."