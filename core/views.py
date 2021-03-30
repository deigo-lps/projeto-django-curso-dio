from django.shortcuts import render,redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.http.response import Http404
# Create your views here.

def login_user(request):
  return render(request,"login.html")

def submit_login(request):
  if request.POST:
    username=request.POST.get('username')
    password=request.POST.get('password')
    usuario=authenticate(username=username,password=password)
    cadastro=request.POST.get('cadastro')
    if usuario:
      login(request,usuario)
    elif cadastro and username and password:
      try:
        usuario=User.objects.create_user(username,'',password)
      except Exception:
        messages.error(request,'Usuário ja existente.')
        return redirect('/')
      else:
        login(request,usuario)
    else:
      messages.error(request,'Usuário ou senha inválidos.')
  return redirect('/')

@login_required(login_url='/login/')
def logout_user(request):
  logout(request)
  return redirect('/')

@login_required(login_url='/login/')
def evento(request):
  id_evento=request.GET.get('id')
  dados={}
  if id_evento:
    try:
      dados['evento']=Evento.objects.get(usuario=request.user,id=id_evento)
    except Exception:
      raise Http404
  return render(request,"evento.html",dados)

@login_required(login_url='/login/')
def submit_evento(request):
  if request.POST:
    titulo=request.POST.get('titulo')
    local=request.POST.get('local')
    descricao=request.POST.get('descricao')
    data_evento=request.POST.get('data_evento')
    usuario=request.user
    id_evento=request.POST.get('id_evento')
    if titulo and data_evento:
      if id_evento:
        Evento.objects.filter(usuario=request.user,id=id_evento).update(titulo=titulo,local=local,descricao=descricao,data_evento=data_evento,usuario=usuario)
      else:
        Evento.objects.create(titulo=titulo,local=local,descricao=descricao,data_evento=data_evento,usuario=usuario)
    else:
      messages.error(request,'Título e data são campos obrigatórios.')
      return redirect('/agenda/evento')
  return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request,id_evento):
  try:
    Evento.objects.get(usuario=request.user,id=id_evento).delete()
  except Exception:
    raise Http404
  return redirect('/')

@login_required(login_url='/login/')
def agenda(request):
  time=datetime.now() - timedelta(days=1)
  evento=Evento.objects.filter(usuario=request.user,data_evento__gt=time)
  dados={'eventos': evento}
  return render(request,'agenda.html',dados)

@login_required(login_url='/login/')
def historico(request):
  time=datetime.now() - timedelta(days=1)
  evento=Evento.objects.filter(usuario=request.user,data_evento__lt=time)
  dados={'eventos': evento}
  return render(request,'historico.html',dados)
