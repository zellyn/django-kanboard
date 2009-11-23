from django.contrib import admin
from kanboard import models


class PhaseInline(admin.StackedInline):
    model = models.Phase


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    search_fields = ('title', 'description')
    inlines = [PhaseInline]


class CardAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(models.Board, BoardAdmin)
admin.site.register(models.Card, CardAdmin)

