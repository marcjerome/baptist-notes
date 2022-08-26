from django.contrib import admin
from .models import Preaching, Tag

class PreachingAdmin(admin.ModelAdmin):
    list_display= ('title', 'date')
    fields = ['title', 'text', 'privacy', 'tags']

    def save_model(self,request,obj,form,change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
        
admin.site.register(Preaching, PreachingAdmin)
admin.site.register(Tag)