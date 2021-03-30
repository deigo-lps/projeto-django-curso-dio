from django.contrib import admin
from core.models import Evento
# Register your models here.

class EventoAdmin(admin.ModelAdmin):
  list_display=('id','titulo','usuario','data_criacao',)
  list_filter=('data_criacao','usuario',)

admin.site.register(Evento,EventoAdmin)
