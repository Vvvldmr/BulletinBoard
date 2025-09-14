from django.contrib import admin
from .models import City, Advertisement

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'city', 'author', 'created_at']
    list_filter = ['city', 'created_at', 'author']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('city', 'author')