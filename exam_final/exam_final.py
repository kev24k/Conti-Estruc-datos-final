# examen_final.py

class NodoPaciente:
    def __init__(self, dni, nombre, prioridad):
        self.dni = dni              # int
        self.nombre = nombre        # str
        self.prioridad = prioridad  # int (1 = baja, 2 = media, 3 = alta)
        self.izq = None
        self.der = None


def insertar_paciente(raiz, paciente):
    """Inserta un paciente en el ABB ordenado por dni."""
    if raiz is None:
        return paciente

    if paciente.dni < raiz.dni:
        raiz.izq = insertar_paciente(raiz.izq, paciente)
    elif paciente.dni > raiz.dni:
        raiz.der = insertar_paciente(raiz.der, paciente)
    return raiz


def cargar_pacientes_desde_archivo(ruta_archivo):
    """Lee el archivo pacientes.txt y construye el ABB de pacientes."""
    raiz = None
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea: continue
                partes = linea.split(";")
                if len(partes) != 3: continue

                dni_str, nombre, prioridad_str = partes
                try:
                    dni = int(dni_str)
                    prioridad = int(prioridad_str)
                except ValueError:
                    continue

                nuevo = NodoPaciente(dni, nombre, prioridad)
                raiz = insertar_paciente(raiz, nuevo)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_archivo}")
    return raiz


# =======================
# FUNCIONES IMPLEMENTADAS
# =======================

def buscar_paciente(raiz, dni_busqueda):
    """
    Busca un paciente por DNI.
    Devuelve el nodo si existe, o None si no.
    """
    if raiz is None:
        return None
    
    if dni_busqueda == raiz.dni:
        return raiz
    elif dni_busqueda < raiz.dni:
        return buscar_paciente(raiz.izq, dni_busqueda)
    else:
        return buscar_paciente(raiz.der, dni_busqueda)


def mostrar_pacientes_inorden(raiz):
    """
    Recorre el ABB en inorden (Izquierda - Raíz - Derecha).
    """
    if raiz is not None:
        mostrar_pacientes_inorden(raiz.izq)
        print(f"DNI: {raiz.dni} | Nombre: {raiz.nombre} | Prioridad: {raiz.prioridad}")
        mostrar_pacientes_inorden(raiz.der)


def generar_reporte_prioridad_alta(raiz, ruta_salida, prioridad_minima):
    """
    Genera un archivo con pacientes de prioridad >= prioridad_minima.
    Incluye conteo total al final.
    """
    contador = 0
    
    # 1. Abrir en modo escritura ("w") para crear/limpiar el archivo
    try:
        with open(ruta_salida, "w", encoding="utf-8") as f:
            
            # Función interna auxiliar para recorrer y escribir
            def _recorrer_escribir(nodo):
                nonlocal contador # Para modificar la variable externa
                if nodo:
                    _recorrer_escribir(nodo.izq)
                    
                    if nodo.prioridad >= prioridad_minima:
                        f.write(f"{nodo.dni};{nodo.nombre};{nodo.prioridad}\n")
                        contador += 1
                        
                    _recorrer_escribir(nodo.der)
            
            # Iniciar recorrido
            _recorrer_escribir(raiz)
            
        # 2. Abrir en modo append ("a") para el resumen
        with open(ruta_salida, "a", encoding="utf-8") as f:
            f.write(f"TOTAL_PACIENTES_REPORTE:{contador}\n")
            
        print(f"Reporte generado exitosamente en: {ruta_salida}")
        print(f"Total de pacientes exportados: {contador}")

    except IOError as e:
        print(f"Error al escribir el archivo: {e}")


def contar_pacientes_hoja(raiz):
    """
    Devuelve la cantidad de nodos hoja (sin hijos).
    """
    if raiz is None:
        return 0
    
    # Si no tiene hijo izquierdo NI derecho, es una hoja
    if raiz.izq is None and raiz.der is None:
        return 1
    
    # Si tiene algún hijo, sumamos las hojas de ambos lados
    return contar_pacientes_hoja(raiz.izq) + contar_pacientes_hoja(raiz.der)


# =======================
# MENÚ PRINCIPAL MODIFICADO
# =======================

def mostrar_menu():
    print("\n=== Menú - Gestión de pacientes ===")
    print("1. Buscar paciente por DNI")
    print("2. Listar pacientes ordenados por DNI (inorden)")
    print("3. Generar reporte por Prioridad")
    print("4. Mostrar cantidad de pacientes hoja")
    print("0. Salir")


def main():
    ruta_pacientes = "pacientes.txt"
    raiz = cargar_pacientes_desde_archivo(ruta_pacientes)

    if raiz is None:
        print("No se pudo cargar el arbol. Verifique que 'pacientes.txt' exista.")
    else:
        print(f"Árbol cargado. Raíz del árbol: {raiz.dni}")

    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            # MODIFICADO: Ahora pide DNI y busca en el árbol
            try:
                dni_input = int(input("Ingrese el DNI a buscar: "))
                nodo = buscar_paciente(raiz, dni_input)
                if nodo:
                    print(f"\n[ENCONTRADO] {nodo.nombre} (DNI: {nodo.dni}, Prioridad: {nodo.prioridad})")
                else:
                    print("\n[NO ENCONTRADO] El paciente no está en el registro.")
            except ValueError:
                print("Error: El DNI debe ser un número entero.")

        elif opcion == "2":
            # MODIFICADO: Llama a la función inorden
            print("\n--- Listado de Pacientes (Ordenado por DNI) ---")
            mostrar_pacientes_inorden(raiz)

        elif opcion == "3":
            # MODIFICADO: Pide prioridad y genera archivo
            try:
                prio = int(input("Ingrese prioridad mínima (1, 2 o 3): "))
                nombre_archivo = "reporte_prioridad.txt"
                generar_reporte_prioridad_alta(raiz, nombre_archivo, prio)
            except ValueError:
                print("Error: La prioridad debe ser un número.")

        elif opcion == "4":
            # MODIFICADO: Muestra hojas
            hojas = contar_pacientes_hoja(raiz)
            print(f"\nCantidad de pacientes 'hoja' (sin hijos) en el árbol: {hojas}")

        elif opcion == "0":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()