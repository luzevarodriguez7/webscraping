# importar el modulo request para extraer una pagina web
import requests
# importar del modulo bs4 la libreria BeautifulSoup para transformar el codigo en html
from bs4 import BeautifulSoup
# importa del modulo datetime la libreria datetime para poder cambiar el formato de las fechas
from datetime import datetime


def formatear_fecha(fecha_caracteres):
    try:
        # se crea un objeto. coge los primeros cuatro caracteres para el año, los  2 siguientes para el mes y los 2 siguientes para el dia
        fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]),
                         int(fecha_caracteres[6:8]))
        # ponemos la cadena de la fecha en el formato año,mes,día
        return fecha.strftime("%Y/%m/%d")
    except Exception as e:
        # si ocurre una excepción en el bloque try, se ejecuta el except y devuelve el siguiente mensaje
        print(f"Error: No se pudo convertir la fecha al formato requerido. {e}")
# definimos una funcion para extraer de la pagina de telemadrid.es, que seria 'url_scraping', las noticias con categoría 'todas'
def webscraping(url_scraping,categoria_scraping='todas'):
    # URL de telemadrid
    url = url_scraping

    # Realizar la petición
    try:
        #realiza la solicitud a la página y la asocia a la variable 'respuesta'
        respuesta = requests.get(url)
        #print(respuesta)
        #print(respuesta.text)
        # Verifica si la petición fue exitosa (código 200)
        if respuesta.status_code == 200:
            try:
                #en caso de que la respuesta sea exitosa crea un archivo CSV para almacenar la información
                with open('../data/noticias.csv', 'w') as f:
                    #almacena la información del título, la dirección web de la noticia, la categoría y la fecha. Indicamos que haga un enter después de cada una
                    f.write('titulo,url,categoria,fecha'+'\n')
                # Analizar el contenido con BeautifulSoup
            except:
                #en caso de no ser exitosa nos devuelve el texto de error que hemos escrito entre comillas
                print("ERROR: no se pudo crear el archivo noticias.csv")
            try:
                #parsea el texto para analicar el contenido html de la respuesta obtenida
                soup = BeautifulSoup(respuesta.text, 'html.parser')
                #print(soup)
                # Aquí puedes realizar operaciones de Web Scraping
                try:
                    #busca en la clase 'card-news' todas las que incluyan 'article'
                    noticias = soup.find_all('article', class_='card-news')
                    if noticias:
                        #print(noticias)
                        #creamos una lista llamada 'lista_categorias' vacia
                        lista_categorias = []
                        #iteración de los elementos de las noticias que se encuentran
                        for articulo in noticias:
                            #print(articulo)
                            #comenzamos a definir la información que queremos extraer de las noticas
                            try:
                                #intentará extraer el título de cada noticia que tenga como clase 'opp-link'. Extrae el texto de cada una.
                                titulo = articulo.find('a', class_='oop-link').text.strip()
                                #hace lo mismo que la anterior línea pero lo que extrae la URL de cada noticia
                                url_noticia = articulo.find('a', class_='opp-link')['href']
                                #print(url_noticia)
                                #convertimos cada URL en una lista utilizando el caracter '/' domo divisor
                                lista_url_noticia = url_noticia.split('/')
                                #verifica si el segundo elemento de la lista es un espacio vacio
                                if lista_url_noticia[1] != '':
                                    #si no es un espacio vacio se asigna lo que haya a la variable 'categoría'
                                    categoria = lista_url_noticia[1]
                                else:
                                    #si el if no se cumple, se asigna lo que haya en la cuarta posición
                                    categoria = lista_url_noticia[3]
                                #cada categoría se añade a la lista
                                lista_categorias.append(categoria)
                                #utilizamos de nuevo la URL creando otra lista para extraer la fecha, utilizando '--' como delimitador
                                lista_fecha = url_noticia.split('--')
                                #coge el segundo elemento de la lista_fecha, que es donde está la fecha y elimina '.html' si lo contiene
                                fecha_caracteres = lista_fecha[1].replace('.html', '')
                                # print(fecha_caracteres)
                                # print(fecha_caracteres[0:4])
                                # print(fecha_caracteres[4:6])
                                # print(fecha_caracteres[6:8])
                                # print(fecha_caracteres[8:10])
                                # print(fecha_caracteres[10:12])
                                # print(fecha_caracteres[12:14])
                                #definimos una funcion para convertir la fecha al formato año/mes/dia
                                fecha = formatear_fecha(fecha_caracteres)
                                #elimina del título las barras, las comillas y las comas
                                titulo = titulo.replace('\'','').replace('"','').replace(',','')
                                #escritura en un archivo CSV si 'categoria_scraping'es igual a 'todas'
                                if categoria_scraping == 'todas':
                                    try:
                                        #si se cumple la condición, la información se almacenará en el archivo noticias.csv
                                        with open('../data/noticias.csv', 'a') as f:
                                            #se almacenará el título, la URL, la catedoria y la fecha como un string. Separado por comas y con un enter al final
                                            f.write(titulo+','+url_noticia+','+categoria+','+str(fecha)+'\n')
                                        # Analizar el contenido con BeautifulSoup
                                        #si no consigue anexionar la noticia ar archivo devolverá el error que indicamos
                                    except:
                                        print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                #en caso de que la categoría no sea igual a 'todas', se repiten las acciones pero para la categoria elegida
                                else:
                                    if categoria == categoria_scraping:
                                        try:
                                            with open('../data/noticias_'+categoria_scraping+'.csv', 'a') as f:
                                                f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                    fecha) + '\n')
                                            # Analizar el contenido con BeautifulSoup
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                            #si no se encuentra la clase opp-link, se repite el código pero en este caso para la clase 'lnk'
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
                                    fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]), int(fecha_caracteres[6:8]))
                                    fecha = fecha.strftime("%Y/%m/%d")
                                    titulo = titulo.replace('\'', '').replace('"', '').replace(',', '')
                                    if categoria_scraping == 'todas':
                                        try:
                                            with open('../data/noticias.csv', 'a') as f:
                                                f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                    fecha) + '\n')
                                            # Analizar el contenido con BeautifulSoup
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                    else:
                                        if categoria == categoria_scraping:
                                            try:
                                                with open('../data/noticias_' + categoria_scraping + '.csv', 'a') as f:
                                                    f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                        fecha) + '\n')
                                                # Analizar el contenido con BeautifulSoup
                                            except:
                                                print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                except:
                                    #si haya algún problema al extraer la información de una noticia, se sigue con la siguiente
                                    pass
                        #print(lista_categorias)
                        conjunto_categorias = set(lista_categorias)
                        #print(conjunto_categorias)
                    else:
                        #devuelve este error en caso de que no URL non encuentre noticias
                        print(f"Error La pagina {url} no contiene noticias")
                except:
                        #devuelve este error si no se encuentra article en el código html
                        print(f"ERROR: No se pudo encontrar articulos en el codigo html")
            except:
                #devuelve este error si encuentra la página pero no puede convertir el código encontrado en html
                print(f"ERROR: no se pudo convertir la pagina a codigo html")
        else:
            #devuelve este error si al hacer la petición no devuelve es status 200
            print(f"Error al obtener la página web. Código de estado: {respuesta.status_code}")
    except:
        #devuelve este error si no encuentra la página que le indicamos o tiene problemas para ello
        print(f"ERROR: No se puede abrir la web pagina {url} o existe un error al procesarla")
    #devuelve el conjunto de categorias una vez que ha realizado el scraping
    return conjunto_categorias

#llama a la función webscraping para obtener todas las categorías
listado_categorias = webscraping('https://www.telemadrid.es/','todas')
seleccion = 'x'
#el bucle while permite al usuario seleccionar la categoría concreta con la que quiere hacer el web scraping
#el bucle se ejecutará solo si la selección del usuario es distinta de cero
while seleccion != '0':
    #imprime un mensaje con la lista de las categorias
    print("Lista de categorias: ")
    #se asocia a la variable i el 1 para enumerar las categorias
    i = 1
    #inicia el bucle for que itera cada elemento
    for opcion in listado_categorias:
        #cada elemento se llama 'opcion'
        print(f"{i}.- {opcion}")
        #va incrementando el valor de cada iteración del bucle para que cada opción tenga su número correlativo
        i = i + 1
    #si el usuario escoge la opción 0 sale del bucle
    print("0.- Salir")
    #se pide al usuario que elija la opción que quiere según el número de cada una
    seleccion = input("Por favor seleccione una opcion indicando un numero:")
    #convierte 'listado_categorias' en una nueva lista llamada 'categorias_listas
    categorias_listas = list(listado_categorias)
    #obtiene la categoría que el usuario ha seleccionado(el -1 es porque en python el primer campo es cero)
    categoria_seleccionada = categorias_listas[int(seleccion)-1]
    #hace el webscraping de la categoría seleccionada
    webscraping('https://www.telemadrid.es/', categoria_seleccionada)