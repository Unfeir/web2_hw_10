from django.contrib import admin

# Register your models here.
from .models import Author, Note, Tag
admin.site.register(Author)
admin.site.register(Note)
admin.site.register(Tag)


