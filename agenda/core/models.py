from django.db import models
from django.contrib.auth.models import User #Sherlon: importa a tabela default "User"

# Create your models here.

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name="Data do Evento")
    data_criacao = models.DateTimeField(auto_now=True) #Insere a hora atual neste campo
    local = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #Sherlon: models.CASCADE é o comportamento a ser definido caso um usuário for definido do banco, neste caso também é excluído todos os eventos deste usuário.

    class Meta: #Força que o nome da tabela seja "evento" e não "core_evento"
        db_table = 'evento'
    
    def __str__(self):
        return self.titulo
    
    #Método para mostrar a DATA/HORA formatada na tela
    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y | %Hh%Mm')
    
    #Método para atualizar a DATA/HORA de acordo com o formato PADRÃO do BD
    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')