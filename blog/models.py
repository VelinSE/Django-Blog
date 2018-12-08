from django.db import models
from django.contrib.auth.models import User

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO

# Create your models here.
class Post(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.FileField(upload_to="blog_image")
    thumbnail = models.FileField(upload_to="blog_thumbnails", null=True, blank=True)

    def ResizeImage(imageInput, name,  size):
        plw_image = Image.open(imageInput)
        resized_image = plw_image.resize(size)
        
        image_io = BytesIO()
        resized_image.save(image_io, format=plw_image.format)
        
        mimeType = Image.MIME[plw_image.format]
        
        return InMemoryUploadedFile(image_io, None, name, mimeType, resized_image.size, None)