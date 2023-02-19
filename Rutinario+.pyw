import tkinter as tk
from tkinter import filedialog as fd
import pygame
import sounddevice as sd
from scipy.io.wavfile import write
from pygame import *
from functools import partial
import os
import csv
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

colors = ["#F9F8F9", "#91D7F2", "#D96277", "#F2B544", "#0D0D0D"]
pygame.mixer.init()

class User:

    def __init__(self):

        self.user_name = ""
        self.user_password = ""
        self.user_img=""
        
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
    def get_user_img(self):
        if os.path.exists(str("Images_user/"+self.get_name()+".png")):
            self.user_img=tk.PhotoImage(file=str("Images_user/"+self.get_name()+".png"))
        else:
            self.user_img=tk.PhotoImage(file="usuario.png")
    def change_user_img(self):
        # Abrir archivo de imagen
        file_path = fd.askopenfilename()
        
        image = Image.open(file_path)

        # Cambiar tamaño de la imagen a 32x32
        resized_img = image.resize((32, 32))
        
        save_dir="Images_user"
        filename=self.get_name()+".png"
        save_path = os.path.join(save_dir, str(filename))
        resized_img.save(save_path)
        # Convertir imagen para usar en tkinter
        photo = ImageTk.PhotoImage(resized_img)

        # Asignar imagen al atributo user_img
        self.user_img = photo



        
    

class MainScreen:
    def __init__(self, root):
        self.root = root
        self.root.geometry("350x660")
        self.root.configure(bg=colors[0])

        self.title = tk.Label(self.root, text="RUTINARIO",
                           font=("Handrawn Color Kid", 40),fg=colors[3],bg=colors[0])
        self.title.pack(pady=20)
        self.img_logo = tk.PhotoImage(file="estilo-de-vida.png")
        self.container1 = tk.Frame(self.root,bg=colors[0])
        self.container1.pack()
        self.logo = tk.Label(self.container1, image=self.img_logo,bg=colors[0])
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

        self.container = tk.Label(self.root,bg=colors[0])
        self.label_username = tk.Label(self.container, text="Nombre de usuario: ",bg=colors[0])
        self.entry_username = tk.Entry(self.container)
        self.label_pasword = tk.Label(self.container, text="Ingrese una clave: ",bg=colors[0])
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
        self.credito_title = tk.Label(text="RUTINARIO", font=("Handrawn Color Kid", 40),fg=colors[3],bg=colors[0])
        self.credito_title.pack(pady=20)
        self.credito_app = tk.Message(self.root, text=open(
            "credito_app.txt", "r", encoding="UTF-8").read(), bg=colors[2], width=300)
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
        self.root.configure(bg=colors[0])
        #self.root.title("Routine App")
        self.label_box = tk.Frame(self.root,bg=colors[1])
        self.label_box.pack(pady=5)
        self.img_0 = tk.PhotoImage(file="exit.png")
        
        
        self.style = ttk.Style()
        self.style.configure("Label.User.TLabel", width=18, height=3, bg=colors[1])

        current_user.get_user_img()
        self.label_username = ttk.Label(
            self.label_box, text=current_user.get_name(), image=current_user.user_img, compound="left",style="Label.User.TLabel")
        
        
        self.label_username.bind("<Button-1>",self.new_user_img)
        
        self.label_stars = tk.Label(
            self.label_box, text=current_user.publish_stars(), width=20, height=3, bg=colors[1])

        self.log_out = tk.Button(
            self.label_box, image=self.img_0,command=self.exit)

        self.label_username.grid(column=0, row=0)
        self.label_stars.grid(column=1, row=0)
        self.log_out.grid(column=2, row=0)
        # create routines buttons
        
        self.btn_box=tk.Frame(self.root,bg=colors[0])
        self.btn_box.pack()
        self.img_enmicasa=tk.PhotoImage(file="Images_btn/enmicasa(1).png")
        self.img_enlaescuela=tk.PhotoImage(file="Images_btn/enlaescuela(1).png")
        self.img_medespierto=tk.PhotoImage(file="Images_btn/wake_up(1).png")
        self.img_mevisto=tk.PhotoImage(file="Images_btn/buscolaropa(1).png")
        self.img_melavolasmanos=tk.PhotoImage(file="Images_btn/Me enjabono las manos(1).png")
        self.img_voyacomer=tk.PhotoImage(file="Images_btn/voyacomer(1).png")
        
        self.enmicasa_button = ttk.Button(self.btn_box, text="En mi casa", image=self.img_enmicasa,compound="left",width=100,command=self.en_mi_casa)
        self.enmicasa_button.pack()
        self.enlaescuela_button = ttk.Button(self.btn_box, text="En la escuela", image=self.img_enlaescuela,compound="left",width=100,command=self.en_la_escuela)
        self.enlaescuela_button.pack()
    
    def new_user_img(self,event):
        current_user.change_user_img()
        self.clean()
        MainWindow(root)    
    
    def en_mi_casa(self):
        self.clean_btn()
        self.wake_up_button = ttk.Button(self.btn_box, text="Me despierto", image=self.img_medespierto,compound="left",width=100,command=self.wake_up)
        self.wake_up_button.pack()

        self.dress_up_button = ttk.Button(self.btn_box, text="Me visto", image=self.img_mevisto,compound="left",width=100,command=self.dress_up)
        self.dress_up_button.pack()

        self.hygiene_button = ttk.Button(self.btn_box, text="Me lavo las manos", image=self.img_melavolasmanos,compound="left",width=100,command=self.hygiene)
        self.hygiene_button.pack()
        
        self.food_button = ttk.Button(self.btn_box, text="Voy a comer", image=self.img_voyacomer,compound="left",width=100, command=self.food)
        self.food_button.pack()


        self.btn_volver=ttk.Button(self.btn_box,text="Volver",command=self.volver_pantalla)
        self.btn_volver.pack()
    def en_la_escuela(self):
        self.clean_btn()
        self.hygiene_button = ttk.Button(self.btn_box, text="Me lavo las manos", image=self.img_melavolasmanos,compound="left",width=100,command=self.hygiene)
        self.hygiene_button.pack()

        self.btn_volver=ttk.Button(self.btn_box,text="Volver",command=self.volver_pantalla)
        self.btn_volver.pack()
        pass
    
    def exit(self):

  
        self.label_box.pack_forget()
        self.btn_box.pack_forget()
        MainScreen(self.root)    

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
        self.btn_box.pack_forget()
        self.label_box.pack_forget()
    
    def clean_btn(self):
        for child in self.btn_box.winfo_children():
            child.pack_forget()   
        for child in self.label_box.winfo_children():
            child.pack_forget() 

    def volver_pantalla(self):
        self.clean()
        MainWindow(root)

class StepsWindow:
    def __init__(self, root, routine):
        self.root=root
        self.root.configure(bg=colors[0])
        self.routine = routine
        self.routin_title=tk.Label(self.root,text=self.routine.upper(),bg="black",fg="white",font=("Comic Sans MS",12))
        self.routin_title.pack(fill="x",pady=15)
        
        self.btn_cerrar=tk.Button(self.root,text="X",command=self.go_back,bg="black",fg="white")
        self.btn_cerrar.place(x=330,y=17)
        self.steps_container=tk.Frame(self.root,bg=colors[0])
        self.steps_container.pack()
        self.i = 0
        self.progressbar_value=0
        self.progressbar = ttk.Progressbar(self.steps_container, orient="horizontal", length=300, mode="determinate",value=self.progressbar_value)
        
        
        #self.root.title("Steps")
        
        self.steps = {
            "Me despierto": [
                {
                    "text": "Me despierto",
                    "image": "Images/wake_up.png",
                    "ico_btn": "Images_btn/wake_up.png",
                    "audio": "Sounds/me despierto.wav"
                },
                {
                    "text": "Salgo de la cama",
                    "image": "Images/get_out_of_bed.png",
                    "audio": "Sounds/salgo de la cama.wav"
                },
                {
                    "text": "Cepillo mis dientes",
                    "image": "Images/cepillarsedientes.png",
                    "audio": "Sounds/cepillo mis dientes.wav"
                },
                {
                    "text": "Me pongo la ropa",
                    "image": "Images/mevistodearriba.png",
                    "audio": "Sounds/me pongo la ropa.wav"                    
                }
            ],
            "Me visto": [
                {
                    "text": "Busco la ropa",
                    "image": "Images/buscolaropa.png",
                    "ico_btn": "Images_btn/buscolaropa.png",
                    "audio": "Sounds/busco la ropa.wav"
                },
                {
                    "text": "Me pongo ropa interior limpia",
                    "image": "Images/ropainteriorlimpia.png",
                    "audio": "Sounds/me pongo ropa interior limpia.wav"
                },
                {
                    "text": "Me visto la parte de arriba",
                    "image": "Images/mevistodearriba.png",
                    "audio": "Sounds/me visto la parte de arriba.wav"
                },
                {
                    "text": "Me visto la parte de abajo",
                    "image": "Images/mevistodeabajo.png",
                    "audio": "Sounds/me visto la parte de abajo.wav"
                },
                {
                    "text": "Me pongo las zapatillas",
                    "image": "Images/mepongozapatillas.png",
                    "audio": "Sounds/me pongo las zapatillas.wav"
                }
            ],
            "Me lavo las manos": [
                {
                    "text": "Abro la canilla",
                    "image": "Images/Abro la canilla.png",
                    "ico_btn": "Images_btn/Me enjabono las manos.png",
                    "audio": "Sounds/Abro la canilla.wav"
                },
                {
                    "text": "Me mojo las manos",
                    "image": "Images/Me enjuago.png",
                    "audio": "Sounds/Me mojo las manos.wav"
                },
                {
                    "text": "Me enjabono las manos",
                    "image": "Images/Me enjabono las manos.png",
                    "audio": "Sounds/Me mojo las manos y las enjabono.wav"
                },
                {
                    "text": "Me enjuago",
                    "image": "Images/Me enjuago.png",
                    "audio": "Sounds/Me enjuago.wav"
                },
                {
                    "text": "Cierro la canilla",
                    "image": "Images/Cierro la canilla.png",
                    "audio": "Sounds/Cierro la canilla.wav"
                },
                {
                    "text": "Me seco las manos",
                    "image": "Images/Me seco las manos.png",
                    "audio": "Sounds/Me seco las manos.wav"
                }
            ],
            "Voy a comer": [
                {
                    "text": "Me lavo las manos",
                    "image": "Images/Me enjabono las manos.png",
                    "ico_btn": "Images_btn/voyacomer.png",
                    "audio": "Sounds\Me lavo las manos.wav"
                },
                {
                    "text": "Me siento a la mesa",
                    "image": "Images/sentarse a la mesa.png",
                    "audio": "Sounds\me siento a la mesa.wav"
                },
                {
                    "text": "Elijo la comida",
                    "image": "Images/elijo la comida.png",
                    "audio": "Sounds/elijo la comida.wav"
                },
                {
                    "text": "Uso los cubiertos para comer",
                    "image": "Images/uso los cubiertos.png",
                    "audio": "Sounds/uso los cubiertos para comer.wav"
                },
                {
                    "text": "Como con traquilidad",
                    "image": "Images/como tranquilo.png",
                    "audio": "Sounds/como con tranquilidad.wav"
                },
                {
                    "text": "Limpio y recojo mis cosas",
                    "image": "Images/limpio y recojo mis cosas.png",
                    "audio": "Sounds/limpio y recojo mis cosas.wav"
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
            
        self.step_label = tk.Label(self.steps_container, text=step["text"].upper(),font=("Comic Sans MS",8),bg=colors[0])
        self.step_label.grid(column=0, row=0)

            # Usa la imagen correspondiente en cada label
        self.image_label = tk.Label(self.steps_container, image=image,bg=colors[0])
        self.image_label.grid(column=0, row=1,pady=5)
        
        self.image_label.bind("<Button-1>",lambda event:self.play_audio_b(event,sound))

        image_sound = tk.PhotoImage(file="listen1.png")
        self.images_sound.append(image_sound)
            
        sound = pygame.mixer.Sound(step["audio"])
        self.sounds.append(sound)
            

        # audio_button = tk.Button(self.steps_container, text="Play Audio", image=image_sound, bd=0,command=partial(self.play_audio,sound),bg=colors[0])
        # audio_button.grid(column=0, row=2)
                       
        image_check = tk.PhotoImage(file="no-comprobado+.png")
        self.images_check.append(image_check)
  
        self.step_check = tk.Button(self.steps_container, image=image_check, highlightthickness=0, relief="flat", width=150,command= self.update_check,bg=colors[0])
        self.step_check.grid(column=0, row=3,pady=20)
        
        self.play_audio(sound)
        self.progressbar.grid(column=0,row=4,pady=120)
        
        
            
        self.i+=1          
          

    
    def play_audio(self, audio_file):

        audio_file.play()
    def play_audio_b(self, event,audio_file):

        audio_file.play()
        

    def update_check(self):

        
        sound_check = pygame.mixer.Sound("beeps-bonks-boinks 1.mp3")
        self.step_check.config(command="")
        
        sound_check.play()
        self.images_check_ok = tk.PhotoImage(file="comprobado+.png")
        self.step_check.config(image=self.images_check_ok)
        self.barra_progreso(100/len(self.steps[self.routine]))
        self.root.after(1000,lambda:self.next_page())


    def next_page(self):
        for child in self.steps_container.winfo_children():
            child.grid_forget()
        if self.i == len(self.steps[self.routine]):
            sound_check=pygame.mixer.Sound("beeps-bonks-boinks 5.mp3")
            sound_check.play()
            self.felicitar()
            self.image_next=tk.PhotoImage(file="siguiente.png")
            self.next_step_button = tk.Button(self.steps_container, text="Siguiente rutina", command=self.next_routin,image=self.image_next,border=0,bg=colors[0])
            self.next_step_button.pack(pady=20) 
            self.go_main_screen_button=tk.Button(self.steps_container,text="Volver",command=self.go_back)
            self.go_main_screen_button.pack(pady=60)

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
        self.image_a=tk.PhotoImage(file=self.steps[self.routine][0]["ico_btn"])
        self.label_congratulations_img=tk.Label(self.steps_container,image=self.image_a,bg=colors[0])
        self.label_congratulations_img.pack(pady=5)
        self.label_congratulations=tk.Label(self.steps_container,text="¡Felicitaciones!",font=("Comic Sans MS",22,"bold"),fg=colors[2],bg=colors[0])
        self.label_congratulations.pack(pady=5)
        current_user.give_stars(10)
    
    def barra_progreso(self,z):
        self.progressbar_value=z        
        self.progressbar["value"]+=self.progressbar_value
        self.steps_container.update_idletasks()
        
    
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
MainScreen(root)

root.mainloop()



