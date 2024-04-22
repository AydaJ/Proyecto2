import tkinter as tk  # Importar la biblioteca Tkinter para la interfaz gráfica
from tkinter import messagebox  # Importar messagebox de Tkinter para mostrar mensajes emergentes
from os import path  # Importar la función path del módulo os para manipular rutas de archivo
import os  # Importar el módulo os para funcionalidades del sistema operativo
class InventarioDescuentosSingleton: # clase
    _instance = None

    def __new__(cls):  # Método especial para crear una nueva instancia
        if cls._instance is None:  # Verificar si no hay una instancia existente
            cls._instance = super().__new__(cls)  # Crear una nueva instancia
            return cls._instance
        else:
            return cls._instance  # Devolver la instancia existente

class JoyeriaFactory:  # Clase
    @staticmethod
    def crear_joya(nombreJoya: str, cantidad: int, precio: float, material: str):  # Tipo de datos en los parámetros
        return Joyeria(nombreJoya, cantidad, precio, material)

class Joyeria:  # Clase
    def __init__(self, nombreJoya: str, cantidad: int, precio: float, material: str):  # Tipo de datos en los parámetros
        self.nombreJoya = nombreJoya
        self.cantidad = cantidad
        self.precio = precio
        self.material = material
        self.descuentoAplicado = False  # Inicializar el indicador de descuento como falso

    def __str__(self):  # Método especial para representar la instancia como cadena de texto
        return f"{self.nombreJoya} - Precio: ${self.precio} - Cantidad: {self.cantidad}"

    def guardar_inventario(self):  # Método para guardar el inventario en un archivo
        with open("joyas.txt", 'a') as archivo:  # Abrir el archivo en modo de escritura
            archivo.write(f"{self.nombreJoya}-{self.cantidad}-{self.precio}-{self.material}-{self.descuentoAplicado}\n")  # Escribir los datos de la joya en el archivo
            print(f"Inventario guardado con éxito")  # Imprimir un mensaje de confirmación

# Clase para adaptar joyas con descuento al sistema existente
class DescuentoJoyaAdapter:  # Clase
    def __init__(self, joya):
        self.joya = joya

    def aplicar_descuento(self, porcentaje):  # Método para aplicar descuento
        self.joya.precio -= self.joya.precio * (porcentaje / 100)  # Aplicar el descuento al precio de la joya
        self.joya.descuentoAplicado = True  # Marcar la joya como con descuento aplicado

    def __str__(self):  # Método especial para representar la instancia como cadena de texto
        return f"DescuentoJoyaAdapter: {self.joya}"

# Clase que representa una joya con descuento
class DescuentoJoya(Joyeria):  # Herencia
    def __init__(self, nombreJoya: str, cantidad: int, precio: float, material: str, porcentaje=0):  # Tipo de datos en los parámetros
        super().__init__(nombreJoya, cantidad, precio, material)

    def aplicar_descuento(self, porcentaje_descuento):  # Método para aplicar descuento
        self.precio -= self.precio * (porcentaje_descuento / 100)  # Aplicar el descuento al precio de la joya
        self.descuentoAplicado = True  # Marcar la joya como con descuento aplicado

# Clase para gestionar el inventario de joyas
class InventarioJoyas:  # Herencia
    def __init__(self):
        self.joyas = []  # Lista para almacenar las joyas en el inventario

    def agregarJoyas(self, joya):  # Método para agregar joyas al inventario
        self.joyas.append(joya)

    def buscarJoyasPorNombre(self, nombre):  # Método para buscar joyas por nombre
        try:
            with open("joyas.txt", "r") as archivo:
                for linea in archivo:
                    info = linea.rstrip().split("-")
                    if info[0] == nombre:
                        return Joyeria(info[0], int(info[1]), float(info[2]), info[3])  # Devolver la joya encontrada
            return None  # Devolver None si no se encuentra la joya
        except Exception as e:
            print(f"Error al buscar joya: {e}")
            return None

    def eliminarJoyas(self, nombre):  # Método para eliminar joyas del inventario
        try:
            with open("joyas.txt", "r") as archivo:
                lineas = archivo.readlines()
            with open("joyas.txt", "w") as archivo:
                for linea in lineas:
                    info = linea.rstrip().split("-")
                    if info[0] != nombre:
                        archivo.write(linea)
            print("Joya eliminada con éxito")
        except Exception as e:
            print(f"Error al eliminar joya: {e}")

    def vectorJoyas(self):  # Método para mostrar el vector de joyas en la consola
        total_descuento = 0
        total_precio = 0

        if not self.joyas:
            print("No hay joyas en el inventario")
            return

        for i, joya in enumerate(self.joyas):
            print(f"{i + 1}. {joya}")
            total_precio += joya.precio
            if joya.descuentoAplicado:
                total_descuento += (joya.precio * joya.porcentaje_descuento / 100)

        print(f"Total Descuento: ${total_descuento}")
        print(f"Total Precio: ${total_precio}")

        return total_descuento, total_precio

# Clase para gestionar el inventario de joyas con descuento
class InventarioDescuentos(InventarioJoyas):  # Herencia
    def __init__(self):
        super().__init__()
        self.joyas = []
        self.actualizarInventarioDesdeArchivo()

    def actualizarInventarioDesdeArchivo(self):  # Método para actualizar el inventario desde un archivo
        try:
            with open("joyas.txt", "r") as archivo:
                for linea in archivo:
                    info = linea.rstrip().split("-")
                    if len(info) == 5:
                        nombre = info[0]
                        cantidad = int(info[1])
                        precio = float(info[2])
                        material = info[3]
                        descuentoAplicado = info[4] == "True"
                        if descuentoAplicado:
                            porcentaje_descuento = float(input(" "))  # Solicitar porcentaje de descuento
                            joya = DescuentoJoya(nombre, cantidad, precio, material, porcentaje_descuento)
                            joya.aplicar_descuento(porcentaje_descuento)
                        else:
                            joya = JoyeriaFactory.crear_joya(nombre, cantidad, precio, material)
                        self.joyas.append(joya)
        except Exception as e:
            print(f"Error al cargar el inventario desde el archivo: {e}")


    def agregarJoyas(self, joya):  # Método para agregar joyas al inventario
        if isinstance(joya, DescuentoJoya):
            Joyeria.guardar_inventario(joya)
            self.joyas.append(DescuentoJoyaAdapter(joya))
        else:
            self.joyas.append(joya)

    def buscarJoyasPorNombre(self, nombre):  # Método para buscar joyas por nombre
        try:
            joya = next(joya for joya in self.joyas if joya.nombreJoya == nombre)
            return joya
        except StopIteration:
            return None
    def eliminarJoyas(self, nombre):  # Método para eliminar joyas del inventario
        try:
            with open("joyas.txt", "r") as archivo:
                lineas = archivo.readlines()
            with open("joyas.txt", "w") as archivo:
                for linea in lineas:
                    info = linea.rstrip().split("-")
                    if info[0] != nombre:
                        archivo.write(linea)
            print("Joya eliminada con éxito")
        except Exception as e:
            print(f"Error al eliminar joya: {e}")

    def aplicar_descuento_inventario(self, porcentaje):  # Método para aplicar descuento al inventario
        for joya in self.joyas:
            if isinstance(joya, DescuentoJoyaAdapter):
                if hasattr(joya.joya, 'descuentoAplicado') and not joya.joya.descuentoAplicado:
                    joya.aplicar_descuento(porcentaje)
            elif isinstance(joya, DescuentoJoya) and not joya.descuentoAplicado:
                joya.aplicar_descuento(porcentaje)

    def matrizInventario(self):  # Método para mostrar la matriz de inventario
        if self.joyas:
            for joya in self.joyas:
                print(joya)
        else:
            print("No hay joyas en el inventario ")

# Clase para la aplicación de inventario de joyería con GUI
class InventarioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventario de Joyería")
        self.geometry("500x400")

        self.inventario = InventarioJoyas()

        # Add a text widget to display the vector information
        self.texto_vector = tk.Text(self, height=10, width=50)
        self.texto_vector.pack()

        # Button to trigger the display of vector information
        btn_mostrar_vector = tk.Button(self, text="Mostrar Vector", command=self.mostrar_vector)
        btn_mostrar_vector.pack()

    # Method to display the vector information
    def mostrar_vector(self):
        print("Mostrando vector...")  # Debugging statement
        self.texto_vector.delete(1.0, tk.END)  # Clear the text widget
        total_descuento, total_precio = self.vectorJoyas()
        vector_info = f"Total Descuento: ${total_descuento}\nTotal Precio: ${total_precio}\n"
        self.texto_vector.insert(tk.END, vector_info)

    # metodo del vector
    def vectorJoyas(self):
        total_descuento = 0
        total_precio = 0
        vector_info = ""

        try:
            if not path.exists("joyas.txt"):
                vector_info = "No hay datos en el inventario\n"
                return total_descuento, total_precio

            with open("joyas.txt", "r") as archivo:
                lineas = archivo.readlines()

                if not lineas:
                    vector_info = "No hay joyas en el inventario\n"
                    return total_descuento, total_precio

                for linea in lineas:
                    info = linea.rstrip().split("-")
                    if len(info) >= 5:
                        nombre = info[0]
                        cantidad = int(info[1])
                        precio = float(info[2])
                        material = info[3]
                        descuentoAplicado = info[4]

                        vector_info += f"{nombre} - Precio: ${precio} - Cantidad: {cantidad} - Material: {material}"
                        if descuentoAplicado and len(info) >= 6:
                            porcentaje_descuento = float(info[5])
                            vector_info += f" - Descuento: {porcentaje_descuento}%\n"
                            total_descuento += precio * (porcentaje_descuento / 100)

                        total_precio += precio

            return total_descuento, total_precio
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return total_descuento, total_precio
    # Método para buscar joyas por nombre
    def buscar_joyas(self):
        nombre = input("Nombre de la Joya a buscar: ")
        joya_encontrada = self.inventario.buscarJoyasPorNombre(nombre)
        if joya_encontrada:
            self.label_resultado.config(
                text=f"Precio: {joya_encontrada.precio}, Cantidad: {joya_encontrada.cantidad}, Material: {joya_encontrada.material}")
        else:
            self.label_resultado.config(text="No se ha encontrado la joya")

# Clase para la ventana de matriz de inventario
class MatrizInventarioWindow(tk.Toplevel):  # Herencia
    def __init__(self):
        super().__init__()
        self.title("Matriz de Inventario")
        self.geometry("500x400")
        self.mostrar_matriz()

    # Método para mostrar la matriz de inventario en la ventana
    def mostrar_matriz(self):
        if path.isfile("joyas.txt"):
            cont = 0
            matriz = []
            with open("joyas.txt", "r") as archivo:
                for linea in archivo:
                    info = linea.rstrip().split("-")
                    matriz.append(info)
                    cont += 1

            for i in range(cont):
                for j in range(5):
                    label = tk.Label(self, text=matriz[i][j], padx=10, pady=5)
                    label.grid(row=i, column=j)
        else:
            label = tk.Label(self, text="No hay datos en el archivo", padx=10, pady=5)
            label.pack()

# Función para agregar joyas al inventario
def agregar_joyas():
    nombre = input("Ingrese el nombre de la Joya: ")
    cantidad = int(input("Ingrese la cantidad: "))
    precio = float(input("Ingrese el precio: "))
    material = input("Ingrese el material: ")
    tipo_joya = input("¿La joya tiene descuento? (Si/No): ")

    if tipo_joya.upper() == "SI":
        porcentaje_descuento = float(input("Ingrese el porcentaje de descuento: "))
        joya = DescuentoJoya(nombre, cantidad, precio, material, porcentaje_descuento)
        joya.aplicar_descuento(porcentaje_descuento)
    else:
        joya = JoyeriaFactory.crear_joya(nombre, cantidad, precio, material)

    Joyeria.guardar_inventario(joya)
    print("Joya agregada al inventario.")

# Función para eliminar joyas del inventario
def eliminar_joyas():
    nombre = input("Nombre de la Joya a eliminar: ")
    try:
        inventario.eliminarJoyas(nombre)
    except Exception as e:
        print(f"Error al eliminar la joya: {e}")

# Función para buscar joyas por nombre
def buscar_joyas():
    nombre = input("Nombre de la Joya a buscar: ")
    joya_encontrada = inventario.buscarJoyasPorNombre(nombre)
    if joya_encontrada:
        messagebox.showinfo("Información de Joya", f"Nombre: {joya_encontrada.nombreJoya}\n"
                                                   f"Cantidad: {joya_encontrada.cantidad}\n"
                                                   f"Precio: ${joya_encontrada.precio}\n"
                                                   f"Material: {joya_encontrada.material}")
    else:
        messagebox.showerror("Error", "No se ha encontrado la joya")

# Función para mostrar la matriz de inventario
def matrizInventario():
    ventana_matriz = MatrizInventarioWindow()  # Crear una nueva ventana para mostrar la matriz
    ventana_matriz.mainloop()  # Ejecutar el bucle de eventos de la ventana

# Función para salir de la aplicación
def salir():
    print("¡Hasta luego!")
    root.quit()

# Función principal que inicia la aplicación de inventario de joyería
def main():
    global inventario
    inventario = InventarioJoyas()  # Crear una instancia de InventarioJoyas para gestionar el inventario

    global root
    root = tk.Tk()  # Crear la ventana principal de la aplicación
    root.title("Inventario de Joyería")
    root.config(width=400, height=300)

    # Botones para realizar acciones en la interfaz gráfica
    btn_agregar = tk.Button(root, text="Agregar Joyas", command=agregar_joyas)
    btn_agregar.place(x=10, y=10)

    btn_eliminar = tk.Button(root, text="Eliminar Joyas", command=eliminar_joyas)
    btn_eliminar.place(x=130, y=10)

    btn_buscar = tk.Button(root, text="Buscar Joyas", command=buscar_joyas)
    btn_buscar.place(x=250, y=10)

    btn_vector = tk.Button(root, text="Vector de Joyas", command=inventario.vectorJoyas)
    btn_vector.place(x=10, y=40)

    btn_cargar = tk.Button(root, text="Matriz", command=matrizInventario)
    btn_cargar.place(x=130, y=40)

    btn_salir = tk.Button(root, text="Salir", command=salir)
    btn_salir.place(x=250, y=40)

    root.mainloop()  # Iniciar el bucle de eventos de la ventana principal

if __name__ == "__main__":
    main()  # Ejecutar la función principal al ejecutar el script
