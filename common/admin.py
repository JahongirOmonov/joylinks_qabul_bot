from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from import_export.formats.base_formats import XLSX, XLS, CSV, JSON
from django.utils.timezone import localtime
from django.apps import apps
from django.contrib import admin
from .models import Archive, Code, Language, RequiredChannels, TelegramProfile, Text, BannedUser



from .models import *
from .resources import (
    TelegramProfileResource,
    RegisterdUsersResource,
    LanguageResource,
    CodeResource,
    TextResource
)


class TextInline(admin.TabularInline):
    extra = 0
    model = Text


@admin.register(TelegramProfile)
class TelegramProfileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'chat_id', 'username', 'first_name', 'created_at', 'role')
    list_display_links = ('chat_id', 'username',)
    list_editable = ('role',)
    list_filter = ('role',)
    search_fields = ('chat_id', 'username', 'first_name', 'role')
    resource_class = TelegramProfileResource

@admin.register(RegisteredUsers)
class RegisteredUsersAdmin(ImportExportModelAdmin):
    list_display = ('id', 'ism', 'familiya', 'telefon', 'get_created_at','get_updated_at' , 'role')
    list_display_links = ('ism', 'familiya',)
    list_editable = ('role',)
    list_filter = (
    'role',)
    search_fields = (
    'chat_id',
    'username',
    'first_name',
    'role')
    resource_class = RegisterdUsersResource
    formats = [XLSX, XLS, CSV, JSON]
    
    
    def get_created_at(self, obj):
        local_time = localtime(obj.created_at)
        return local_time  # Yangi format
    get_created_at.short_description = "Yaratildi"  # Ustun nomi

    def get_updated_at(self, obj):
        local_time = localtime(obj.updated_at)
        return local_time  # Yangi format
    get_updated_at.short_description = "Yangilandi"  # Ustun nomi


@admin.register(Archive)
class ArchiveAdmin(ImportExportModelAdmin):
    list_display = ('short_title', 'author', 'created_at')

    def short_title(self, obj):
        return obj.title[:100]
    short_title.short_description = 'Title'


@admin.register(Language)
class LanguageAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'code')
    list_display_links = 'title', 'code'
    resource_class = LanguageResource


@admin.register(Code)
class CodeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title',)
    search_fields = ('title',)
    inlines = (TextInline,)
    resource_class = CodeResource




@admin.register(Text)
class TextAdmin(ImportExportModelAdmin):
    list_display = ('id', 'value', 'code', 'language', 'order', 'type')
    list_display_links = ('value', 'code')
    search_fields = ('value', 'code')
    resource_class = TextResource


for model in apps.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


# Ushbu bo‘limlarni admin paneldan olib tashlash
admin.site.unregister(Archive)
admin.site.unregister(Code)
admin.site.unregister(Language)
admin.site.unregister(RequiredChannels)
admin.site.unregister(TelegramProfile)
admin.site.unregister(Text)
admin.site.unregister(BannedUser)





