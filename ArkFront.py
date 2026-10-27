"""
@author: Orlando Vargas Gomez
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
from datetime import datetime 

def comprobarRuta(ruta,nombre,tipo):
    if tipo == "Carpeta":
        if not os.path.exists(ruta):
            print(f"La carpeta {nombre} no se encuentra en {ruta}, generando uno nuevo...")
            os.mkdir(ruta)
            print(f"{nombre} Listo !!")
        else:
            print(f"{nombre} Verificado")
    else:
        rutaArchivo = os.path.join(ruta,f"{nombre}.txt")
        if not os.path.exists(rutaArchivo):
            with open(rutaArchivo, "w") as disp:
                match nombre:
                    case "UsuariosRegistrados":
                        print("Nombre;Correo;Fecha", file = disp)
                    case "Agentes":
                        print("Nombre;Elemento;Arma", file = disp)
                    case "Materiales":
                        print("Nombre;Menas;Pureza;Region", file = disp)
                    case _:
                        print("Error archivo incorrecto")
        else:
            print(f"{nombre} Verificado")
            with open(rutaArchivo, "r") as disp:
                fila = disp.readlines()
                match nombre:
                        case "UsuariosRegistrados":
                            for f in fila[1:]:
                                dato = f.strip().split(";")
                                UsuariosRegistrados.append(Usuario(dato[0],dato[1],dato[2]))
                        case "Agentes":
                            for f in fila[1:]:
                                dato = f.strip().split(";")
                                Agentes.append(Agente(dato[0],dato[1],dato[2]))
                        case "Materiales":
                            for f in fila[1:]:
                                dato = f.strip().split(";")
                                Materiales.append(Material(dato[0],dato[1],dato[2],dato[3]))
                        case _:
                            print("Error archivo incorrecto")
            

class Usuario():
    def __init__(self, nombre, correo, fecha):
        self.nombre = nombre
        self.correo = correo
        self.fecha = fecha
    
    def __repr__(self):
        return f"Usuario(nombre='{self.nombre}', email='{self.correo}', fecha de creacion='{self.fecha}')"
    
class Agente():
    def __init__(self, nombre, elemento, arma):
        self.nombre = nombre
        self.elemento = elemento
        self.arma = arma
    
    def __repr__(self):
        return f"Usuario(nombre='{self.nombre}', elemento='{self.elemento}', arma='{self.arma}')"
    
class Material():
    def __init__(self, nombre, menas, pureza, region):
        self.nombre = nombre
        self.menas = menas
        self.pureza = pureza
        self.region = region
    
    def __repr__(self):
        return f"Usuario(nombre='{self.nombre}', Cantidad de menas='{self.menas}', pureza='{self.pureza}', region='{self.region}')"

UsuariosRegistrados=[]
Agentes=[]
Materiales=[]

usuarioActivo = [None]

rutaNucleo = "Proyecto/Nucleo"
rutaUsuario = "Proyecto/Usuarios"

comprobarRuta(rutaNucleo,"Nucleo","Carpeta")
comprobarRuta(rutaUsuario,"Usuarios","Carpeta")
comprobarRuta(rutaNucleo,"UsuariosRegistrados","Archivo")
comprobarRuta(rutaNucleo,"Agentes","Archivo")
comprobarRuta(rutaNucleo,"Materiales","Archivo")

UsuariosNombre = []
def vaciarNombres():
    for f in UsuariosRegistrados:
        UsuariosNombre.append(f.nombre)
vaciarNombres()

# --- Ventana principal ---

# Ventana Registro
ventana_secundaria = None
def abrir_ventana_secundaria():
    global ventana_secundaria
    if ventana_secundaria is None or not ventana_secundaria.winfo_exists():
        ventana_secundaria = tk.Toplevel(Ventana)
        ventana_secundaria.title("Ventana registro")
        ventana_secundaria.geometry("500x200")
        
        btn_top_style = {"bg": "#1C3A75", "fg": "white", "relief": "flat", "font": ("Helvetica", 8, "bold"), "cursor": "hand2"}
        ventana_secundaria.config(background="#7491CA")
        etiqueta = tk.Label(ventana_secundaria, text="Registrar...", background="#7491CA", fg="#eee")
        etiqueta.pack(pady=20)

        Bnt_R = tk.Frame(ventana_secundaria, bg="#7491CA")
        Bnt_R.pack()
        BTON_RP = tk.Button(Bnt_R, text="Usuario", **btn_top_style, width=10,command=reg_Usuario)
        BTON_RP.grid(column=1, row=1, padx=5)
        BTON_RM = tk.Button(Bnt_R, text="Material", **btn_top_style, width=10,command=reg_Material)
        BTON_RM.grid(column=2, row=1, padx=5)
        BTON_RA = tk.Button(Bnt_R, text="Agente", **btn_top_style, width=10,command=reg_Agente)
        BTON_RA.grid(column=3, row=1, padx=5)

        Bnt_C = tk.Frame(ventana_secundaria, bg="#7491CA")
        Bnt_C.pack()
        BNT_CE = tk.Button(Bnt_C, text="Cerrar",**btn_top_style, width=10, command=ventana_secundaria.destroy)
        BNT_CE.grid(column=0, row=0, pady=50)
    else:
        ventana_secundaria.focus_force()

# Combobox
def activarUsuario(u):
    usuarioActivo[0] = u
    if not usuarioActivo[0] == "":
        BTON_P.config(state='normal')
        BTON_M.config(state='normal')
        BTON_A.config(state='normal')
        texto_variable.set(u)   

# Mostrar datos de tabla
def mostrar_datos(tipo,dato1):
    Tabla.delete(*Tabla.get_children())
    match tipo:
        case "PUsuario":
            for i, usuario in enumerate(UsuariosRegistrados):
                if usuario.nombre == dato1:
                    posicion = i
            datoRegistrado = UsuariosRegistrados[posicion]
            Tabla.insert("", "end", values=(datoRegistrado.nombre, datoRegistrado.correo, datoRegistrado.fecha))
        case "PMateriales":
            for elementos in Materiales:
                Tabla.insert("", "end", values=(elementos.nombre, elementos.menas, elementos.pureza, elementos.region))
        case "PAgentes":
            for elementos in Agentes:
                Tabla.insert("", "end", values=(elementos.nombre, elementos.elemento, elementos.arma))

# Perfil
def pestanaPerfil(usuario):
    texto_variableActividad.set("Perfil")
    columnas_actuales = list(Tabla["column"])
    columnas_actuales.pop()
    Tabla["displaycolumns"] = columnas_actuales
    for col, text in zip(["C1","C2","C3"], ["Nombre", "Email", "Fecha de creacion"]):  
        Tabla.heading(col, text=text)
    Tabla.column("C1", width=200)
    Tabla.column("C2", width=200)
    Tabla.column("C3", width=200)
    mostrar_datos("PUsuario",usuario)

# Materiales
def pestanaMateriales():
    for col, text in zip(["C1","C2","C3","C4"], ["Nombre", "Cantidad de menas", "Pureza","Region"]):  
        Tabla.heading(col, text=text)
    columnas_actuales = list(Tabla["column"])
    Tabla["displaycolumns"] = columnas_actuales
    Tabla.column("C1", width=200)
    Tabla.column("C2", width=200)
    Tabla.column("C3", width=200)
    Tabla.column("C4", width=200)
    Tabla.update_idletasks()
    mostrar_datos("PMateriales",None)

# Agentes
def pestanaAgentes():
    columnas_actuales = list(Tabla["column"])
    columnas_actuales.pop()
    Tabla["displaycolumns"] = columnas_actuales
    for col, text in zip(["C1","C2","C3"], ["Nombre", "Elemento", "Arma"]):  
        Tabla.heading(col, text=text)
    Tabla.column("C1", width=200)
    Tabla.column("C2", width=200)
    Tabla.column("C3", width=200)
    mostrar_datos("PAgentes",None)


# --- Ventana Registro ---
ventana_Reg = None

def gen_VentanaR(titulo):
    global ventana_secundaria
    global ventana_Reg
    ventana_secundaria.destroy()
    if ventana_Reg is None or not ventana_Reg.winfo_exists():
        ventana_Reg = tk.Toplevel(Ventana)
        ventana_Reg.title("Ventana registro")
        ventana_Reg.geometry("800x200")
        ventana_Reg.config(background="#7491CA")
        etiqueta = tk.Label(ventana_Reg, textvariable=tituloRegistro,**lbl_style, background="#7491CA")
        tituloRegistro.set(f"{titulo}")
        etiqueta.pack(pady=20)
    else:
        ventana_Reg.focus_force()

# Usuario
def reg_Usuario():
    gen_VentanaR("Usuario")
    FRegistros = tk.Frame(ventana_Reg, bg="#7491CA")
    FRegistros.pack()

    tk.Label(FRegistros, text="Nombre completo:", **lbl_style).grid(column=1, row=0)
    ENTRY_N = tk.Entry(FRegistros, width=10)
    ENTRY_N.grid(column=2, row=0, padx=5)
    
    tk.Label(FRegistros, text="Correo:", **lbl_style).grid(column=3, row=0)
    ENTRY_E = tk.Entry(FRegistros, width=10)
    ENTRY_E.grid(column=4, row=0, padx=5)

    FBnt_E = tk.Frame(ventana_Reg, bg="#7491CA")
    FBnt_E.pack()

    fecha = datetime.now().strftime("%d/%m/%Y")

    BNT_E = tk.Button(FBnt_E, text="Enviar",**btn_top_style, width=10, command=lambda: registro(rutaNucleo,"UsuariosRegistrados",ENTRY_N.get(), ENTRY_E.get(),fecha,None))
    BNT_E.grid(column=0, row=0, pady=50)

# Material
def reg_Material():
    gen_VentanaR("Materiales")
    FRegistros = tk.Frame(ventana_Reg, bg="#7491CA")
    FRegistros.pack()

    tk.Label(FRegistros, text="Nombre:", **lbl_style).grid(column=1, row=0)
    ENTRY_N = tk.Entry(FRegistros, width=10)
    ENTRY_N.grid(column=2, row=0, padx=5)
    
    tk.Label(FRegistros, text="Menas:", **lbl_style).grid(column=3, row=0)
    ENTRY_M = tk.Entry(FRegistros, width=10)
    ENTRY_M.grid(column=4, row=0, padx=5)

    tk.Label(FRegistros, text="Pureza:", **lbl_style).grid(column=5, row=0)
    ENTRY_P = tk.Entry(FRegistros, width=10)
    ENTRY_P.grid(column=6, row=0, padx=5)
    
    tk.Label(FRegistros, text="Region:", **lbl_style).grid(column=7, row=0)
    ENTRY_R = tk.Entry(FRegistros, width=10)
    ENTRY_R.grid(column=8, row=0, padx=5)

    FBnt_E = tk.Frame(ventana_Reg, bg="#7491CA")
    FBnt_E.pack()

    BNT_E = tk.Button(FBnt_E, text="Enviar",**btn_top_style, width=10, command=lambda: registro(rutaNucleo,"Materiales",ENTRY_N.get(), ENTRY_M.get(),ENTRY_P.get(),ENTRY_R.get()))
    BNT_E.grid(column=0, row=0, pady=50)

# Agente
def reg_Agente():
    gen_VentanaR("Usuario")
    FRegistros = tk.Frame(ventana_Reg, bg="#7491CA")
    FRegistros.pack()

    tk.Label(FRegistros, text="Nombre:", **lbl_style).grid(column=1, row=0)
    ENTRY_N = tk.Entry(FRegistros, width=10)
    ENTRY_N.grid(column=2, row=0, padx=5)
    
    tk.Label(FRegistros, text="Elemento:", **lbl_style).grid(column=3, row=0)
    ENTRY_E = tk.Entry(FRegistros, width=10)
    ENTRY_E.grid(column=4, row=0, padx=5)

    tk.Label(FRegistros, text="Arma:", **lbl_style).grid(column=5, row=0)
    ENTRY_A = tk.Entry(FRegistros, width=10)
    ENTRY_A.grid(column=6, row=0, padx=5)

    FBnt_E = tk.Frame(ventana_Reg, bg="#7491CA")
    FBnt_E.pack()

    BNT_E = tk.Button(FBnt_E, text="Enviar",**btn_top_style, width=10, command=lambda: registro(rutaNucleo,"Agentes",ENTRY_N.get(), ENTRY_E.get(),ENTRY_A.get(),None))
    BNT_E.grid(column=0, row=0, pady=50)


## Registro

def registro(ruta,nombre,nombreRegistro,registro2,registro3,registro4):
    rutaArchivo = os.path.join(ruta,f"{nombre}.txt")
    global tituloRegistro
    if os.path.exists(rutaArchivo):
        with open(rutaArchivo, "a") as disp:
            match nombre:
                case "UsuariosRegistrados":
                    print(f"{nombreRegistro};{registro2};{registro3}", file = disp)
                    tituloRegistro.set("Registrado correctamente")
                case "Agentes":
                    print(f"{nombreRegistro};{registro2};{registro3};{registro4}", file = disp)
                    tituloRegistro.set("Registrado correctamente")
                case "Materiales":
                    print(f"{nombreRegistro};{registro2};{registro3}", file = disp)
                    tituloRegistro.set("Registrado correctamente")
                case _:
                    tituloRegistro.set("Error archivo incorrecto")
    else:
        tituloRegistro.set("ERROR al encontrar la Base de Datos")

# --- Configuración de la Ventana Principal ---
Ventana = tk.Tk()
Ventana.title("ArkSystem | Sistema de Gestión de Personajes de Arkings")
Ventana.geometry("1600x850") 
Ventana.configure(bg="#B5C6E7") 

# --- ESTILOS ---
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("Treeview.Heading", background="#2C3E50", foreground="white", font=("Helvetica", 10, "bold"))
estilo.map("Treeview.Heading", background=[('active', "#425C8B")] )
estilo.configure("Treeview",background="#B8C4DB", fieldbackground="#f1f6fa", rowheight=30, font=("Helvetica", 10),)
estilo.map("Treeview", background=[('selected', "#869FCF")] )

lbl_style = {"bg": "#7491CA", "fg": "white", "font": ("Helvetica", 10, "bold")}
btn_top_style = {"bg": "#1C3A75", "fg": "white", "relief": "flat", "font": ("Helvetica", 8, "bold"), "cursor": "hand2"}
btn_reg_style = {"bg": "#435475", "fg": "white", "relief": "flat", "font": ("Helvetica", 10, "bold"), "cursor": "hand2"}
tituloRegistro = tk.StringVar(value="None")


AreaPrincipal = tk.Frame(Ventana, bg="#435475")
AreaPrincipal.pack(side="right", fill="both", expand=True)

# --- Encabezado de Usuario ---
FrameHeader = tk.Frame(AreaPrincipal, bg="#1E2D4B", pady=10, padx=30)
FrameHeader.pack(fill="x")
f_usuario = tk.Frame(FrameHeader, bg="#1E2D4B")
f_usuario.pack(side="right")
tk.Label(f_usuario, text="Usuario", font=("Helvetica", 10), bg="#1E2D4B", fg="#eee", pady=0).pack()
texto_variable = tk.StringVar(value="None")
L_USUARIO = tk.Label(f_usuario, textvariable=texto_variable, font=("Helvetica", 16, "bold"), bg="#1E2D4B", fg="#eee").pack()

f_registro = tk.Frame(FrameHeader, bg="#1E2D4B")
f_registro.pack(side="left")
BTON_L = tk.Button(f_registro, text="Registrar", **btn_reg_style, width=10, command=abrir_ventana_secundaria).pack()

# --- Cuerpo Eleccion ----
FrameControl = tk.Frame(AreaPrincipal, bg="#7491CA", padx=10, pady=10)
FrameControl.pack(fill="x")

sub_control = tk.Frame(FrameControl, bg="#7491CA")
sub_control.pack()

tk.Label(sub_control, text="Usuarios", **lbl_style).grid(column=0, row=0, padx=10)
ListaUsuarios = ttk.Combobox(sub_control, values=UsuariosNombre, state="readonly")
ListaUsuarios.grid(column=0, row=1, padx=10, pady=5)

BTON_L = tk.Button(sub_control, text="Usar", **btn_top_style, width=10, command=lambda: activarUsuario(ListaUsuarios.get()))
BTON_L.grid(column=1, row=1, padx=5)


# -- Acciones --
FrameControl2 = tk.Frame(AreaPrincipal, bg="#7491CA", padx=1, pady=10)
FrameControl2.pack(fill="x")

sub_control2 = tk.Frame(FrameControl2, bg="#7491CA")
sub_control2.pack()


tk.Label(sub_control2, text="Perfil", **lbl_style).grid(column=1, row=0)
BTON_P = tk.Button(sub_control2, text="Ver", **btn_top_style, width=10,command=lambda: pestanaPerfil(usuarioActivo[0]), state='disabled')
BTON_P.grid(column=1, row=1, padx=5)

tk.Label(sub_control2, text="Materiales", **lbl_style).grid(column=2, row=0)
BTON_M = tk.Button(sub_control2, text="Ver", **btn_top_style, width=10,command=pestanaMateriales, state='disabled')
BTON_M.grid(column=2, row=1, padx=5)

tk.Label(sub_control2, text="Agentes", **lbl_style).grid(column=3, row=0)
BTON_A = tk.Button(sub_control2, text="Ver", **btn_top_style, width=10,command=pestanaAgentes, state='disabled')
BTON_A.grid(column=3, row=1, padx=5)

# -- Area principal --
texto_variableActividad = tk.StringVar(value="No Seleccionado")
tk.Label(AreaPrincipal, textvariable=texto_variableActividad, font=("Helvetica", 10, "bold"), bg="#435475", fg="#eee").pack(pady=(10, 0))
FrameInformacion = tk.Frame(AreaPrincipal, bg="#B5C6E7", padx=10, pady=10)
FrameInformacion.pack(fill="both", expand=True, padx=20, pady=(0, 20))
scroll = ttk.Scrollbar(FrameInformacion, orient="vertical")
scroll.pack(side="right", fill="y")
Tabla = ttk.Treeview(FrameInformacion, columns=("C1","C2","C3","C4"), show="headings",yscrollcommand=scroll.set)
Tabla.heading("C1", text="")
Tabla.heading("C2", text="")
Tabla.heading("C3", text="")
Tabla.heading("C4", text="")

Tabla.column("C1", width=200)
Tabla.column("C2", width=200)
Tabla.column("C3", width=200)
Tabla.column("C4", width=200)

Tabla.pack(side="left", fill="both", expand=True)
scroll.configure(command=Tabla.yview)





Ventana.mainloop()
