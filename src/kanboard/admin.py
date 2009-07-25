from kanboard.models import Board, Card, Phase
from django.contrib import admin

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    # list_filter = ('room', 'user', 'status')
    # date_hierarchy = 'created_at'
    search_fields = ('title', 'description')

class CardAdmin(admin.ModelAdmin):
    pass

class PhaseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Board, BoardAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Phase, PhaseAdmin)

