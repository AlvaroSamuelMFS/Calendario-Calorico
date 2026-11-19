import tkinter

import customtkinter
import customtkinter as ctk
from customtkinter import CTk, CTkToplevel, CTkFrame

import database
import menuPrincipal
from database import crear_tabla, crear_usuario, verificar_usuario, inicio_sesion,crear_tabla_alimentos
from database import verificar_usuario, crear_usuario
from CTkMessagebox import CTkMessagebox
from datetime import date, datetime
from menuPrincipal import MenuPrincipal


class Inicio(ctk.CTk):

    #Creacion de la ventana de inicio de la aplicacion
    def __init__(self):
        super().__init__()
        self.title("Calendario de Comidas")
        self.geometry("600x400")
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=4)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=2)

        #Creacion del Label de titulo de la aplicacion y los dos botones de iniciar sesion y registrarse
        labelTitulo = ctk.CTkLabel(master=self, text="Calendario de Comidas",font=("Arial", 30),)
        labelTitulo.grid(row=0, column=0, columnspan=2, sticky="nsew")
        button1 = ctk.CTkButton(master=self, text="Crear Cuenta", font=("Arial",20),height=50, width=200, command=self.boton1, border_width=1)
        button1.grid(row=1, column=0, sticky="e",  padx=20)
        button2 = ctk.CTkButton(master=self, text="Iniciar Sesion", font=("Arial",20),height=50,width=200, command=self.boton2, border_width=1)
        button2.grid(row=1, column=1, sticky="w", padx=20)

    def boton1(self):
        # Crea ventana toplevel para introducir datos de creación de cuenta
        crearCuenta = CTkToplevel(self)
        crearCuenta.title("Crear Cuenta")
        crearCuenta.geometry("400x450")
        crearCuenta.maxsize(400, 450)
        crearCuenta.minsize(400, 450)
        crearCuenta.grid_columnconfigure(0, weight=1)

        # Creacion del Frame uno que contiene para introducir el nombre y contraseña del usuario
        frame1 = CTkFrame(crearCuenta, fg_color="transparent")
        frame1.grid_rowconfigure(0, weight=1)
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_columnconfigure(1, weight=10)
        frame1.grid(row=0, column=0, pady=20, sticky="nsew")
        labelNombre = ctk.CTkLabel(master=frame1, text="Nombre: ", font=("Arial", 14))
        labelNombre.grid(row=0, column=0, sticky="nsw")
        textBoxNombre = ctk.CTkEntry(master=frame1, border_width=2, width=250, height=30, font=("Arial", 14))
        textBoxNombre.grid(row=1, column=0, sticky="nsw")
        labelContrasena = ctk.CTkLabel(master=frame1, text="Contraseña: ", font=("Arial", 14))
        labelContrasena.grid(row=2, column=0, sticky="nsw")
        textBoxContrasena = ctk.CTkEntry(master=frame1, border_width=2, width=250, height=30, font=("Arial", 14), show="*")
        textBoxContrasena.grid(row=3, column=0, sticky="nsw")
        def ver_contrasena():
            if checkboxContrasena.get() == 1:
                textBoxContrasena.configure(show="")
            elif checkboxContrasena.get() == 2:
                textBoxContrasena.configure(show="*")
        checkboxContrasena = ctk.CTkCheckBox(master=frame1, onvalue=1,offvalue=2,command=ver_contrasena, text="", border_width=2,width=5,
                                             height=5)
        checkboxContrasena.grid(row=3, column=1,sticky="nsw")

        # Creacion del Frame 2 para introducir peso, altura, edad y sexo del usuario
        frame2 = CTkFrame(crearCuenta, fg_color="transparent")
        frame2.grid_rowconfigure(0, weight=2)
        frame2.grid_rowconfigure(1, weight=2)
        frame2.grid_rowconfigure(2, weight=2)
        frame2.grid_rowconfigure(3, weight=2)
        frame2.grid_columnconfigure(0, weight=2)
        frame2.grid_columnconfigure(1, weight=2)
        frame2.grid(row=1, column=0, sticky="nsew")
        labelPeso = ctk.CTkLabel(master=frame2, text="Peso: ", font=("Arial", 14))
        labelPeso.grid(row=0, column=0, sticky="nsw")
        entryPeso = ctk.CTkEntry(frame2)
        entryPeso.grid(row=1, column=0, sticky="nsw")
        labelAltura = ctk.CTkLabel(master=frame2, text="Altura: ", font=("Arial", 14))
        labelAltura.grid(row=2, column=0, sticky="nsw")
        entryAltura = ctk.CTkEntry(frame2)
        entryAltura.grid(row=3, column=0, sticky="nsw")
        labelEdad = ctk.CTkLabel(master=frame2, text="Fecha de Nacimiento: ", font=("Arial", 14))
        labelEdad.grid(row=0, column=1, sticky="nsw")
        frameEdad = ctk.CTkFrame(frame2,width=210,height=20,fg_color="transparent")
        frameEdad.grid(row=1, column=1, sticky="nsw")
        frameEdad.grid_propagate(False)
        entryDia = ctk.CTkEntry(frameEdad,width=70,height=22,placeholder_text="Dia")
        entryDia.grid(row=0, column=0, sticky="nsw")
        entryMes = ctk.CTkEntry(frameEdad,width=70,height=22,placeholder_text="Mes")
        entryMes.grid(row=0, column=1, sticky="nsw")
        entryAño = ctk.CTkEntry(frameEdad,width=70,height=22,placeholder_text="Año")
        entryAño.grid(row=0, column=2, sticky="nsw")
        labelSexo = ctk.CTkLabel(master=frame2, text="Sexo: ", font=("Arial", 14))
        labelSexo.grid(row=2, column=1, sticky="nsw")
        frameSexo = CTkFrame(frame2, height=20, fg_color="transparent")
        frameSexo.grid(row=3, column=1, sticky="nsw")
        radio_sexo = tkinter.IntVar(value=0)
        radioB1 = ctk.CTkRadioButton(frameSexo, text="M", variable=radio_sexo, value=1)
        radioB1.grid(row=0, column=0, sticky="nsw")
        radioB2 = ctk.CTkRadioButton(frameSexo, text="F", variable=radio_sexo, value=2)
        radioB2.grid(row=0, column=1, sticky="nsw")

        # Creacion del Frame 3 para la introduccion de la cantidad de actividad y el objetivo del usuario
        frame3 = CTkFrame(crearCuenta, fg_color="transparent")
        frame3.grid(row=2, column=0, pady=20, sticky="nsew")
        labelActividad = ctk.CTkLabel(master=frame3, text="Cantidad de Actividad", font=("Arial", 14))
        labelActividad.grid(row=0, column=0, sticky="nsw")
        frameActividad = CTkFrame(master=frame3, height=20, fg_color="transparent")
        frameActividad.grid(row=1, column=0, pady=5, sticky="nsw")
        labelSlider = ctk.CTkLabel(master=frameActividad, text="Actividad Moderada", font=("Arial", 12))
        labelSlider.grid(row=1, column=0, sticky="nsew")

        # Funcion para que el label del slider cambie segun en que posicion se encuentra el slider
        def cambioSlider(value):
            if value == 1:
                labelSlider.configure(text="Sedentario")
            elif value == 2:
                labelSlider.configure(text="Poca Actividad")
            elif value == 3:
                labelSlider.configure(text="Actividad Moderada")
            elif value == 4:
                labelSlider.configure(text="Bastante Actividad")
            elif value == 5:
                labelSlider.configure(text="Mucha Actividad")
        slider = customtkinter.CTkSlider(frameActividad, from_=1, to=5, number_of_steps=4, command=cambioSlider,
                                         width=190)
        slider.grid(row=0, column=0, sticky="nsw")
        labelObjetivo = ctk.CTkLabel(master=frame3, text="Objetivo", font=("Arial", 14))
        labelObjetivo.grid(row=0, column=1, sticky="nsw")
        frameObjetivo = CTkFrame(frame3, height=20, fg_color="transparent")
        frameObjetivo.grid(row=1, column=1, sticky="nsw")
        radio_objetivo = tkinter.IntVar(value=0)
        radioB3 = ctk.CTkRadioButton(frameObjetivo, text="Tonificar", variable=radio_objetivo, value=1)
        radioB3.grid(row=0, column=0, sticky="nsw")
        radioB4 = ctk.CTkRadioButton(frameObjetivo, text="Adelgazar", variable=radio_objetivo, value=2)
        radioB4.grid(row=0, column=1, sticky="nsw")
        # Creacion del Frame 4, para el boton de Aceptar que pasara a analizar los datos introducidos para crear el usuario
        frame4 = CTkFrame(crearCuenta, fg_color="transparent")
        frame4.grid(row=3, column=0, pady=20, sticky="nsew")
        frame4.grid_columnconfigure(0, weight=2)
        frame4.grid_columnconfigure(1, weight=2)
        def crearUsuario():
            nombre = textBoxNombre.get()
            contrasena = textBoxContrasena.get()
            if not nombre or not contrasena:
                CTkMessagebox(title="Error", message="Nombre o Apellido no introducidos", icon="cancel")
                return
            peso = entryPeso.get()
            altura = entryAltura.get()
            sexo = ""
            match radio_sexo.get():
                case 1:
                    sexo = "M"
                case 2:
                    sexo = "F"

            dia = entryDia.get()
            mes=entryMes.get()
            año = entryAño.get()
            actividad = slider.get()
            objetivo = ""
            match radio_objetivo.get():
                case 1:
                    objetivo = "tonificar"
                case 2:
                    objetivo = "adelgazar"
            if not peso or not altura  or not sexo or not objetivo or not dia or not mes or not año:
                CTkMessagebox(title="Error", message="Faltan Datos Por Introducir", icon="cancel")
            elif not peso.isnumeric() or not altura.isnumeric() or not dia.isnumeric() or not mes.isnumeric() or not año.isnumeric():
                CTkMessagebox(title="Error", message="Datos Introducidos En Formato Erroneo", icon="cancel")
            elif not 1 <= int(dia) <= 31 or not 1 <= int(mes) <= 12 or not 1900 <= int(año) <= int(date.today().year):
                print(dia,mes,año)
                CTkMessagebox(title="Error", message="Datos Mal introducidos", icon="cancel")
            else:

                if verificar_usuario(nombre):
                    crear_tabla()
                    crear_tabla_alimentos()
                    crear_usuario(nombre,contrasena,peso,altura,dia,mes,año,sexo,actividad,objetivo)
                    id = inicio_sesion(nombre, contrasena)
                    if id >= 0:
                        resultado = database.datos_usuario(nombre)
                        msg = CTkMessagebox(title="Sesion Iniciada", message=f"Bienvenido {nombre}", icon="check")
                        if msg.get() == "OK":
                            crear_tabla()
                            crear_tabla_alimentos()
                            crearCuenta.destroy()
                            menu_principal = MenuPrincipal(resultado, id, self)
                            self.after(100, lambda: [self.withdraw(), menu_principal.mainloop()])

                else:
                    CTkMessagebox(title="Error", message="El usuario ya existe", icon="cancel")

        buttonAceptar = ctk.CTkButton(master=frame4, text="Aceptar", font=("Arial", 16), height=40, width=80,
                                      border_width=1, command=crearUsuario)
        buttonAceptar.grid(row=0, column=1, sticky="nsew")

    def boton2(self):
        iniciarSesion = CTkToplevel(self)
        iniciarSesion.title("Iniciar Sesion")
        iniciarSesion.geometry("400x400")
        iniciarSesion.maxsize(400, 400)
        iniciarSesion.minsize(400, 400)
        frameNombre = CTkFrame(iniciarSesion, fg_color="transparent")
        frameNombre.grid(row=0, column=0, pady=30, sticky="nsew")
        labelNombre = ctk.CTkLabel(master=frameNombre, text="Nombre: ", font=("Arial", 14))
        labelNombre.grid(row=0, column=0, sticky="nsw")
        EntryNombre = ctk.CTkEntry(master=frameNombre, border_width=2, width=250, height=35, font=("Arial", 14))
        EntryNombre.grid(row=1, column=0, sticky="nsw")
        frameContraseña = CTkFrame(iniciarSesion, fg_color="transparent")
        frameContraseña.grid(row=1, column=0, sticky="nsew")
        labelContrasena = ctk.CTkLabel(master=frameContraseña, text="Contraseña: ", font=("Arial", 14))
        labelContrasena.grid(row=0, column=0, sticky="nsw")
        EntryContrasena = ctk.CTkEntry(master=frameContraseña, border_width=2, width=250, height=35, font=("Arial", 14),show="*")
        EntryContrasena.grid(row=1, column=0, sticky="nsw")
        def ver_contrasena():
            if checkboxContrasena.get() == 1:
                EntryContrasena.configure(show="")
            elif checkboxContrasena.get() == 2:
                EntryContrasena.configure(show="*")
        checkboxContrasena = ctk.CTkCheckBox(master=frameContraseña, onvalue=1,offvalue=2,command=ver_contrasena, text="", border_width=2,width=5,
                                             height=5)
        checkboxContrasena.grid(row=1, column=1,sticky="nsw", padx=10)
        frameBoton = CTkFrame(iniciarSesion, fg_color="transparent")
        frameBoton.grid_columnconfigure(0,weight=2)
        frameBoton.grid_columnconfigure(1, weight=2)
        frameBoton.grid(row=2, column=0, pady=100, sticky="new")
        def inicioSesion():
            nombre = EntryNombre.get()
            contrasena = EntryContrasena.get()
            id = inicio_sesion(nombre,contrasena)
            if id >=0:
                resultado = database.datos_usuario(nombre)
                msg = CTkMessagebox(title="Sesion Iniciada", message=f"Bienvenido {nombre}", icon="check")
                if msg.get() == "OK":
                    crear_tabla()
                    crear_tabla_alimentos()
                    iniciarSesion.destroy()
                    menu_principal = MenuPrincipal(resultado,id,self)
                    self.after(100,lambda:[self.withdraw(), menu_principal.mainloop()])

            else:
                CTkMessagebox(title="Error", message="El usuario o contraseña incorrectas", icon="cancel")


        buttonAceptar = ctk.CTkButton(master=frameBoton, text="Iniciar Sesion", font=("Arial", 16), height=40,
                                      width=80, command=inicioSesion, border_width=1)
        buttonAceptar.grid(row=0, column=1,sticky="nswe")


