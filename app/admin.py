from django.contrib import admin
from .models import Category, Video, UserCategoryAccess
from django_bunny_storage.storage import BunnyStorage

admin.site.register(Category)
# admin.site.register(Video)
admin.site.register(UserCategoryAccess)
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Dynamically set storage at runtime for the admin form
        form.base_fields['video_file'].storage = BunnyStorage()
        return form
