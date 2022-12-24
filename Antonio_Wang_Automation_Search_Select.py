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

4- Usuario Selecciona uno de los preferidos -> maybe use: TK, matplotlib
    1- Usuario selecciona una imagen entre las opciones

5- Automation Edit
"""



import numpy as np
import os
import cv2 as cv
import wget
from serpapi import GoogleSearch
import sys
import datetime
import time
from tkinter import *
from PIL import Image, ImageTk
import requests
import shutil


GoogleSearch.SERP_API_KEY = "2d7a85845704f2371158b0b4c5239fec8e5e121e5667cdd10ee515cbf6b0b376"
DPI_min = 30
Width_min = 600
Height_min = 600
image_selected = {
                    "Filedir": None,
                    "Filename": None,
                    "Image DPI": None,
                    "Image Height": None,
                    "Image Width": None,
                    "Image Format": None,
                    "Image Mode": None
                }

#main
#to improve:
#   1- need interface for dpi and resolution
#   2- need interface for "5", edit process OKKKKKK
#   3- do a clock on searching process -> https://stackoverflow.com/questions/492519/timeout-on-a-function-call
#   4- find more edit tools and maybe improve use of APIs Naaaa
#   5- google search method to let the searching more p

def main():
    ventana = Tk()

    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    screen_size = "{}{}{}".format(screen_width, "x", screen_height)

    ventana.geometry(screen_size)
    ventana.title("Elegir modo")

    button_width = 20
    button_height = 5

    search_select_x = screen_width / 4 * 1 - button_width
    search_select_y = screen_height / 2 - button_height * 4

    edit_x = screen_width / 4 * 3 - button_width
    edit_y = search_select_y

    quit_x = screen_width - button_width * 8
    quit_y = 0

    search_select_botton = Button(ventana, text="Modo search select", command=lambda : modo_search_select(ventana),
                                 height=button_height, width=button_width)
    search_select_botton.place(x=search_select_x, y=search_select_y)
    edit_botton = Button(ventana, text="Modo edit", command=lambda: modo_editar(ventana),
                              height=button_height, width=button_width)
    edit_botton.place(x=edit_x, y=edit_y)
    Quit = Button(ventana, text="Quit", command=ventana.destroy, height=button_height, width=button_width)
    Quit.place(x=quit_x, y=quit_y)

    ventana.mainloop()

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
            except:
                os.remove(file_path)

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
            name = "{}{}{}{}{}{}".format(file["Filedir"], '\\', productoName, " ", i, ".jpg")
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
def image_found(rename_info_list, position, root):
    root.destroy()
    global image_selected
    image_selected = rename_info_list[position]

def mostrar_imagen(rename_info_list, position, max_position, root):
    root = Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    screen_size = "{}{}{}".format(screen_width, "x", screen_height)

    max_height = screen_height / 3 * 2

    root.geometry(screen_size)
    try:
        root.title(rename_info_list[position]["Filename"])
    except:
        root.title("unknown")

    if 0 <= position <= max_position:
        file_path = file_path_shortcut(rename_info_list[position])

        image = Image.open(file_path)
        image_width = image.width
        image_height = image.height

        proportion = max_height / image_height

        if proportion < 1:
            image_width_resize = image_width * proportion
            image_height_resize = image_height * proportion

            new_size = (int(image_width_resize), int(image_height_resize))
            image = image.resize(new_size)

            image_position_x = screen_width / 2 - image_width_resize / 2
            image_position_y = 0

        else:
            image_position_x = screen_width / 2 - image_width / 2
            image_position_y = 0

        image_show = ImageTk.PhotoImage(image)
        label_image = Label(root, image = image_show).place(x=image_position_x, y=image_position_y)

        button_width = 20
        button_height = 5

        select_position_x = screen_width / 2 - button_width / 2 * 8
        select_position_y = screen_height - ((screen_height - max_height) / 2 ) - 100

        next_position_x = select_position_x + button_width * 10
        next_position_y = select_position_y

        previous_position_x = select_position_x - button_width * 10
        previous_position_y = select_position_y

        Previous = Button(root, text="Previous", command=lambda: ckeckear_root(rename_info_list, position - 1, max_position, root),
                          height=button_height, width=button_width).place(x=previous_position_x, y=previous_position_y)
        Select = Button(root, text="Select", command=lambda: image_found(rename_info_list, position, root),
                        height=button_height, width=button_width).place(x=select_position_x, y=select_position_y)
        Next = Button(root, text="Next", command=lambda: ckeckear_root(rename_info_list, position + 1, max_position, root),
                      height=button_height, width=button_width).place(x=next_position_x, y=next_position_y)

        root.mainloop()
    else:
        if position < 0:
            ckeckear_root(rename_info_list, position + 1, max_position, root)
        elif position > max_position:
            ckeckear_root(rename_info_list, position - 1, max_position, root)
        else:
            print("error")

def ckeckear_root(rename_info_list, position, max_position, root):
    if root == None:
        mostrar_imagen(rename_info_list, position, max_position, root)
    else:
        try:
            root.destroy()
            mostrar_imagen(rename_info_list, position, max_position, root)
        except:
            pass

def modo_editar(ventana):
    ventana.destroy()

    folder_padre = os.getcwd()
    folder_input = os.path.join(folder_padre, "LR")
    folder_guardados = os.path.join(folder_padre, "imagenes_finalizados")

    print(folder_input)
    print(image_selected["Filename"])

    name = os.path.split(image_selected["Filename"])[1]

    print(name)
    image_to_move = os.path.join(folder_guardados, name)

    if os.listdir(folder_input) == 0:
        try:
            shutil.move(image_to_move, folder_input)
        except shutil.Error:
            print("error")
    else:
        for file in os.listdir(folder_input):
            path = os.path.join(folder_input, file)
            print(path)
            os.remove(path)
        try:
            shutil.move(image_to_move, folder_input)
        except shutil.Error:
            print("error")

    import Antonio_Wang_Automation_Edit

def modo_search_select(ventana):
    ventana.destroy()
    folder_padre = os.getcwd()
    folder_name = "AntoC_automation"
    folder_finish = "imagenes_finalizados"
    folder_to_finish = os.path.join(folder_padre, folder_finish)
    folder_to_move = os.path.join(folder_padre, folder_name)
    print(folder_to_move)

    info_list = []
    DPIrequerido = True

    productoName = recibirNombreDeProducto()
    crearUnaCarpetaPadre(folder_to_move)

    folder_to_move = updateDir(folder_to_move, productoName)
    crearUnaCarpetaHija(folder_to_move)
    encontrarLinksDeProducto(productoName, folder_to_move)

    format_Filter(folder_to_move)

    all_info_list = extract_features(folder_to_move, info_list)

    dpi_info_list = dpi_Filter(all_info_list, DPIrequerido)
    resolution_info_list = resolution_Filter(dpi_info_list)
    rename_info_list = rename_Filter(resolution_info_list, productoName)

    position = 0
    max_position = len(rename_info_list) - 1
    root = None

    ckeckear_root(rename_info_list, position, max_position, root)

    try:
        shutil.move(image_selected["Filename"], folder_to_finish)
    except:
        print("image already exist")

    main()

main()

