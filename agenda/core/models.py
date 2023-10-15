from django.db import models
from django.contrib.auth.models import User #Sherlon: importa a tabela default "User"

# Create your models here.

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name="Data do Evento")
    data_criacao = models.DateTimeField(auto_now=True) #Insere a hora atual neste campo
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #Sherlon: models.CASCADE é o comportamento a ser definido caso um usuário for definido do banco, neste caso também é excluído todos os eventos deste usuário.

    class Meta: #Força que o nome da tabela seja "evento" e não "core_evento"
        db_table = 'evento'
    
    def __str__(self):
        return self.titulo
    
    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y | %Hh%Mm')