from django.contrib import admin

from blog.models import Post

@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
    pass