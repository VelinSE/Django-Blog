from django.contrib import admin

from recepie.models import UserExtended

from blog.models import Post, Ingredient

@admin.register(Post)
@admin.register(Ingredient)
@admin.register(UserExtended)
class AuthorAdmin(admin.ModelAdmin):
    pass