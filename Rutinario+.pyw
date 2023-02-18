import tkinter as tk
from tkinter import messagebox
import random as rd

import pygame
import sounddevice as sd
from scipy.io.wavfile import write
from pygame import *
from functools import partial
import cv2
import csv
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

colors = ["#88F2A2", "#7D7ABF", "#F2C335", "#D93B84", "#F2D649","#60A140"]
pygame.mixer.init()

class Game:
    def __init__(self):
        self.root = root
        self.counter = 3

    def define_element(self, file):
        self.file = file
        with open(self.file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            self.element = list(reader)

    def choose(self):

        self.selected_index = rd.randrange(1, len(self.element))

        return self.element[self.selected_index]

    def listen(self, sound):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    def speaching(self):
        return self.element[self.selected_index]

    def end_screen(self):
        if self.counter < 1:

            self.root.after(2000, lambda: self.go_back())
        else:
            self.root.after(2200, lambda: self.play())


class User:

    def __init__(self):

        self.user_name = ""
        self.user_password = ""
        self.user_stars = 0

    def set_name(self, name):
        self.user_name = name

    def get_name(self):

        return self.user_name

    def give_stars(self, points):

        self.user_stars += points

        df = pd.read_csv("usuarios.csv")

        # Obtiene el índice de la fila que deseas modificar
        index = df[df["name"] == self.user_name].index[0]

        # Asigna un valor a la celda en la columna "stars" de esa fila
        df.at[index, "stars"] = self.user_stars

        # Guarda los cambios en el archivo csv
        df.to_csv("usuarios.csv", index=False)

    def publish_stars(self):

        x = str(self.user_stars) + " puntos"
        return x


class MainScreen:
    def __init__(self, root):
        self.root = root
        self.root.geometry("350x660")

        self.title = tk.Label(self.root, text="RUTINARIO",
                           font=("Fun Blob", 35),fg=colors[5])
        self.title.pack(pady=20)
        self.img_logo = tk.PhotoImage(file="estilo-de-vida.png")
        self.container1 = tk.Frame(self.root)
        self.container1.pack()
        self.logo = ttk.Label(self.container1, image=self.img_logo)
        self.logo.grid(row=0, columnspan=2)
        self.btn_style = ttk.Style()
        self.btn_style.configure("MyButton.TButton", font=("Serif", 12))
        self.login_button = ttk.Button(
            self.container1, text="Iniciar sesión", command=self.login, style="MyButton.TButton")
        self.login_button.grid(row=1, column=0, pady=20)
        self.signup_button = ttk.Button(
            self.container1, text="Registrarse", style="MyButton.TButton", command=self.signup)
        self.signup_button.grid(row=1, column=1, pady=20)

        self.img_exit = tk.PhotoImage(file="off.png")
        self.exit = tk.Button(self.container1, text="Salir",
                           image=self.img_exit, command=self.app_exit)
        self.exit.grid(columnspan=2, row=2, pady=35)
        self.creditos = tk.Button(
            self.container1, text="Créditos", command=self.ir_creditos)
        self.creditos.grid(columnspan=2, row=3, pady=35)

        self.container = tk.Label(self.root)
        self.label_username = tk.Label(self.container, text="Nombre de usuario: ")
        self.entry_username = tk.Entry(self.container)
        self.label_pasword = tk.Label(self.container, text="Ingrese una clave: ")
        self.entry_password = tk.Entry(self.container, show="*")
        self.label_pasword_repeat = tk.Label(
            self.container, text="Repita la clave: ")
        self.entry_password_repeat = tk.Entry(self.container, show="*")
        self.button_signup = ttk.Button(
            self.container, text="Registrarse", command=self.datos_completos, style="MyButton.TButton")
        self.button_login = ttk.Button(self.container, text="Ingresar", command=lambda: self.login_comprobate(
            self.entry_username.get(), self.entry_password.get()), style="MyButton.TButton")
        self.button_back = tk.Button(
            self.container, text="Volver", command=self.volver)

    def login(self):
        self.clean()

        self.title.pack(pady=20)
        self.container1.pack()
        self.logo.grid(row=0, column=0)
        self.container.pack()
        self.label_username.grid(column=0, row=0, pady=10)
        self.entry_username.grid(column=1, row=0, pady=10)
        self.label_pasword.grid(column=0, row=1, pady=10)
        self.entry_password.grid(column=1, row=1, pady=10)
        self.button_login.grid(columnspan=2, row=2, pady=10)
        self.button_back.grid(columnspan=2, row=3)

    def login_comprobate(self, name, clave):
        if self.entry_username.get() and self.entry_password.get():
            df = pd.read_csv("usuarios.csv")
            if name in df['name'].values:
                # Obtener la fila en la que el elemento aparece en la columna "name"
                row = df[df['name'] == name].index[0]
                # Comprobar si la clave coincide con el elemento correspondiente en la misma fila
                if df.at[row, 'clave'] == clave:
                    print("ok")

                    result = df[(df["name"] == name) & (df["clave"] == clave)]

                    current_user.user_stars = int(result["stars"].values[0])

                    current_user.set_name(name)
                    current_user.publish_stars()
                    self.go_to_second_screen()
                    return True
                else:
                    print("El usuario o clave son incorrectos")
                    return False
            else:
                return False

    def signup(self):
        self.clean()

        self.title.pack(pady=20)
        self.container1.pack()
        self.logo.grid(row=0, column=0)
        self.container.pack()

        self.label_username.grid(column=0, row=0, pady=10)
        self.entry_username.grid(column=1, row=0, pady=10)
        self.label_pasword.grid(column=0, row=1, pady=10)
        self.entry_password.grid(column=1, row=1, pady=10)
        self.label_pasword_repeat.grid(column=0, row=2, pady=10)
        self.entry_password_repeat.grid(column=1, row=2, pady=10)
        self.button_signup.grid(columnspan=2, row=3, pady=10)
        self.button_back.grid(columnspan=2, row=4)

    def signup_create(self, name, clave, clave1):
        with open("usuarios.csv", "r") as file:
            reader = csv.reader(file)
            try:
                usuarios = [row[0] for row in reader]

            except IndexError:
                print("El archivo CSV no contiene la columna requerida")
                return False

        if name in usuarios:
            print("El usuario ya existe.")
            self.ventana_aviso("El usuario ya existe.")
            return False

        if clave != clave1:
            print("Las claves no coinciden.")
            self.ventana_aviso("Las claves no coinciden.")
            return False

        with open("usuarios.csv", "a", newline="\n") as file:
            writer = csv.writer(file)
            writer.writerow([name, clave, 0.0])

        print("Usuario creado exitosamente.")

        self.login()

    def ventana_aviso(self, msj):
        self.ventana = tk.Toplevel(self.root)
        self.ventana.geometry("200x100+100+100")
        self.ventana.title("Ventana Emergente")

        self.mensaje = tk.Label(self.ventana, text=msj)
        self.mensaje.pack()
        self.btn_cerrar = tk.Button(
            self.ventana, text="Cerrar", command=self.cerrar)
        self.btn_cerrar.pack()

    def cerrar(self):
        self.ventana.destroy()

    def datos_completos(self):
        if self.entry_username.get() and self.entry_password.get() and self.entry_password_repeat.get():

            self.signup_create(self.entry_username.get(
            ), self.entry_password.get(), self.entry_password_repeat.get())
        else:
            self.ventana_aviso("Hay campos sin completar")

    def clean(self):

        self.title.pack_forget()
        self.login_button.grid_forget()
        self.signup_button.grid_forget()
        self.entry_password.grid_forget()
        self.entry_password_repeat.grid_forget()
        self.entry_username.grid_forget()
        self.label_pasword.grid_forget()
        self.label_pasword_repeat.grid_forget()
        self.label_username.grid_forget()
        self.button_signup.grid_forget()
        self.container.pack_forget()
        self.container1.pack_forget
        self.logo.grid_forget()
        self.button_login.pack_forget()
        self.login_button.pack_forget()
        self.button_back.grid_forget()
        self.logo.grid_forget()
        self.signup_button.grid_forget()
        self.container1.pack_forget()
        self.creditos.grid_forget()
        self.exit.grid_forget()

    def ir_creditos(self):
        self.clean()
        Creditos(self.root)

    def volver(self):
        self.clean()
        MainScreen(root)

    def app_exit(self):
        self.root.destroy()

    def go_to_second_screen(self):
        self.clean()
        MainWindow(self.root)


class Creditos:
    def __init__(self, root):
        self.root = root
        self.credito_title = tk.Label(text="PALABRERO", font=("Fun Blob", 35),fg=colors[5])
        self.credito_title.pack(pady=20)
        self.credito_app = tk.Message(self.root, text=open(
            "credito_app.txt", "r", encoding="UTF-8").read(), bg=colors[4], width=300)
        self.credito_app.pack()
        #self.img_cc = Image.open("cc.png")
        #self.img_cc_tk = ImageTk.PhotoImage(self.img_cc)
        #self.img_label = Label(self.root, image=self.img_cc_tk)
        #self.img_label.pack(pady=20)

        self.credito_exit = tk.Button(
            self.root, text="Volver", command=self.go_back)
        self.credito_exit.pack()

    def clean(self):
        self.credito_title.pack_forget()

        self.credito_app.pack_forget()
        self.credito_exit.pack_forget()
        #self.img_label.pack_forget()

    def go_back(self):
        self.clean()
        MainScreen(root)


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("350x660")
        #self.root.title("Routine App")

        # create routines buttons
        self.wake_up_button = tk.Button(self.root, text="Me despierto", command=self.wake_up)
        self.wake_up_button.pack()

        self.dress_up_button = tk.Button(self.root, text="Me visto", command=self.dress_up)
        self.dress_up_button.pack()

        self.hygiene_button = tk.Button(self.root, text="Me lavo las manos", command=self.hygiene)
        self.hygiene_button.pack()

        self.food_button = tk.Button(self.root, text="Voy a comer", command=self.food)
        self.food_button.pack()
        

    def wake_up(self):
        self.open_routine("Me despierto")

    def dress_up(self):
        self.open_routine("Me visto")


    def hygiene(self):
        self.open_routine("Me lavo las manos")

    def food(self):
        self.open_routine("Voy a comer")


    def open_routine(self, routine):
        self.clean()
        self.steps_window = StepsWindow(self.root, routine)
        
    def clean(self):
        self.wake_up_button.pack_forget()
        self.dress_up_button.pack_forget()
        self.hygiene_button.pack_forget()
        self.food_button.pack_forget()


class StepsWindow:
    def __init__(self, root, routine):
        self.root=root
        self.routine = routine
        self.routin_title=tk.Label(self.root,text=self.routine.upper(),bg="black",fg="white",font=("Comic Sans MS",12))
        self.routin_title.pack(fill="x",pady=15)
        
        self.btn_cerrar=tk.Button(self.root,text="X",command=self.go_back,bg="black",fg="white")
        self.btn_cerrar.place(x=330,y=17)
        self.steps_container=tk.Frame(self.root)
        self.steps_container.pack()
        self.i = 0

        
        
        #self.root.title("Steps")
        
        self.steps = {
            "Me despierto": [
                {
                    "text": "Me despierto",
                    "image": "Images/wake_up.png",
                    "image_sm": "Images_small/wake_up.png",
                    "audio": "Sounds/me despierto.wav"
                },
                {
                    "text": "Salgo de la cama",
                    "image": "Images/get_out_of_bed.png",
                    "image_sm": "Images_small/get_out_of_bed.png",
                    "audio": "Sounds/salgo de la cama.wav"
                },
                {
                    "text": "Cepillo mis dientes",
                    "image": "Images/cepillarsedientes.png",
                    "image_sm": "Images_small/cepillarsedientes.png",
                    "audio": "Sounds/cepillo mis dientes.wav"
                },
                {
                    "text": "Me pongo la ropa",
                    "image": "Images/mevistodearriba.png",
                    "image_sm": "Images_small/mevistodearriba.png",
                    "audio": "Sounds/me pongo la ropa.wav"                    
                }
            ],
            "Me visto": [
                {
                    "text": "Busco la ropa",
                    "image": "Images/buscolaropa.png",
                    "image_sm": "Images_small/buscolaropa.png",
                    "audio": "Sounds/busco la ropa.wav"
                },
                {
                    "text": "Me pongo ropa interior limpia",
                    "image": "Images/ropainteriorlimpia.png",
                    "image_sm": "Images_small/ropainteriorlimpia.png",
                    "audio": "Sounds/me pongo ropa interior limpia.wav"
                },
                {
                    "text": "Me visto la parte de arriba",
                    "image": "Images/mevistodearriba.png",
                    "image_sm": "Images_small/mevistodearriba.png",
                    "audio": "Sounds/me visto la parte de arriba.wav"
                },
                {
                    "text": "Me visto la parte de abajo",
                    "image": "Images/mevistodeabajo.png",
                    "image_sm": "Images_small/mevistodeabajo.png",
                    "audio": "Sounds/me visto la parte de abajo.wav"
                },
                {
                    "text": "Me pongo las zapatillas",
                    "image": "Images/mepongozapatillas.png",
                    "image_sm": "Images_small/mepongozapatillas.png",
                    "audio": "Sounds/me pongo las zapatillas.wav"
                }
            ],
            "Me lavo las manos": [
                {
                    "text": "Abro la canilla",
                    "image": "Images/Abro la canilla.png",
                    "image_sm": "Images_small/Abro la canilla.png",
                    "audio": "Sounds/Abro la canilla.wav"
                },
                {
                    "text": "Me mojo las manos y las enjabono",
                    "image": "Images/Me mojo las manos y las enjabono.png",
                    "image": "Images/Me mojo las manos y las enjabono.png",
                    "image_sm": "Images_small/Me mojo las manos y las enjabono.png",
                    "audio": "Sounds/Me mojo las manos y las enjabono.wav"
                },
                {
                    "text": "Me enjuago",
                    "image": "Images/Me enjuago.png",
                    "image_sm": "Images_small/Me enjuago.png",
                    "audio": "Sounds/Me enjuago.wav"
                },
                {
                    "text": "Cierro la canilla",
                    "image": "Images/Cierro la canilla.png",
                    "image_sm": "Images_small/Cierro la canilla.png",
                    "audio": "Sounds/Cierro la canilla.wav"
                },
                {
                    "text": "Me seco las manos",
                    "image": "Images/Me seco las manos.png",
                    "image_sm": "Images_small/Me seco las manos.png",
                    "audio": "Sounds/Me seco las manos.wav"
                }
            ],
            "Me voy a comer": [
                {
                    "text": "Put on shirt",
                    "image": "Images/put_on_shirt.png",
                    "image_sm": "Image_small/put_on_shirt.png",
                    "audio": "Sounds\put_on_shirt.wav"
                },
                {
                    "text": "Put on pants",
                    "image": "Images/put_on_pants.png",
                    "image_sm": "Image_small/put_on_pants.png",
                    "audio": "Sounds\put_on_pants.wav"
                },
                {
                    "text": "Put on shoes",
                    "image": "Images/put_on_shoes.png",
                    "image_sm": "Image_small/put_on_shoes.png",
                    "audio": "Sounds\put_on_shoes.wav"
                }
            ]
                }  
        self.show_step()
    
    def show_step(self):
        

        # Agrega una lista de imágenes y sonidos para mantener una referencia a cada una
        self.images = []
        self.images_sound=[]
        self.sounds=[]
        self.images_check=[]
        
        
   

        step=self.steps[self.routine][self.i]
            # Crea una nueva instancia de PhotoImage para cada imagen
        image = tk.PhotoImage(file=step["image"])
        self.images.append(image)  # Agrega la imagen a la lista de imágenes
            
        self.step_label = tk.Label(self.steps_container, text=step["text"].upper(),font=("Comic Sans MS",8))
        self.step_label.grid(column=0, row=0)

            # Usa la imagen correspondiente en cada label
        self.image_label = tk.Label(self.steps_container, image=image)
        self.image_label.grid(column=0, row=1,pady=5)

        image_sound = tk.PhotoImage(file="listen1.png")
        self.images_sound.append(image_sound)
            
        sound = pygame.mixer.Sound(step["audio"])
        self.sounds.append(sound)
            

        audio_button = tk.Button(self.steps_container, text="Play Audio", image=image_sound, command=partial(self.play_audio,sound))
        audio_button.grid(column=0, row=2)
                       
        image_check = tk.PhotoImage(file="no-comprobado+.png")
        self.images_check.append(image_check)
  
        self.step_check = tk.Button(self.steps_container, image=image_check, highlightthickness=0, relief="flat", command= self.update_check)
        self.step_check.grid(column=0, row=3,pady=20)
        
            
        self.i+=1          
          

    
    def play_audio(self, audio_file):

        audio_file.play()
        

    def update_check(self):

        
        sound_check = pygame.mixer.Sound("beeps-bonks-boinks 1.mp3")
        self.step_check.config(command="")
        
        sound_check.play()
        self.images_check_ok = tk.PhotoImage(file="comprobado+.png")
        self.step_check.config(image=self.images_check_ok)
        self.root.after(1000,lambda:self.next_page())


    def next_page(self):
        for child in self.steps_container.winfo_children():
            child.grid_forget()
        if self.i == len(self.steps[self.routine]):
            sound_check=pygame.mixer.Sound("beeps-bonks-boinks 5.mp3")
            sound_check.play()
            self.felicitar()
            self.image_next=tk.PhotoImage(file="siguiente.png")
            self.next_step_button = tk.Button(self.steps_container, text="Siguiente rutina", command=self.next_routin,image=self.image_next,border=0)
            self.next_step_button.pack(pady=20) 
            self.go_main_screen_button=tk.Button(self.steps_container,text="Volver",command=self.go_back)
            self.go_main_screen_button.pack(pady=80)

        else:
            self.show_step()
        
    def next_routin(self):
        
        for elem in self.root.winfo_children():
            elem.destroy()
        if self.routine == "Me despierto":
            self.steps_window = StepsWindow(self.root, "Me visto")
        
        else:
            MainWindow(root)
    
    def felicitar(self):
        self.image_a=tk.PhotoImage(file=self.steps[self.routine][0]["image"])
        self.label_congratulations_img=tk.Label(self.steps_container,image=self.image_a)
        self.label_congratulations_img.pack(pady=5)
        self.label_congratulations=tk.Label(self.steps_container,text="¡Felicitaciones!",font=("Comic Sans MS",16),fg="blue")
        self.label_congratulations.pack(pady=5)
    
    def go_back(self):
        self.routin_title.pack_forget()
        self.steps_container.pack_forget()
        self.btn_cerrar.place_forget()
        MainWindow(root)
      
#soy visual
#podría hacer muchas actividades independientes y que aparezcan así o que estén contectadas entre sí por otras funciones mayores


root = tk.Tk()
root.iconbitmap("ico.ico")
root.title("Rutinario")
current_user = User()
#MainScreen(root)
MainWindow(root)
root.mainloop()



