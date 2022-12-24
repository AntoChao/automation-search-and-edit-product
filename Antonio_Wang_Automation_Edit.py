"""
1- input = 1 photo
2- Ofrecer diferentes funcionalidades
    1- scratch the image and transform to png
    2- Mejor Calidad
    3- ReLighting
    4- Sacar Waterproof
"""

import os
from tkinter import *
from PIL import Image, ImageTk
import requests
import shutil


#2-0
def move_file_background(image_name, image_path):
    folder_output = os.getcwd()
    image_output = os.path.join(folder_output, image_name)

    original_name_withExtension = os.path.split(image_path)[1]
    original_name_noExtension = os.path.splitext(original_name_withExtension)[0].lower()

    image_output_rename = "{}{}{}{}{}".format(folder_output, "\\", original_name_noExtension, " no bg", ".png")

    os.rename(image_output, image_output_rename)

    folder_finalizados = "imagenes_finalizados"
    folder_to_move = os.path.join(folder_output, folder_finalizados)

    try:
        shutil.move(image_output_rename, folder_to_move)
    except shutil.Error:
        print("image already exist")


#2-1
#https://www.remove.bg/tools-api
def remove_background(image_path):
    try:
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(image_path, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': 'Your_API_Key'},
        )

        if response.status_code == requests.codes.ok:
            with open('no-bg.png', 'wb') as out:
                out.write(response.content)
        else:
            print("Error:", response.status_code, response.text)
        move_file_background('no-bg.png', image_path)
    except:
        print("error")

#2-2
def super_resolution(image_path):
    #mandar la imagen a la direccion
    folder_padre = os.getcwd()
    print(folder_padre)

    folder_input = os.path.join(folder_padre, "LR")
    folder_output = os.path.join(folder_padre, "results")

    try:
        shutil.move(image_path, folder_input)
    except shutil.Error:
        print("image already exist")

    try:
        import test #call super resolution
    except:
        print("gpu no suf memoria")

    folder_finalizados = "imagenes_finalizados"
    folder_to_move = os.path.join(folder_padre, folder_finalizados)

    for imagen in os.listdir(folder_output):
        try:
            imagen_direccion = os.path.join(folder_output, imagen)
            shutil.move(imagen_direccion, folder_to_move)
        except:
            print("image already exist")
    print("finish super resolution")

def main():
    image_direction = os.getcwd()
    image_LR = "LR"

    folder_finalizados = "imagenes_finalizados"
    folder_miau = os.path.join(image_direction, folder_finalizados)

    image_folder_edit = os.path.join(image_direction, image_LR)
    list_check = []

    for image in os.listdir(image_folder_edit):
        image_path = os.path.join(image_folder_edit, image)
        list_check.append(image_path)

    if len(list_check) == 1:
        root = Tk()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        screen_size = "{}{}{}".format(screen_width, "x", screen_height)

        root.geometry(screen_size)
        root.title("Edit")

        max_weidth = screen_width / 3 * 2

        image = Image.open(image_path)
        image_width = image.width
        image_height = image.height

        proportion = max_weidth / screen_width

        if proportion < 1:
            image_width_resize = image_width * proportion
            image_height_resize = image_height * proportion

            new_size = (int(image_width_resize), int(image_height_resize))
            image = image.resize(new_size)

            image_position_x = 0
            image_position_y = screen_height / 2 - image_height_resize / 2

        else:
            image_position_x = 0
            image_position_y = screen_height / 2 - image_height / 2

        image_show = ImageTk.PhotoImage(image)
        label_image = Label(root, image=image_show)
        label_image.place(x=image_position_x, y=image_position_y)


        button_width = 20
        button_height = 5

        super_resolution_x = screen_width - (screen_width - max_weidth)
        super_resolution_y = screen_height/5*2 - 100

        remove_background_x = screen_width - (screen_width - max_weidth)
        remove_background_y = screen_height/5*4 - 100

        quit_x = screen_width - button_width * 8
        quit_y = 0

        Super_resolution = Button(root, text="Super Resolution", command=lambda: super_resolution(image_path), height=button_height, width=button_width)
        Super_resolution.place(x=super_resolution_x, y=super_resolution_y)
        Remove_background = Button(root, text="Remove Background", command=lambda: remove_background(image_path), height=button_height, width=button_width)
        Remove_background.place(x=remove_background_x, y=remove_background_y)
        Quit = Button(root, text="Quit", command= root.destroy, height=button_height, width=button_width)
        Quit.place(x=quit_x, y=quit_y)

        root.mainloop()

        for image in os.listdir(image_folder_edit):
            image_eliminar = os.path.join(image_folder_edit, image)
            try:
                shutil.move(image_eliminar, folder_miau)
            except:
                print("image already exist")

    else:
        print("el input es incorrecto")

main()
