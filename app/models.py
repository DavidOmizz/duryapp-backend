
# your_app/models.py
from django.db import models
from django.core.files.storage import default_storage
import logging
from django_bunny_storage.storage import BunnyStorage
import logging
from django.db.models.signals import post_save # Import for signal
from django.dispatch import receiver # Import for signal


class Category(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # The 'videos/' part will be a folder inside your Bunny Storage Zone
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', related_name='videos', on_delete=models.CASCADE)
    video_url = models.URLField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # FORCE BunnyStorage only when file is being updated
        if self.video_file and not isinstance(self.video_file.storage, BunnyStorage):
            self.video_file.storage = BunnyStorage()
            logging.warning(f'Forced BunnyStorage at save time: {self.video_file.storage.__class__}')
        super().save(*args, **kwargs)

    
    # Signal to populate video_url after the video_file is saved to storage
@receiver(post_save, sender=Video)
def update_video_url(sender, instance, created, **kwargs):
    # This signal runs after a Video instance is saved.
    # We only want to set the URL if the instance was just created AND
    # if a video_file was actually uploaded/assigned.
    # Also, we check if video_url is already set to prevent re-setting if it's manually changed.
    if created and instance.video_file and not instance.video_url:
        # instance.video_file.url dynamically gets the URL from the configured storage backend
        # (which should be BunnyStorage if your settings were correctly applied).
        instance.video_url = instance.video_file.url
        # Save the instance again, but ONLY update the video_url field
        # to prevent infinite recursion on the save method.
        instance.save(update_fields=['video_url'])