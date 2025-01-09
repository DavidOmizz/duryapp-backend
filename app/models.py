from django.db import models
import cloudinary
import cloudinary.uploader
from cloudinary_storage.storage import RawMediaCloudinaryStorage
# from cloudinary_storage.storage import MediaCloudinaryStorage, RawMediaCloudinaryStorage
# from cloudinary_storage.fields import CloudinaryFileField


# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class Video(models.Model):
#     title = models.CharField(max_length=255)
#     # video_file = models.FileField(upload_to='videos/', storage=MediaCloudinaryStorage())
#     video_file = models.FileField(
#         upload_to='videos/',
#         storage=RawMediaCloudinaryStorage()  # Use RawMediaCloudinaryStorage for non-image files
#     )
#     # video_file = CloudinaryFileField(
#     #     resource_type='video',  # Specify video file type
#     #     upload_to='videos/',
#     #     storage=MediaCloudinaryStorage()
#     # )
#     category = models.ForeignKey(Category, related_name='videos', on_delete=models.CASCADE)

#     def save(self, *args, **kwargs):
#         # Ensure video is uploaded as `resource_type='video'`
#         if self.video_file and not hasattr(self.video_file, 'url'):
#             uploaded_file = cloudinary.uploader.upload(
#                 self.video_file,
#                 resource_type='video',  # Explicitly specify video
#                 folder='videos/'  # Specify folder in Cloudinary
#             )
#             self.video_file.name = uploaded_file['url']
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.title


from django.db import models
import cloudinary.uploader
from cloudinary_storage.storage import RawMediaCloudinaryStorage
# class Video(models.Model):
#     title = models.CharField(max_length=255)
#     video_file = models.FileField(upload_to='videos/', storage=RawMediaCloudinaryStorage())  # For user uploads
#     video_url = models.URLField(blank=True, null=True)  # To store Cloudinary URL
#     category = models.ForeignKey(Category, related_name='videos', on_delete=models.CASCADE)

#     # def save(self, *args, **kwargs):
#     #     if self.video_file and not self.video_url:
#     #         # Upload the video to Cloudinary as resource_type='video'
#     #         uploaded_file = cloudinary.uploader.upload(
#     #             self.video_file.file,  # Raw file object
#     #             resource_type='video',  # Specify video type
#     #             folder='videos/'  # Folder in Cloudinary
#     #         )
#     #         # Store the Cloudinary URL in the video_url field
#     #         self.video_url = uploaded_file['secure_url']

#     #     super().save(*args, **kwargs)

#     def save(self, *args, **kwargs):
#         # Check if video_file is updated or new
#         if self.pk:  # Object already exists
#             original_video = Video.objects.get(pk=self.pk)
#             if original_video.video_file != self.video_file:  # Check if video_file has changed
#                 # Upload the new video to Cloudinary
#                 uploaded_file = cloudinary.uploader.upload(
#                     self.video_file.file,  # Raw file object
#                     resource_type='video',  # Specify video type
#                     folder='videos/'  # Folder in Cloudinary
#                 )
#                 # Update the video_url with the new Cloudinary URL
#                 self.video_url = uploaded_file['secure_url']
#         elif self.video_file and not self.video_url:
#             # If it's a new video and there's no URL yet, upload to Cloudinary
#             uploaded_file = cloudinary.uploader.upload(
#                 self.video_file.file,  # Raw file object
#                 resource_type='video',  # Specify video type
#                 folder='videos/'  # Folder in Cloudinary
#             )
#             # Store the Cloudinary URL in the video_url field
#             self.video_url = uploaded_file['secure_url']

#         # Call the parent save method
#         super().save(*args, **kwargs)


#     def __str__(self):
#         return self.title




class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', storage=RawMediaCloudinaryStorage())  # Cloudinary storage
    video_url = models.URLField(blank=True, null=True)  # Cloudinary URL
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     if self.video_file and not self.video_url:
    #         # Upload video to Cloudinary
    #         uploaded_file = cloudinary.uploader.upload(
    #             self.video_file.file,  # Raw file object
    #             resource_type='video',
    #             folder='videos/'  # Folder in Cloudinary
    #         )
    #         # Store the Cloudinary URL in the video_url field
    #         self.video_url = uploaded_file['secure_url']
    #         # Prevent the file from being saved locally by clearing it
    #         self.video_file = None

    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:  # Check if updating an existing object
            old_video = Video.objects.filter(pk=self.pk).first()
            if old_video and old_video.video_url != self.video_url:
                # Delete the old video from Cloudinary
                public_id = old_video.video_url.split('/')[-1].split('.')[0]
                cloudinary.uploader.destroy(public_id, resource_type='video')

        if self.video_file:
            uploaded_file = cloudinary.uploader.upload(
                self.video_file.file,
                resource_type='video',
                folder='videos/'
            )
            self.video_url = uploaded_file['secure_url']
            self.video_file = None  # Prevent local save

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

