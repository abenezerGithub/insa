from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Report, Attachment
from .models import User
from django.utils.html import format_html

# Define the custom UserAdmin class
class UserAdmin(BaseUserAdmin):
    # Define the fields to be displayed in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Define the fields to be displayed in the user edit form
    fieldsets = (
        ("Identifiers", {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Define the fields to be used when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

# Register the custom UserAdmin class
admin.site.register(User, UserAdmin)

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1
    readonly_fields = ('display_image',)

    def display_image(self, instance):
        if instance.image:
            image_url = instance.image.url
            return format_html('<a href="{}" target="_blank"><img src="{}" width="280" /></a>', image_url, image_url)
        return "No Image"
    display_image.short_description = 'Image'

class ReportAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]
    list_display = ('report_type', 'user', 'date_reported', 'is_resolved', 'seen')
    search_fields = ('report_type', 'report_description', 'user__username')

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'image_link')
    search_fields = ('image',)
    
    def image_link(self, obj):
        if obj.image:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.image.url, obj.image.url)
        return "No Image"

admin.site.register(Report, ReportAdmin)
admin.site.register(Attachment, AttachmentAdmin)
