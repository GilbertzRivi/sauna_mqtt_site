from django import setup
setup()
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django import urls
import paho.mqtt.client as mqtt
from .models import Mqtt
import time

def on_connect(client, userdata, flags, rc):
    client.subscribe("/sauna/T")
    client.subscribe("/sauna/H")
    client.subscribe("/sauna/status")

def on_message(client, userdata, msg):
    obj = Mqtt.objects.first()
    if msg.topic == "/sauna/T":
        obj.T = msg.payload.decode("ASCII")
    if msg.topic == "/sauna/H":
        obj.H = msg.payload.decode("ASCII")
    if msg.topic == "/sauna/status":
        status = msg.payload.decode("ASCII")
        if status == '0':
            obj.status = "OFF"
        else:
            obj.status = "ON"
    obj.save()

def main_site(request):
    logout(request)
    if request.method == 'POST':
        
        username = request.POST.get('login')
        password = request.POST.get('password')
        print(username, password)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(urls.reverse(loggedin))
    
    return render(request, 'index.html')

def loggedin(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        if 'ON' in list(request.POST.keys()):
            client.publish('/sauna', 'ON')
        elif 'OFF' in list(request.POST.keys()):
            client.publish('/sauna', 'OFF')
        time.sleep(0.5)
    obj = Mqtt.objects.first()
    context = {
        'T': obj.T,
        'H': obj.H,
        'status': obj.status,
        }
    return render(request, 'loggedin.html', context=context)

client = mqtt.Client('test')
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("", "")
client.connect("", )
