from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
# Create your models here.

class Evento(models.Model):
  titulo=models.CharField(max_length=100)
  local=models.CharField(blank=True,null=True,max_length=100,verbose_name='Local do Evento')
  descricao=models.TextField(blank=True,null=True)
  data_evento=models.DateTimeField(verbose_name='Data do Evento')
  data_criacao=models.DateTimeField(auto_now=True,verbose_name='Data de Criação')
  usuario=models.ForeignKey(User,on_delete=models.CASCADE)

  class Meta:
    db_table='evento'

  def __str__(self):
    return self.titulo

  def get_data_input_evento(self):
    return self.data_evento.strftime('%Y-%m-%dT%H:%M')

  def get_data_atrasado(self):
    return self.data_evento <= datetime.now()

  def get_data_comecando(self):
    data=datetime.now() + timedelta(hours=1)
    return self.data_evento <= data and self.data_evento > datetime.now()
