from django.http import HttpResponse
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views.generic import View
#nueva página = la misma pero con otra url, no se abre otra ventana
def hello_world(request):
    url = 'https://rickandmortyapi.com/api/episode'
    response = requests.get(url)
    todo = []
    if response.status_code == 200:
        response_json = response.json()
        for episodio in response_json['results']:
            todo.append({"id":episodio["id"],"name":episodio["name"],"info": "Fecha de emisión: " + episodio["air_date"] + " , Código: " + episodio["episode"]})
    #segunda página
    url = 'https://rickandmortyapi.com/api/episode?page=2'
    response = requests.get(url)
    if response.status_code == 200:
        response_json = response.json()
        for episodio in response_json['results']:  
            todo.append({"id":episodio["id"],"name":episodio["name"],"info": "Fecha de emisión: " +episodio["aid_date"]+ " , Código: " + episodio["episode"]})
            
    #ordenar lista por id 
    todo= sorted(todo, key = lambda i: i['id']) 
    if request.GET.get('buscar'):  
        palabra=request.GET.get('buscar')
        return buscador(request,palabra)
    
    context = {
    'informacion' : todo, 
    'número': len(todo)
    }
    return render(request, 'home.html', context)

def home2(request,capitulo):
    url = 'https://rickandmortyapi.com/api/episode/'+ capitulo
    response = requests.get(url)
    informacion = {}
    caracters = []
    if response.status_code == 200:
        response_json = response.json()
        informacion["id"] = response_json["id"]
        informacion["name"] = response_json["name"]
        informacion["fecha"] = response_json["air_date"]
        informacion["código"] = response_json["episode"]
        for caracter in response_json["characters"]:
            response_p = requests.get(caracter)
            response_json_p = response_p.json()
            caracters.append({"id": response_json_p["id"], "name": response_json_p["name"]})
    if request.GET.get('buscar'):  
        palabra=request.GET.get('buscar')
        return buscador(request,palabra)
    informacion["caracteres"] = caracters
    context = {
    'info2' : informacion  
    }
    return render(request, 'home2.html', context)

def home3(request,personaje):  #id
    url = 'https://rickandmortyapi.com/api/character/'+ personaje
    response = requests.get(url)
    informacion = {}
    episodios = []
    if response.status_code == 200:
        response_json = response.json()
        informacion["id"] = response_json["id"]
        informacion["name"] = response_json["name"]
        informacion["estado"] = response_json["status"]
        informacion["especie"] = response_json["species"]
        informacion["lugar_origen"] = response_json["origin"]  
        l=response_json["origin"]["url"]
        num=False
        numero=False
        for j in range(len(l)):
            if l[len(l)-1-j]== "/":
                num= l[len(l)-j:]
                break
        if num:
            informacion["lugar_origen"]["id"] = num
        else:
            informacion["lugar_origen"]["id"] = 0
        informacion["imagen"] = response_json["image"]
        informacion["genero"] = response_json["gender"]
        informacion["ultima_l"] = response_json["location"] #name, url
        s=response_json["location"]["url"]
        for i in range(len(s)):
            if s[len(s)-1-i]== "/":
                numero= s[len(s)-i:]
                break
        if numero:
            informacion["ultima_l"]["id"] = numero
        else:
            informacion["ultima_l"]["id"] = 0
        if response_json["type"] == "":
            informacion["tipo"] = "Sin información"
        else:
            informacion["tipo"] =  response_json["type"] 
        for episodio in response_json["episode"]:
            response2 = requests.get(episodio)
            response_json2 = response2.json()
            episodios.append({"name":response_json2["name"] , "id":response_json2["id"] })

    informacion["episodios"] = episodios
    if request.GET.get('buscar'):  
        palabra=request.GET.get('buscar')
        return buscador(request,palabra)
    context = {
    'info3' : informacion
    }
    return render(request, 'home3.html', context)

def home4(request, locacion):
    url = 'https://rickandmortyapi.com/api/location/'+ locacion
    response = requests.get(url)
    informacion = {}
    gente = []
    if response.status_code == 200:
        response_json = response.json()
        informacion["id"] = response_json["id"]
        informacion["name"] = response_json["name"]
        if informacion["id"]==0:
            informacion["tipo"] = "unknown"
            informacion["dimension"] = "unknown"
        else:
            informacion["tipo"] = response_json["type"]
            informacion["dimension"] = response_json["dimension"]
            for persona in response_json["residents"]:
                response2 = requests.get(persona)
                response_json2 = response2.json()
                gente.append({"name":response_json2["name"] , "id":response_json2["id"] })

        informacion["gente"] = gente

    if request.GET.get('buscar'):  
        palabra=request.GET.get('buscar')
        return buscador(request,palabra)

    context = {
    'info4' : informacion
    }
    return render(request, 'home4.html', context)

def buscador(request, palabra):
    #buscar en episodios,caracterres y lugares solo en el nombre
    print("ENTRO AL BUSCARDOR")
    url = 'https://rickandmortyapi.com/api/episode/?name='+palabra
    response = requests.get(url)
    informacion = {}
    episodios = []
    if response.status_code == 200:
        response_json = response.json()
        paginas= response_json["info"]["pages"]
        for epi in response_json["results"]:  #primera página
            episodios.append({"id": epi["id"],"name":epi["name"]})
        if paginas>1:
            for pagina in range(1,paginas):  
                response = requests.get(response_json["info"]["next"])
                response_json = response.json()
                for epi in response_json["results"]:
                    episodios.append({"id": epi["id"],"name":epi["name"]})
    url2 = 'https://rickandmortyapi.com/api/character/?name='+palabra
    response = requests.get(url2)
    caracteres = []
    if response.status_code == 200:
        response_json = response.json()
        paginas= response_json["info"]["pages"]
        for car in response_json["results"]:  #primera página
            caracteres.append({"id": car["id"],"name":car["name"]})
        if paginas>1:
            for pagina in range(1,paginas):  
                response = requests.get(response_json["info"]["next"])
                response_json = response.json()
                for car in response_json["results"]:
                    caracteres.append({"id": car["id"],"name": car["name"]})
    url3 = 'https://rickandmortyapi.com/api/location/?name='+palabra
    response = requests.get(url3)
    lugares = []
    if response.status_code == 200:
        response_json = response.json()
        paginas= response_json["info"]["pages"]
        for lug in response_json["results"]:  #primera página
            lugares.append({"id": lug["id"],"name":lug["name"]})
        if paginas>1:
            for pagina in range(1,paginas):  
                response = requests.get(response_json["info"]["next"])
                response_json = response.json()
                for lug in response_json["results"]:
                    lugares.append({"id": lug["id"],"name": lug["name"]})                    
    informacion["episodios"]= episodios
    informacion["caracteres"]=caracteres
    informacion["lugares"]=lugares
    context = {'encontrado' : informacion, 'buscar': palabra}
    return render(request, 'buscador.html', context)

