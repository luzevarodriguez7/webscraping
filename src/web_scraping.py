import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# URL de de telemadrid
url = 'https://www.telemadrid.es/'

# Realizar la petición
try:
    respuesta = requests.get(url)
    #print(respuesta)
    #print(respuesta.text)
    # Verificar si la petición fue exitosa (código 200)
    if respuesta.status_code == 200:
        # Analizar el contenido con BeautifulSoup
        try:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            #print(soup)
            # Aquí puedes realizar operaciones de Web Scraping
            # ...
            try:
                noticias = soup.find_all('article', class_='card-news')
                if noticias:
                    #print(noticias)
                    lista_categorias = []
                    for articulo in noticias:
                        #print(articulo)
                        try:
                            titulo = articulo.find('a', class_='oop-link').text.strip()
                            url_noticia = articulo.find('a', class_='opp-link')['href']
                            print(url_noticia)
                            lista_url_noticia = url_noticia.split('/')
                            if lista_url_noticia[1] != '':
                                categoria = lista_url_noticia[1]
                            else:
                                categoria = lista_url_noticia[3]
                            lista_categorias.append(categoria)
                            lista_fecha = url_noticia.split('--')
                            fecha = lista_fecha[1].replace('.html','')
                            fecha_caracteres = lista_fecha[1].replace('.html', '')
                            # print(fecha_caracteres)
                            # print(fecha_caracteres[0:4])
                            # print(fecha_caracteres[4:6])
                            # print(fecha_caracteres[6:8])
                            # print(fecha_caracteres[8:10])
                            # print(fecha_caracteres[10:12])
                            # print(fecha_caracteres[12:14])
                            fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]),
                                             int(fecha_caracteres[6:8]), int(fecha_caracteres[8:10]),
                                             int(fecha_caracteres[10:12]), int(fecha_caracteres[12:14]))
                            fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
                            print(fecha)
                            print("hola")
                        except:
                            try:
                                titulo = articulo.find('a', class_='lnk').text.strip()
                                url_noticia = articulo.find('a', class_='lnk')['href']
                                lista_url_noticia = url_noticia.split('/')
                                if lista_url_noticia[1] != '':
                                    categoria = lista_url_noticia[1]
                                else:
                                    categoria = lista_url_noticia[3]
                                lista_categorias.append(categoria)
                                lista_fecha = url_noticia.split('--')
                                fecha_caracteres = lista_fecha[1].replace('.html', '')
                                #print(fecha_caracteres)
                                #print(fecha_caracteres[0:4])
                                #print(fecha_caracteres[4:6])
                                #print(fecha_caracteres[6:8])
                                #print(fecha_caracteres[8:10])
                                #print(fecha_caracteres[10:12])
                                #print(fecha_caracteres[12:14])
                                fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]), int(fecha_caracteres[6:8]),int(fecha_caracteres[8:10]),int(fecha_caracteres[10:12]),int(fecha_caracteres[12:14]))
                                fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
                            except:
                                pass
                    #print(lista_categorias)
                    conjunto_categorias = set(lista_categorias)
                    print(conjunto_categorias)
                else:
                    print(f"Error La pagina {url} no contiene noticias")
            except:
                    print(f"ERROR: No se pudo encontrar articulos en el codigo html")
        except:
            print(f"ERROR: no se pudo convertir la pagina a codigo html")
    else:
        print(f"Error al obtener la página web. Código de estado: {respuesta.status_code}")
except:
    print(f"ERROR: No se puede abrir la web pagina {url} o existe un error al procesarla")