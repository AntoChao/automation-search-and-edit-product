"""
object
    Se trata de automaticamente encontrar la imagen que pide usuario, y ofrecer varias funciones, puede ser mejorar la calidad, sacar waterproof...
"""
import os
import wget
from serpapi import GoogleSearch
from tkinter import *
from PIL import Image, ImageTk
import shutil


GoogleSearch.SERP_API_KEY = "Your_serpapi_api_key"
producto_nombre = ""
dpi_limit = 0
width_limit = 0
height_limit = 0
image_selected = {
                    "Filedir": None,
                    "Filename": None,
                    "Image DPI": None,
                    "Image Height": None,
                    "Image Width": None,
                    "Image Format": None,
                    "Image Mode": None
                }
fue_seleccionado = False

# to improve:
#   1- do multiprocess to act like a clock for google search
#   2- google search method to let the searching more p

def main():
    limpiar_tmp_file()
    menu_principal()

#0-1
def crearUnaCarpetaPadre(dir):
    if not(os.path.isdir(dir)):
        os.mkdir(dir)

#1-1
def recibirNombreDeProducto():
    productoName = input("input the product name: ")
    return productoName

#2-1
def encontrarLinksDeProducto(productoName, dir):
    search = GoogleSearch({"q": productoName, "tbm": "isch"})
    for image_result in search.get_dict()['images_results']:
        link = image_result["original"]
        try:
            transformarLinkAImagen(link, dir)
        except:
            print("error")
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
def dpi_Filter(all_info_list):
    if int(dpi_limit) != 0:
        new_list = []
        print("dpi filter")
        for file in all_info_list:
            file_path = file_path_shortcut(file)
            if "Image DPI" in file:
                if file["Image DPI"][0] > int(dpi_limit):
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
        if file["Image Height"] > height_limit and file["Image Width"] > width_limit:
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

def menu_principal():
    ventana = Tk()

    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    screen_size = "{}{}{}".format(screen_width, "x", screen_height)

    ventana.geometry(screen_size)
    ventana.title("Choose mode")

    button_width = 20
    button_height = 5

    search_select_x = screen_width / 4 * 1 - button_width
    search_select_y = screen_height / 2 - button_height * 4

    edit_x = screen_width / 4 * 3 - button_width
    edit_y = search_select_y

    quit_x = screen_width - button_width * 8
    quit_y = 0

    search_select_botton = Button(ventana, text="search select mode ", command=lambda: modo_search_select(ventana),
                                  height=button_height, width=button_width)
    search_select_botton.place(x=search_select_x, y=search_select_y)
    edit_botton = Button(ventana, text="edit modo", command=lambda: modo_editar(ventana),
                         height=button_height, width=button_width)
    edit_botton.place(x=edit_x, y=edit_y)
    Quit = Button(ventana, text="Quit", command=ventana.destroy, height=button_height, width=button_width)
    Quit.place(x=quit_x, y=quit_y)

    ventana.mainloop()

def modo_editar(ventana):
    ventana.destroy()

    if fue_seleccionado:
        folder_padre = os.getcwd()
        folder_input = os.path.join(folder_padre, "LR")
        folder_guardados = os.path.join(folder_padre, "imagenes_finalizados")

        name = os.path.split(image_selected["Filename"])[1]

        image_to_move = os.path.join(folder_guardados, name)

        if os.listdir(folder_input) == 0:
            try:
                shutil.move(image_to_move, folder_input)
            except shutil.Error:
                print("error")
        else:
            for file in os.listdir(folder_input):
                path = os.path.join(folder_input, file)
                os.remove(path)
            try:
                shutil.move(image_to_move, folder_input)
            except shutil.Error:
                print("error")

        print(1)
        import Antonio_Wang_Automation_Edit
    else:
        print(2)
        import Antonio_Wang_Automation_Edit

def modo_search_select(ventana):
    ventana.destroy()
    folder_padre = os.getcwd()
    folder_name = "AntoC_automation"
    folder_finish = "imagenes_finalizados"
    folder_to_finish = os.path.join(folder_padre, folder_finish)
    folder_to_move = os.path.join(folder_padre, folder_name)

    info_list = []

    menu_ingresar_datos()

    productoName = producto_nombre
    crearUnaCarpetaPadre(folder_to_move)

    folder_to_move = updateDir(folder_to_move, productoName)
    crearUnaCarpetaHija(folder_to_move)

    encontrarLinksDeProducto(productoName, folder_to_move)

    format_Filter(folder_to_move)

    all_info_list = extract_features(folder_to_move, info_list)

    dpi_info_list = dpi_Filter(all_info_list)
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

    global fue_seleccionado
    fue_seleccionado = True

    menu_principal()

def limpiar_tmp_file():
    path_padre = os.getcwd()
    for file in path_padre:
        path_file = os.path.join(path_padre, file)
        extention = os.path.splitext(file)
        if extention == ".tmp":
            os.remove(path_file)
        else:
            pass

def aparecer_el_input(Dpi_limit, entry_x, dpi_y):
    Dpi_limit.place(x=entry_x, y=dpi_y)

def recibir_valores(ventana_ingreso, Producto_name, Dpi_limit, Width_limit, Height_limit):
    global producto_nombre
    global dpi_limit
    global height_limit
    global width_limit
    producto_nombre = Producto_name.get()
    dpi_limit_miau = Dpi_limit.get()
    try:
        dpi_limit = int(dpi_limit_miau)
    except:
        dpi_limit = 0

    width_limit_miau = Width_limit.get()
    width_limit = int(width_limit_miau)
    height_limit_miau = Height_limit.get()
    height_limit = int(height_limit_miau)

    ventana_ingreso.destroy()

def menu_ingresar_datos():
    ventana_ingreso = Tk()

    screen_width = ventana_ingreso.winfo_screenwidth()
    screen_height = ventana_ingreso.winfo_screenheight()

    screen_size = "{}{}{}".format(screen_width, "x", screen_height)

    ventana_ingreso.geometry(screen_size)
    ventana_ingreso.title("input information")

    button_width = 20
    button_height = 5

    label_x = screen_width / 4 * 1
    entry_x = screen_width / 4 * 3

    dpi_yes = entry_x - button_width * 8
    dpi_no = entry_x + button_width * 8

    product_y = screen_height / 6 * 1
    width_y = screen_height / 6 * 2
    height_y = screen_height / 6 * 3
    dpi_YoN_y = screen_height / 6 * 4
    dpi_y = screen_height / 6 * 5

    listo_x = screen_width - button_width * 8
    listo_y = screen_height - button_height - 120

    quit_x = screen_width - button_width * 8
    quit_y = 0

    Label_Product = Label(ventana_ingreso, text="Ingrese nombre de producto: ", font=(25))
    Label_Product.place(x = label_x, y= product_y)
    Label_Width = Label(ventana_ingreso, text="Ingrese width: ", font=(25))
    Label_Width.place(x = label_x, y = width_y)
    Label_Height = Label(ventana_ingreso, text="Ingrese height: ", font=(25))
    Label_Height.place(x = label_x, y= height_y)
    Label_DPI = Label(ventana_ingreso, text="Ingrese DPI: ", font=(25))
    Label_DPI.place(x= label_x, y=dpi_YoN_y)

    Producto_name = Entry(ventana_ingreso, font=(25))
    Producto_name.place(x=entry_x, y=product_y)

    Width_limit = Entry(ventana_ingreso, font=(25))
    Width_limit.place(x=entry_x, y=width_y)

    Height_limit = Entry(ventana_ingreso, font=(25))
    Height_limit.place(x=entry_x, y=height_y)

    Dpi_limit = Entry(ventana_ingreso, font=(25))

    button_dpi_yes = Button(ventana_ingreso, text="yes, existe dpi limit", command = lambda : aparecer_el_input(Dpi_limit, entry_x, dpi_y), height=button_height, width=button_width)
    button_dpi_yes.place(x=dpi_yes, y=dpi_YoN_y)
    button_dpi_no = Button(ventana_ingreso, text="no, no necesito dpi", command=None, height=button_height, width=button_width)
    button_dpi_no.place(x=dpi_no, y=dpi_YoN_y)
    button_listo = Button(ventana_ingreso, text="dale, ingresa valores", command= lambda : recibir_valores(ventana_ingreso, Producto_name, Dpi_limit, Width_limit, Height_limit), height=button_height, width=button_width)
    button_listo.place(x=listo_x, y=listo_y)

    Quit = Button(ventana_ingreso, text="Quit", command=ventana_ingreso.destroy, height=button_height, width=button_width)
    Quit.place(x=quit_x, y=quit_y)

    mainloop()

main()
