import tkinter

import customtkinter
import customtkinter as ctk
from PIL.ImageOps import expand
from customtkinter import CTk, CTkToplevel, CTkFrame
from CTkMessagebox import CTkMessagebox

from alimentos import calcular_macros
from database import guardar_alimento, eliminar_alimento,modificar_usuario, cargar_comidas, cargar_comidas, obtener_resultados_semanales, datos_usuario_id

import alimentos
from usuario import Usuario
from PIL import Image

class MenuPrincipal(ctk.CTkToplevel):

    def __init__(self,resultado,id,inicio):
        super().__init__()
        self.id = id
        self.inicio = inicio
        datos = resultado[0]
        self.usuario = Usuario(
            datos[1],
            float(datos[3]),
            float(datos[4]),
            datos[5],
            datos[6],
            int(datos[7]),
            datos[8]
        )
        self.caloriasNecesarias = self.usuario.calcularCalorias()
        self.minsize(1600, 900)
        self.title("Calendario de Comidas")
        self.resultado = resultado
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.comidas = ["Desayuno", "Comida", "Merienda", "Cena"]
        self.scroll = ctk.CTkScrollableFrame(self,fg_color="gray95")
        self.scroll.pack(fill="both",expand=True)
        self.celdas = {}
        self.datosnutricionales={}
        for i, dia in enumerate(self.dias):
            labelD = ctk.CTkLabel(master=self.scroll, text=dia)
            labelD.grid(row=0,column=i+1,ipadx=30 , sticky="nswe")
            labelD.grid_propagate(False)
        for j, comida in enumerate(self.comidas):
            labelD = ctk.CTkLabel(master=self.scroll, text=comida)
            labelD.grid(row=j+1, column=0, ipadx=30, sticky="nswe")
            for i in range(len(self.dias)):
                frameBlanco = CTkFrame(self.scroll, width=190, height=220, fg_color="gray95", border_width=2)
                frameBlanco.grid(row=j+1, column=i+1, sticky="nswe")
                frameAlimento = ctk.CTkScrollableFrame(master=frameBlanco,width=155,height=175,fg_color="gray95",scrollbar_button_color="gray95",scrollbar_button_hover_color="gray95")
                frameAlimento._scrollbar.configure(height=0)
                frameAlimento.pack(padx=2, pady=2)
                labelvacio = ctk.CTkLabel(master=frameAlimento, text="Alimento sin Añadir")
                labelvacio.pack()
                self.celdas[(j, i)] = frameAlimento
                botonPlus = ctk.CTkButton(master=frameBlanco, text="+", command=lambda row=j, column=i :self.introducirAlimentos(row,column), height=30,width=185)
                botonPlus.pack()
        for i in range(0, len(self.dias)):
            frameResumen = CTkFrame(self.scroll, height=80,width=180, fg_color="gray95", border_width=3)
            frameResumen.grid(row=5, column=i + 1, sticky="nswe",pady=5)
            frameResumen.grid_propagate(False)
            frameResumen.grid_columnconfigure(0, weight=1)
            frameResumen.grid_columnconfigure(1, weight=1)
            frameResumen.grid_columnconfigure(2, weight=1)
            frameResumen.grid_rowconfigure(0, weight=1)
            frameResumen.grid_rowconfigure(1, weight=1)
            frameResumen.grid_rowconfigure(2, weight=1)
            self.celdas[(5,i)] = frameResumen
            labelCal = ctk.CTkLabel(master=frameResumen,text="Calorias",border_width=1)
            labelCal.grid(row=0,column=0,sticky="nswe")
            calorias = ctk.CTkLabel(master=frameResumen,text="0",border_width=1)
            calorias.grid(row=0,column=1,sticky="nswe",columnspan=2)
            self.datosnutricionales[(i,0)] = calorias
            labelp = ctk.CTkLabel(master=frameResumen, text="Proteinas",border_width=1)
            labelp.grid(row=1, column=0, sticky="nswe")
            proteinas = ctk.CTkLabel(master=frameResumen, text="0",border_width=1)
            proteinas.grid(row=2, column=0, sticky="nswe")
            self.datosnutricionales[(i, 1)] = proteinas
            labelh = ctk.CTkLabel(master=frameResumen, text="Hidratos",border_width=1)
            labelh.grid(row=1, column=1, sticky="nswe")
            hdc = ctk.CTkLabel(master=frameResumen, text="0",border_width=1)
            hdc.grid(row=2, column=1, sticky="nswe")
            self.datosnutricionales[(i, 2)] = hdc
            labelg = ctk.CTkLabel(master=frameResumen, text="Grasas",border_width=1)
            labelg.grid(row=1, column=2, sticky="nswe")
            grasas = ctk.CTkLabel(master=frameResumen, text="0",border_width=1)
            grasas.grid(row=2, column=2, sticky="nswe")
            self.datosnutricionales[(i, 3)] = grasas
        self.informacion_usuario()
        self.cargar_botones_cerrar_sesion()
        self.cargar_datos()
        self.protocol("WM_DELETE_WINDOW", self.salir)
        self.state('zoomed')

        #def menu():
        #    if frameMenu.winfo_width() == 50:
        #        frameMenu.configure(width=150,height=300)
        #    else:
        #        frameMenu.configure(width=50, height=50)
        #botonOpciones = ctk.CTkButton(master=frameMenu, width=50, height=50, text="☰", command=menu)
        #botonOpciones.grid(row=0, column=0, sticky="nw")
        #boton_menu_cambiardatos =  ctk.CTkButton(master=frameMenu, text="Cambiar Datos Usuario")
        #boton_menu_cambiardatos.grid(row=1, column=0,sticky="nswe")
        #boton_menu_cerrarsesion = ctk.CTkButton(master=frameMenu, text="Cerrar Sesion")
        #boton_menu_cerrarsesion.grid(row=2, column=0, sticky="nswe")
        #boton_menu_cerraraplicacion = ctk.CTkButton(master=frameMenu, text="Salir")
        #boton_menu_cerraraplicacion.grid(row=3, column=0, sticky="nswe")


    def introducirAlimentos(self,row,colum):
        introducirDatos =  CTkToplevel(self)
        introducirDatos.title("Introducir Datos")
        introducirDatos.geometry("300x350")
        introducirDatos.maxsize(300, 350)
        introducirDatos.minsize(300, 350)
        labelcomida = ctk.CTkLabel(master=introducirDatos, text="Comida", font=("Arial", 14))
        labelcomida.place(x=80, y=40)
        entrycomida = ctk.CTkEntry(master=introducirDatos)
        entrycomida.place(x=80, y=60)
        labelg = ctk.CTkLabel(master=introducirDatos, text="Num Gramos", font=("Arial", 14))
        labelg.place(x=80, y=120)
        entryg = ctk.CTkEntry(master=introducirDatos)
        entryg.place(x=80, y=140)
        botonAlimentos = ctk.CTkButton(master=introducirDatos, text="Aceptar", command= lambda: self.guardarAlimento(entrycomida.get(),entryg.get(),row,colum))
        botonAlimentos.place(x=80, y=220)

    def guardarAlimento(self, alim, g, row, colum):
        try:
            celda = self.celdas[(row,colum)]
            labelDefault = celda.winfo_children()[0]
            if isinstance(labelDefault,ctk.CTkLabel):
                celda.winfo_children()[0].destroy()
            nutrientes = calcular_macros(alim, int(g))
            print(nutrientes["calorias"],nutrientes["proteinas"],nutrientes["hdc"],nutrientes["grasas"])
            id_insertado = guardar_alimento(self.id, self.dias[colum], self.comidas[row], alim, g,nutrientes["calorias"],nutrientes["proteinas"],nutrientes["hdc"],nutrientes["grasas"])
            frame = CTkFrame(celda, fg_color="gray95")
            frame.pack(expand=True)
            label = ctk.CTkLabel(frame, text=f"{alim}: {g}g")
            label.grid(row=0, column=0, sticky="nse")
            bton_eliminar = ctk.CTkButton(frame, width=20, height=10,text="-", command= lambda: self.borrar(celda,frame,id_insertado))
            bton_eliminar.grid(row=0, column=1, padx=5)
            if celda.winfo_height()>159:
                celda.configure(scrollbar_button_color="gray35",scrollbar_button_hover_color="gray30")
            self.cargar_resultados()

        except:
            CTkMessagebox(title="Error", message="Datos no válidos", icon="cancel")
    def guardarAlimentos(self,id, alim, g, row, colum):
        try:
            celda = self.celdas[(row,colum)]
            labelDefault = celda.winfo_children()[0]
            if isinstance(labelDefault,ctk.CTkLabel):
                celda.winfo_children()[0].destroy()
            frame = CTkFrame(celda, fg_color="gray95")
            frame.pack(expand=True)
            label = ctk.CTkLabel(frame, text=f"{alim}: {g}g")
            label.grid(row=0, column=0, sticky="nse")
            bton_eliminar = ctk.CTkButton(frame, width=20, height=10,text="-", command= lambda: self.borrar(celda,frame,id))
            bton_eliminar.grid(row=0, column=1, padx=5)
            if celda.winfo_height()>159:
                celda.configure(scrollbar_button_color="gray35",scrollbar_button_hover_color="gray30")
            self.cargar_resultados()


        except:
            CTkMessagebox(title="Error", message="Datos no válidos", icon="cancel")

    def borrar(self, celda, frame,id_insertado):
        frame.destroy()
        eliminar_alimento(id_insertado)
        if not celda.winfo_children():
            labelvacio = ctk.CTkLabel(celda, text="Alimento sin Añadir")
            labelvacio.pack()
        self.cargar_resultados()

    def cargar_datos(self):
        contenido_a_cargar = cargar_comidas(self.id)
        for i in range(0, len(contenido_a_cargar)):
            row = self.comidas.index(contenido_a_cargar[i][3])
            column = self.dias.index(contenido_a_cargar[i][2])
            self.guardarAlimentos(contenido_a_cargar[i][0], contenido_a_cargar[i][4], contenido_a_cargar[i][5], row, column)
        self.cargar_resultados()

    def cargar_resultados(self):
        resultados = obtener_resultados_semanales(self.id)
        for i in range(0, len(resultados)):
            dia = self.dias.index(resultados[i][0])
            if int(resultados[i][1])>int(self.usuario.calcularCalorias())+100 or int(resultados[i][1])<int(self.usuario.calcularCalorias())-100:
                self.datosnutricionales[(dia, 0)].configure(text=resultados[i][1], text_color="red")
            else:
                self.datosnutricionales[(dia, 0)].configure(text=resultados[i][1], text_color="green")
            self.datosnutricionales[(dia, 1)].configure(text=resultados[i][2])
            self.datosnutricionales[(dia, 2)].configure(text=resultados[i][3])
            self.datosnutricionales[(dia, 3)].configure(text=resultados[i][4])

    def informacion_usuario(self):
        frameDatos = CTkFrame(self.scroll, height=260, width=200, fg_color="gray95", border_width=1)
        frameDatos.grid(row=1, column=8, sticky="nwe",padx=15,rowspan=2, columnspan=2)
        frameDatos.pack_propagate(False)
        frameDatos.grid_propagate(False)
        frameInformacion = CTkFrame(master=frameDatos, height=50, width=200, fg_color="gray95")
        frameInformacion.pack(side=ctk.TOP)
        frameInformacion.grid_rowconfigure(0, weight=2)
        frameInformacion.grid_columnconfigure(0, weight=2)
        frameInformacion.grid_propagate(False)
        labelInformacion = ctk.CTkLabel(master=frameInformacion, text="INFORMACIÓN", font=("Arial", 18), fg_color="gray95",
                                        border_width=1)
        labelInformacion.grid(row=0, column=0, sticky="nsew")
        frameNombre = CTkFrame(master=frameDatos, height=30, width=200, fg_color="gray95")
        frameNombre.pack()
        frameNombre.grid_columnconfigure(0, weight=5)
        frameNombre.grid_columnconfigure(1, weight=5)
        frameNombre.grid_propagate(False)
        labelNombre = ctk.CTkLabel(master=frameNombre, text="Nombre:", height=30, width=100, font=("Arial", 14),
                                   border_width=1)
        labelNombre.grid(row=0, column=0, sticky="nsew")
        nombre = ctk.CTkEntry(master=frameNombre, height=30, width=100, font=("Arial", 14), border_width=1,
                              justify="center", corner_radius=0)
        nombre.insert(0, f"{self.usuario.nombre}")
        nombre.configure(state="disabled")
        nombre.grid(row=0, column=1, sticky="nsew")
        frameAltura = CTkFrame(master=frameDatos, height=30, width=200, fg_color="gray95")
        frameAltura.pack()
        frameAltura.grid_columnconfigure(0, weight=5)
        frameAltura.grid_columnconfigure(1, weight=5)
        frameAltura.grid_propagate(False)
        labelAltura = ctk.CTkLabel(master=frameAltura, text="Altura(cm):", height=30, width=100, font=("Arial", 14),
                                   border_width=1)
        labelAltura.grid(row=0, column=0, sticky="nsew")
        altura = ctk.CTkEntry(master=frameAltura, height=30, width=100, font=("Arial", 14), border_width=1,
                              justify="center", corner_radius=0)
        altura.grid(row=0, column=1, sticky="nsew")
        altura.insert(0, f"{int(self.usuario.altura)}")
        altura.configure(state="disabled")
        framePeso = CTkFrame(master=frameDatos, height=30, width=200, fg_color="gray95")
        framePeso.pack()
        framePeso.grid_columnconfigure(0, weight=5)
        framePeso.grid_columnconfigure(1, weight=5)
        framePeso.grid_propagate(False)
        labelPeso = ctk.CTkLabel(master=framePeso, text="Peso(kg):", height=30, width=100, font=("Arial", 14), border_width=1)
        labelPeso.grid(row=0, column=0, sticky="nsew")
        peso = ctk.CTkEntry(master=framePeso, height=30, width=100, font=("Arial", 14), border_width=1, justify="center", corner_radius=0)
        peso.insert(0, f"{int(self.usuario.peso)}")
        altura.configure(state="disabled")
        peso.grid(row=0, column=1, sticky="nsew")
        frameEdad = CTkFrame(master=frameDatos, height=30, width=200, fg_color="gray95")
        frameEdad.pack()
        frameEdad.grid_columnconfigure(0, weight=5)
        frameEdad.grid_columnconfigure(1, weight=5)
        frameEdad.grid_propagate(False)
        labelEdad = ctk.CTkLabel(master=frameEdad, text="Edad:", height=30, width=100, font=("Arial", 14), border_width=1)
        labelEdad.grid(row=0, column=0, sticky="nsew")
        edad = ctk.CTkEntry(master=frameEdad, height=30, width=100, font=("Arial", 14), border_width=1, justify="center", corner_radius=0)
        edad.insert(0, f"{self.usuario.edad}")
        edad.configure(state="disabled")
        edad.grid(row=0, column=1, sticky="nsew")
        frameActividad = CTkFrame(master=frameDatos, height=30, width=200, fg_color="gray95")
        frameActividad.pack()
        frameActividad.grid_columnconfigure(0, weight=5)
        frameActividad.grid_columnconfigure(1, weight=5)
        frameActividad.grid_propagate(False)
        labelActividad = ctk.CTkLabel(master=frameActividad, text="Actividad:", height=30, width=100, font=("Arial", 14),
                                      border_width=1)
        labelActividad.grid(row=0, column=0, sticky="nsew")
        actividad = ctk.CTkEntry(master=frameActividad, height=30, width=100, font=("Arial", 14), border_width=1,
                                 justify="center", corner_radius=0)
        actividad.insert(0, f"{self.usuario.actividad}")
        actividad.configure(state="disabled")
        actividad.grid(row=0, column=1, sticky="nsew")
        frameObjetivo = CTkFrame(master=frameDatos, height=30, width=200, fg_color="gray95")
        frameObjetivo.pack()
        frameObjetivo.grid_columnconfigure(0, weight=5)
        frameObjetivo.grid_columnconfigure(1, weight=5)
        frameObjetivo.grid_propagate(False)
        labelObjetivo = ctk.CTkLabel(master=frameObjetivo, text="Objetivo:", height=30, width=100, font=("Arial", 14),
                                     border_width=1)
        labelObjetivo.grid(row=0, column=0, sticky="nsew")
        objetivo = ctk.CTkEntry(master=frameObjetivo, height=30, width=100, font=("Arial", 14), border_width=1,
                                justify="center", corner_radius=0)
        objetivo.insert(0, f"{self.usuario.objetivo}")
        objetivo.configure(state="disabled")
        objetivo.grid(row=0, column=1, sticky="nsew")
        frameCal = CTkFrame(master=frameDatos, height=30, width=200, fg_color="gray95")
        frameCal.pack()
        frameCal.grid_columnconfigure(0, weight=5)
        frameCal.grid_columnconfigure(1, weight=5)
        frameCal.grid_propagate(False)
        labelCal = ctk.CTkLabel(master=frameCal, text="Calorias/dia:", height=30, width=100, font=("Arial", 14),
                                border_width=1)
        labelCal.grid(row=0, column=0, sticky="nsew")
        cal = ctk.CTkLabel(master=frameCal, text=f"{self.caloriasNecesarias} cal", height=30, width=100, font=("Arial", 14),
                           border_width=1)
        cal.grid(row=0, column=1, sticky="nsew")
        frameBotones = CTkFrame(self.scroll, height=260, width=130, fg_color="gray95")
        frameBotones.grid(row=1, column=10, sticky="nwe", pady=5, rowspan=2, columnspan=2)
        frameBotones.pack_propagate(False)
        frameBotones.grid_propagate(False)
        self.botonModificar = ctk.CTkButton(master=frameBotones, width=130, height=35, text="Modificar",command=lambda: self.modificar(altura,peso,actividad,objetivo))
        self.botonGuardar = ctk.CTkButton(master=frameBotones,state="disabled", width=130, height=35, text="Guardar",command=lambda: self.guardar(altura,peso,actividad,objetivo,cal))
        self.botonCancelar = ctk.CTkButton(master=frameBotones,state="disabled", width=130, height=35, text="Cancelar",command=lambda: self.cargar_informacion(altura,peso,actividad,objetivo))
        self.botonModificar.pack(pady=25)
        self.botonGuardar.pack(pady=25)
        self.botonCancelar.pack(pady=25)

    def cargar_botones_cerrar_sesion(self):
        frameCerrar = CTkFrame(self.scroll, width=200, height=40,fg_color="gray95")
        frameCerrar.grid(row=2, column=8,pady=50, sticky="nwe")
        img_cerrar_sesion = ctk.CTkImage(light_image=Image.open("images/cerrar-sesion.png"))
        img_salir = ctk.CTkImage(light_image=Image.open("images/close.png"))
        boton_cerrar_sesion = ctk.CTkButton(master=frameCerrar, image=img_cerrar_sesion, text="", width=40,height=40, command=self.cerrar_sesion)
        boton_cerrar_sesion.pack(side=ctk.LEFT, padx=40)
        boton_salir = ctk.CTkButton(master=frameCerrar, image=img_salir, text="", width=40, height=40,command=self.salir)
        boton_salir.pack(padx=10)

    def cerrar_sesion(self):
        self.inicio.deiconify()
        self.destroy()

    def salir(self):
        self.inicio.destroy()

    def modificar(self,altura,peso,actividad,objetivo):
        altura.configure(state="normal",fg_color="gray85")
        peso.configure(state="normal",fg_color="gray85")
        actividad.configure(state="normal",fg_color="gray85")
        objetivo.configure(state="normal",fg_color="gray85")
        self.botonModificar.configure(state="disabled")
        self.botonGuardar.configure(state="normal")
        self.botonCancelar.configure(state="normal")


    def cargar_informacion(self, altura, peso, actividad, objetivo):
        campos = [
            (altura, int(self.usuario.altura)),
            (peso, int(self.usuario.peso)),
            (actividad, int(self.usuario.actividad)),
            (objetivo, self.usuario.objetivo),
        ]
        for entry, valor in campos:
            entry.configure(state="normal",fg_color="gray95")
            entry.delete(0, "end")
            entry.insert(0, f"{valor}")
            entry.configure(state="disabled")
        self.botonModificar.configure(state="normal")
        self.botonGuardar.configure(state="disabled")
        self.botonCancelar.configure(state="disabled")

    def guardar(self, altura, peso, actividad, objetivo,cal):
        if 1<=int(actividad.get())<=5 and objetivo.get() == "adelgazar" or objetivo.get()== "tonificar":
            self.usuario.altura = int(altura.get())
            self.usuario.peso = int(peso.get())
            self.usuario.actividad = int(actividad.get())
            self.usuario.objetivo = objetivo.get()
            self.caloriasNecesarias = self.usuario.calcularCalorias()
            cal.configure(text=self.caloriasNecesarias)
            modificar_usuario(self.id,self.usuario.altura,self.usuario.peso,self.usuario.actividad,self.usuario.objetivo)
            self.cargar_informacion(altura, peso, actividad, objetivo)
            self.cargar_resultados()
            self.botonModificar.configure(state="normal")
            self.botonGuardar.configure(state="disabled")
            self.botonCancelar.configure(state="disabled")
        else:
            self.cargar_informacion(altura, peso, actividad, objetivo)
