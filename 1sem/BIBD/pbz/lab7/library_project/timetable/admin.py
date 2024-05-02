from django.contrib import admin
from .models import Library

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('library_number', 'address', 'phone')
    search_fields = ('library_number', 'address', 'phone')
    list_filter = ('address', 'phone')
