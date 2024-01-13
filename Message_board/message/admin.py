from django.contrib import admin
from .models import UserProfile, Advertisement, AdCategory, Response, PrivatePage, PrivateResponse, Newsletter

admin.site.register(UserProfile)
admin.site.register(Advertisement)
admin.site.register(AdCategory)
admin.site.register(Response)
admin.site.register(PrivatePage)
admin.site.register(PrivateResponse)
admin.site.register(Newsletter)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = '__all__'


class AdCategoryAdmin(admin.ModelAdmin):
    list_display = '__all__'


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = '__all__'


class ResponseAdmin(admin.ModelAdmin):
    list_display = '__all__'


class PrivatePageAdmin(admin.ModelAdmin):
    list_display = '__all__'


class PrivateResponseAdmin(admin.ModelAdmin):
    list_display = '__all__'


class NewsletterAdmin(admin.ModelAdmin):
    list_display = '__all__'
