"""
object
    Se trata de automaticamente encontrar la imagen que pide usuario, y ofrecer varias funciones, puede ser mejorar la calidad, sacar waterproof...

----------------------------------------------------------------------------------------------------------------------------------------------------
0- add a clock que finaliza el programa si no funca

1- Recibir el producto
    1- Recibir el nombre

2- Encontrar el producto en el internet
    1- Encontrar links mas apropiados del productos (webscrapting or API)
    2- Crear una carpeta basando la direccion
    3- Bajar imagenes a traves de sus links correspondientes y guardarlos en la carpeta creada en 2-2

3- Filters
    1- Format Filter
    2- info_list -> extract features of all images
    3- DPI Filter
    4- Resolution (width / height) Filter
    5- Rename Filter

4- Usuario Selecciona uno de los preferidos
    1- Usuario selecciona una imagen entre las opciones

5- Ofrecer diferentes funcionalidades
    1- scratch the image and transform to png
    2- Mejor Calidad
    3- ReLighting
    4- Sacar Waterproof
    5- ...
"""

import numpy as np
import os
import cv2 as cv
import wget
from serpapi import GoogleSearch
import sys
import datetime
import time
from PIL import Image


GoogleSearch.SERP_API_KEY = api_key
DPI_min = 80
Width_min = 600
Height_min = 600

#mian
def main():
    dir = r"C:\Users\Administrator\AntoC_automation\demon slayer"
    info_list = []
    DPIrequerido = True


    productoName = recibirNombreDeProducto()
    crearUnaCarpetaPadre(dir)

    dir = updateDir(dir, productoName)
    crearUnaCarpetaHija(dir)
    encontrarLinksDeProducto(productoName, dir)
    
    format_Filter(dir)

    all_info_list = extract_features(dir, info_list)

    dpi_info_list = dpi_Filter(all_info_list, DPIrequerido)
    resolution_info_list = resolution_Filter(dpi_info_list)
    rename_info_list = rename_Filter(resolution_info_list, productoName)
    

    for image in all_info_list:
        print(image)

    mostrarTodasImagenes(all_info_list)




#0
def setAClock():
    Hour = 0
    Minute = 1
    Second = 0

    now = datetime.datetime.now()
    hour_now = now.hour
    minute_now = now.minute
    second_now = now.second

    Sum_now = hour_now * 3600 + minute_now * 60 + second_now
    Sum = Hour * 3600 + Minute * 60 + Second

    Sum_Predict = Sum_now + Sum

    Hour_Predict = int(Sum_Predict / 3600)
    RestHour_Predict = Sum_Predict % 3600
    Minute_Predict = int(RestHour_Predict / 60)
    Second_Predict = RestHour_Predict % 60

    print("{}{}{}{}{}".format(Hour_Predict, ":", Minute_Predict, ":", Second_Predict))

    for i in range(Sum):
        TrueHour = int((Sum - i) / 3600)
        RestHour = (Sum - i) % 3600
        TrueMinute = int(RestHour / 60)
        TrueSecond = RestHour % 60
        print("{}{}{}{}{}".format(TrueHour, ":", TrueMinute, ":", TrueSecond))
        time.sleep(1)

    sys.exit()

#0-1
def crearUnaCarpetaPadre(dir):
    if not(os.path.isdir(dir)):
        os.mkdir(dir)

#1-1
def recibirNombreDeProducto():
    productoName = input("输入产品名称: ")
    return productoName

#2-1
def encontrarLinksDeProducto(productoName, dir):
    search = GoogleSearch({"q": productoName, "tbm": "isch"})
    for image_result in search.get_dict()['images_results']:
        link = image_result["original"]
        try:
            print("link: " + link)
            transformarLinkAImagen(link, dir)
        except:
            pass
    print("images found")

#2-2
def updateDir(dir, productoName):
    NewDir = os.path.join(dir, productoName)
    return NewDir

def crearUnaCarpetaHija(dir):
    if not(os.path.isdir(dir)):
        os.mkdir(dir)

#2-3
def transformarLinkAImagen(link, dir):
    wget.download(link, out = dir)

#3-0
def file_path_shortcut(file):
    file_path = os.path.join(file["Filedir"], file["Filename"])
    return file_path

#PIL library no es suficiente powerful, su image.format no puede identificar aquellos imagenes que no tengan formato, peor que library os.
#3-1
def format_Filter(dir):
    print("format filter")
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        # Delete all non .jpg or .png or jpeg files
        file_extension = os.path.splitext(file_path)[1].lower()
        if os.path.isfile(file_path):
            if file_extension == ".jpg" or file_extension == ".png" or file_extension == ".jpeg":
                pass
            else:
                os.remove(file_path)
        else:
            print("error")
    print("format filter OK")

#3-2
# Delete all non .jpg or .png file
def extract_features(dir, info_list):
    print("extract_features")
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        image = Image.open(file_path)
        if os.path.isfile(file_path):
            try:
                info_image = {
                    "Filedir": os.path.dirname(image.filename),
                    "Filename": os.path.basename(image.filename),
                    "Image DPI": image.info['dpi'],
                    "Image Height": image.height,
                    "Image Width": image.width,
                    "Image Format": image.format,
                    "Image Mode": image.mode
                }
            except KeyError:
                info_image = {
                    "Filedir": os.path.dirname(image.filename),
                    "Filename": os.path.basename(image.filename),
                    "Image Height": image.height,
                    "Image Width": image.width,
                    "Image Format": image.format,
                    "Image Mode": image.mode
                }
            info_list.append(info_image)
        else:
            print("error")
    return info_list

#3-3
# filter dpi
def dpi_Filter(all_info_list, requerido):
    if requerido:
        new_list = []
        print("dpi filter")
        for file in all_info_list:
            file_path = file_path_shortcut(file)
            if "Image DPI" in file:
                if file["Image DPI"][0] > DPI_min:
                    new_list.append(file)
                else:
                    os.remove(file_path)
            else:
                os.remove(file_path)
        print("dpi filter OK")
        return new_list
    else:
        return all_info_list

#3-4
# filter resolution
def resolution_Filter(dpi_info_list):
    new_list = []
    print("resolution filter")
    for file in dpi_info_list:
        file_path = file_path_shortcut(file)
        if file["Image Height"] > Height_min and file["Image Width"] > Width_min:
            new_list.append(file)
        else:
            os.remove(file_path)
    return new_list

#3-5
def rename_Filter(resolution_info_list, productoName):
    new_list = []
    print("rename filter")
    i = 0
    for file in resolution_info_list:
        file_path = file_path_shortcut(file)
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".jpg":
            name = "{}{}{}{}{}".format(file["Filedir"], '\\', productoName, i, ".jpg")
            i += 1
            file["Filename"] = name
            new_list.append(file)
            os.rename(file_path, name)
        elif file_extension == ".png":
            name = "{}{}{}{}{}".format(file["Filedir"], '\\', productoName, i, ".png")
            i += 1
            file["Filename"] = name
            new_list.append(file)
            os.rename(file_path, name)
        elif file_extension == ".jpeg":
            name = "{}{}{}{}{}".format(file["Filedir"], '\\', productoName, i, ".jpeg")
            i += 1
            file["Filename"] = name
            new_list.append(file)
            os.rename(file_path, name)
        else:
            print("error")
    print("rename filter OK")
    return new_list

#4-1
def mostrarTodasImagenes(rename_info_list):
        for file in rename_info_list:
            file_path = file_path_shortcut(file)

            img = cv.imread(file_path)
            #img = cv.resize(img, (800, 800), interpolation=cv.INTER_CUBIC)
            cv.imshow('Image', img)

            cv.waitKey(0)


main()

