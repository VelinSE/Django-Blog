from django.db import models
from django.contrib.auth.models import User

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO

# Create your models here.
class Post(models.Model):
    user =  models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.FileField(upload_to="blog_image")
    thumbnail = models.FileField(upload_to="blog_thumbnails", null=True, blank=True)

    class Meta:
        permissions = (
            ("view_original_img", "Can view the original image of a blog post"),
            ("run_seeds", "Can sun seed methods against the database"),
            ("run_exports", "Can run user and blog exports")
        )

    def ResizeImage(imageInput, name,  size):
        plw_image = Image.open(imageInput)
        resized_image = plw_image.resize(size)
        
        image_io = BytesIO()
        resized_image.save(image_io, format=plw_image.format)
        
        mimeType = Image.MIME[plw_image.format]
        
        return InMemoryUploadedFile(image_io, None, name, mimeType, resized_image.size, None)