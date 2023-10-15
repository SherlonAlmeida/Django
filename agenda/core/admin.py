from django.contrib import admin
from core.models import Evento #Sherlon: Adicionado

# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    #Mostra os CAMPOS desejados na rota 'admin/'
    list_display = ('titulo', 'local', 'data_evento', 'data_criacao')

    #Apresenta um filtro interativo pelos CAMPOS definidos
    list_filter = ('usuario', 'data_evento', )

admin.site.register(Evento, EventoAdmin) #Sherlon: Adicionado