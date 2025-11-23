# SISTEMA DE GESTIÓN DE FLOTA - RENT A CAR

def ingresar_devolver_auto(flota):
    """
    Gestiona el ingreso de nuevos autos a la flota o la devolución de unidades.
    Si el modelo ya existe, suma el stock (devolución o compra).
    Si no existe, lo crea.
    """
    modelo = input("Ingrese el modelo del auto (ej. Toyota Yaris): ").strip().title()
    try:
        cant = int(input(f"Cantidad a ingresar/devolver de '{modelo}': "))
        if cant < 0:
            print("Error: No puedes ingresar cantidades negativas.")
            return
        # Lógica principal: Diccionario.get() para evitar errores si no existe
        flota[modelo] = flota.get(modelo, 0) + cant
        print(f"ÉXITO: Stock actualizado. {modelo} = {flota[modelo]} unidades.")
    except ValueError:
        print("Error: Debes ingresar un número entero.(0-9)")

def alquilar_auto(flota):
    """
    Cambia el estado del proceso: Reduce el stock disponible.
    Simula el alquiler de una unidad al cliente.
    """
    modelo = input("Modelo a alquilar: ").strip().title()
    # Verificamos disponibilidad (Stock > 0)
    if flota.get(modelo, 0) > 0:
        flota[modelo] -= 1
        print(f"ALQUILER REALIZADO. Disfrute su {modelo}.")
        print(f"   (Quedan {flota[modelo]} disponibles).")
    else:
        print(f"Lo sentimos, no hay stock disponible de {modelo} o no existe.")

def consultar_disponibilidad(flota):
    """Busca un modelo específico para ver si hay unidades."""
    modelo = input("Modelo a consultar: ").strip().title()
    if modelo in flota:
        print(f"{modelo}: {flota[modelo]} unidades listas para alquilar.")
    else:
        print("El modelo no está en nuestra flota.")

def dar_baja_modelo(flota):
    """Elimina un modelo completamente del sistema (ej. venta de flota antigua)."""
    modelo = input("Modelo a retirar de la flota: ").strip().title()
    if modelo in flota:
        del flota[modelo]
        print(f"El modelo {modelo} ha sido eliminado del sistema.")
    else:
        print("No se encontró ese modelo.")

def ver_flota(flota):
    """Muestra todo el inventario disponible."""
    print("\n--- ESTADO ACTUAL DE LA FLOTA ---")
    if not flota:
        print("(No hay autos registrados en el sistema)")
    else:
        for modelo, cantidad in flota.items():
            estado = "Disponible" if cantidad > 0 else "Agotado"
            print(f"- {modelo}: {cantidad} unidades [{estado}]")
    print("---------------------------------")

def menu_principal():
    """Función de control de flujo (Menú)."""
    flota_autos = {} # Inicialización del (Diccionario)
    
    while True:
        print("\n=== RENT-A-CAR SYSTEM ===")
        print("1) Ingresar/Devolver Auto (Stock)")
        print("2) Alquilar Auto (Cliente)")
        print("3) Consultar Disponibilidad")
        print("4) Dar de baja Modelo")
        print("5) Ver Flota Completa")
        print("0) Salir")
        
        op = input(">> Seleccione opción: ").strip()
        
        if op == "1": ingresar_devolver_auto(flota_autos)
        elif op == "2": alquilar_auto(flota_autos)
        elif op == "3": consultar_disponibilidad(flota_autos)
        elif op == "4": dar_baja_modelo(flota_autos)
        elif op == "5": ver_flota(flota_autos)
        elif op == "0": 
            print("Cerrando sistema... :)")
            break
        else: 
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu_principal()