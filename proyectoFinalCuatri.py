import datetime
import random
import re

class Usuario:
    def __init__(self, cedula, nombre, fecha_nacimiento, sexo, residencia, tipo_usuario, contrasena):
        self.cedula = cedula
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = self.calcular_edad()
        self.sexo = sexo
        self.residencia = residencia
        self.tipo_usuario = tipo_usuario
        self.contrasena = contrasena

    def calcular_edad(self):
        hoy = datetime.date.today()
        nacimiento = datetime.datetime.strptime(self.fecha_nacimiento, "%d/%m/%Y").date()
        return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
    
    def __str__(self):
        return (f"Tipo Usuario: {self.tipo_usuario}, Cedula: {self.cedula}, Nombre: {self.nombre}, Sexo: {self.sexo}, "
                f"Fecha Nacimiento: {self.fecha_nacimiento}, Edad: {self.edad}, Residencia: {self.residencia}")


class Ciudadano(Usuario):
    def __init__(self, cedula, nombre, fecha_nacimiento, sexo, residencia, contrasena):
        super().__init__(cedula, nombre, fecha_nacimiento, sexo, residencia, 'Ciudadano', contrasena)
        self.vehiculos = []

class OficialTransito(Usuario):
    def __init__(self, cedula, nombre, fecha_nacimiento, sexo, residencia, contrasena):
        super().__init__(cedula, nombre, fecha_nacimiento, sexo, residencia, 'Oficial de Transito', contrasena)

class OficinaJuzgado(Usuario):
    def __init__(self, cedula, nombre, fecha_nacimiento, sexo, residencia, contrasena):
        super().__init__(cedula, nombre, fecha_nacimiento, sexo, residencia, 'Oficina del Juzgado', contrasena)

class Administrador(Usuario):
    def __init__(self, cedula, nombre, fecha_nacimiento, sexo, residencia, contrasena):
        super().__init__(cedula, nombre, fecha_nacimiento, sexo, residencia, 'Administrador', contrasena)

class Vehiculo:
    def __init__(self, cedula_propietario, placa, anio, marca, color, tipo):
        self.cedula_propietario = cedula_propietario
        self.placa = placa
        self.anio = anio
        self.marca = marca
        self.color = color
        self.tipo = tipo
    
    def __str__(self):
        return (f"Propietario: {self.cedula_propietario}, Placa: {self.placa}, Año: {self.anio}, "
                f"Marca: {self.marca}, Color: {self.color}, Tipo: {self.tipo}")

class Evento:
    def __init__(self, usuario, lugar, placa, calcular_multa=True):
        self.codigo = random.randint(10000, 99999)
        self.usuario = usuario
        self.lugar = lugar
        self.placa = placa
        self.estado = 'Abierto'
        self.fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if calcular_multa:
            self.multa = self.calcular_multa()
        self.nombre_oficial = None
        self.numero_parte = None
        self.nombre_juzgado = None
        self.numero_registro = None

    def __str__(self):
        return (f"Codigo: {self.codigo}, Nombre de usuario: {self.usuario}, Lugar del incidente: {self.lugar}, "
                f"Placa: {self.placa}, Estado: {self.estado}, Fecha: {self.fecha_hora}, Multa: {self.multa}, "
                f"Nombre del Oficial: {self.nombre_oficial}, Numero de parte: {self.numero_parte}, "
                f"Nombre Oficina del Juzgado: {self.nombre_juzgado}, Numero de registro: {self.numero_registro}")

    def calcular_multa(self):#This function calculates the price of fines based on vehicle data
        vehiculo=vehiculos[self.placa]
        tipo_vehiculo=vehiculo.tipo
        resultado_multa=0
        for multa in multas:
            if tipo_vehiculo==multa["Tipo vehiculo"]:
                resultado_multa=multa["Valor de la multa"]+multa["Valor de la multa"]*multa["Impuesto"]
                if int(vehiculo.anio)<2000:
                    resultado_multa+=resultado_multa*0.10
                break
        print(f"El monto de su multa es de: {resultado_multa}")
        return resultado_multa

# Dictionaries to store data
provincias = {
    "San Jose": ["Escazu", "Desamparados"],
    "Alajuela": ["San Carlos", "Grecia"],
    "Cartago": ["Turrialba", "Paraiso"],
    "Heredia": ["San Rafael", "Belen"]
}

multas = []
usuarios = {}
vehiculos = {}
eventos = {}
usuario_actual = None

def cargar_info_multas():#The information about the fines is loaded from a txt file
    global multas
    archivo = open("multas.txt")
    for linea in archivo.readlines():
        info_multa = linea.split(",")
        multa = {
            "Tipo vehiculo": info_multa[0],
            "Valor de la multa":int(info_multa[1]),
            "Impuesto": float(info_multa[2])
        }

        multas.append(multa)

# Create the admin 
admin = Administrador("admin", "Administrador", "01/01/1980", "M", "San Jose", "admin123")
usuarios[admin.cedula] = admin

# function to verify accessn certain areas of the code
def verificar_acceso(tipos_permitidos):
    if usuario_actual.tipo_usuario not in tipos_permitidos:
        print("Acceso denegado.")
        return False
    return True

def entrada_entero(mensaje):#This function validates that the data input is integers
    try:
        return int(input(mensaje))
    except ValueError:
        print("Entrada invalida. Debe ser un numero entero.")
        return None

def agregar_provincia(provincia): #function to add provinces
    if provincia not in provincias:
        provincias[provincia] = []
    else:
        print("La provincia ya existe.")

def eliminar_provincia(provincia):#function to delete provinces
    if provincia in provincias and not any(provincia == evento.lugar.split(' / ')[0] for evento in eventos.values()):
        del provincias[provincia]
    else:
        print("La provincia no existe o esta asignada a un evento.")

def agregar_canton(provincia, canton):#function to add canton
    if provincia in provincias and canton not in provincias[provincia]:
        provincias[provincia].append(canton)
    else:
        print("La provincia no existe o el canton ya existe en esta provincia.")

def eliminar_canton(provincia, canton):#function to delete canton
    if provincia in provincias and canton in provincias[provincia] and not any(canton == evento.lugar.split(' / ')[1] for evento in eventos.values()):
        provincias[provincia].remove(canton)
    else:
        print("La provincia o el canton no existe o esta asignado a un evento.")

def seleccionar_provincia_canton(mensaje):#This function is used to choose a province
    while True:
        try:
            print(mensaje)
            print("Provincias")
            for posicion, provincia in enumerate(provincias):
                print(f"{posicion+1}. {provincia}")

            opcion_provinicia = int(input("Eliga una provincia: "))
            if opcion_provinicia >= 1 and opcion_provinicia <= len(provincias):
                lista_provincias = list(provincias.keys())
                provincia_elegida = lista_provincias[opcion_provinicia - 1]
                break
            print("Opcion incorrecta.")
            
        except ValueError:
            print("Opcion incorrecta.")

    while True:
        try:
            print("Cantones")
            for posicion, canton in enumerate(provincias[provincia_elegida]):
                print(f"{posicion+1}. {canton}")

            opcion_canton = int(input("Eliga un canton: "))
            if opcion_canton >= 1 and opcion_canton <= len(provincias[provincia_elegida]):
                canton_elegido = provincias[provincia_elegida][opcion_canton - 1]
                break
            print("Opcion incorrecta.")
            
        except ValueError:
            print("Opcion incorrecta.")
    
    return f"{provincia_elegida} / {canton_elegido}"
    

def agregar_usuario(usuario):#function to add a user 
    if usuario.cedula not in usuarios and usuario.edad >= 18:
        usuarios[usuario.cedula] = usuario
    else:
        print("El usuario ya existe o es menor de 18 años.")

def eliminar_usuario(cedula):#function to delete user
    if cedula in usuarios:
        del usuarios[cedula]
    else:
        print("El usuario no existe.")

#function used for mod a user
def modificar_usuario(cedula, nombre=None, fecha_nacimiento=None, sexo=None, residencia=None, contrasena=None):
    if cedula in usuarios:
        usuario = usuarios[cedula]
        usuario.nombre = nombre or usuario.nombre
        usuario.fecha_nacimiento = fecha_nacimiento or usuario.fecha_nacimiento
        usuario.edad = usuario.calcular_edad()
        usuario.sexo = sexo or usuario.sexo
        usuario.residencia = residencia or usuario.residencia
        usuario.contrasena = contrasena or usuario.contrasena
    else:
        print("El usuario no existe.")

def mostrar_usuarios():#this function show the user in the system
    print("Usuarios")
    for usuario in usuarios.values():
        print(usuario)

def selecionar_tipo_usuario():# this function used for choose the user type
    tipos_usuario = ["Ciudadano", "Oficial de Transito", "Oficina del Juzgado", "Administrador"]
    while True:
        try:
            opcion = int(input("1.Ciudadano\n2.Oficial de Transito\n3.Oficina del Juzgado\n4.Administrador\nSeleccione el tipo de usuario: "))
            if 1 <= opcion <= 4:
                return tipos_usuario[opcion - 1]
            print("Ingrese una opcion valida")
        except ValueError:
            print("Ingrese una opcion valida")

def cambiar_usuario():#this function used for change user
    global usuario_actual
    cedula = input("Ingrese la cedula del usuario: ")
    contrasena = input("Ingrese la contraseña: ")
    if cedula in usuarios and usuarios[cedula].contrasena == contrasena:
        usuario_actual = usuarios[cedula]
        print(f"Sesion iniciada como {usuario_actual.nombre} ({usuario_actual.tipo_usuario})")
    else:
        print("Cedula o contraseña incorrecta.")

def agregar_vehiculo(vehiculo):#this function is used for add vehicles
    cedulas = [usuario.cedula for usuario in usuarios.values()]
    if not vehiculo.cedula_propietario in cedulas:
        print("Este usuario no existe.")
        return

    patron = re.compile(r'^[A-Z]{3}-\d{3}$')
    if vehiculo.placa not in vehiculos and patron.match(vehiculo.placa):
        vehiculos[vehiculo.placa] = vehiculo
    else:
        print("El vehiculo ya existe o la placa es incorrecta.")

def eliminar_vehiculo(placa):#this function is used for delete vehicles
    if placa in vehiculos:
        del vehiculos[placa]
    else:
        print("El vehiculo no existe.")

#this function is used for mod a vehicles
def modificar_vehiculo(placa, cedula_propietario=None, anio=None, marca=None, color=None, tipo=None):
    if placa in vehiculos:
        vehiculo = vehiculos[placa]
        vehiculo.cedula_propietario = cedula_propietario or vehiculo.cedula_propietario
        vehiculo.anio = anio or vehiculo.anio
        vehiculo.marca = marca or vehiculo.marca
        vehiculo.color = color or vehiculo.color
        vehiculo.tipo = tipo or vehiculo.tipo
    else:
        print("El vehiculo no existe o la placa es incorrecta.")

def mostrar_vehiculos():#this function is   used for show vehicle
    print("Vehiculos")
    for vehiculo in vehiculos.values():
        print(vehiculo)

def validar_tipo_vehiculo():#This function is used to validate the vehicle type
    while True:
        try:
            tipos = ["moto","carro","bus","camion"]
            tipo_elegido = int(input("Tipos de vehiculo\n1.moto\n2.carro\n3.bus\n4.camion\nIngrese el tipo: "))
            
            if 1 <= tipo_elegido <= 4:
                return tipos[tipo_elegido - 1]
            print("Opcion incorrecta.")
        except ValueError:
            print("Opcion incorrecta.")

def agregar_evento(usuario, lugar, placa):#this function is used to add a event
    if not verificar_acceso(['Ciudadano']):
        return
    evento = Evento(usuario, lugar, placa)
    if evento.placa in vehiculos and vehiculos[evento.placa].cedula_propietario == usuario:
        if not any(e.placa == evento.placa for e in eventos.values()):
            eventos[evento.codigo] = evento
            print(f"Evento creado: {evento}")
        else:
            print("El vehiculo ya tiene un evento asociado.")
    else:
        print("El vehiculo no pertenece al ciudadano logueado o no existe.")

def eliminar_evento(codigo):#this function is used to remove a event
    if not verificar_acceso(['Ciudadano']):
        return
    if codigo in eventos and eventos[codigo].usuario == usuario_actual.cedula and eventos[codigo].estado == 'Abierto':
        del eventos[codigo]
        print("Evento eliminado.")
    else:
        print("El evento no existe, no pertenece al usuario actual o no esta en estado Abierto.")

def modificar_evento(codigo, lugar=None, placa=None, multa=None):#this function is used to mod a event
    if not verificar_acceso(['Ciudadano']):
        return
    if codigo in eventos and eventos[codigo].usuario == usuario_actual.cedula and eventos[codigo].estado == 'Abierto':
        evento = eventos[codigo]
        evento.lugar = lugar or evento.lugar
        evento.placa = placa or evento.placa
        try:
            evento.multa = int(multa) if multa else evento.multa
        except ValueError:
            print("Error: La multa debe ser un numero entero.")
            return
        print(f"Evento modificado: {evento}")
    else:
        print("El evento no existe, no pertenece al usuario actual o no esta en estado Abierto.")

def aprobar_evento(codigo, nombre_oficial):#this function is used to aprove a event 
    if not verificar_acceso(['Oficial de Transito']):
        return
    if codigo in eventos:
        evento = eventos[codigo]
        if evento.estado == 'Abierto' and (datetime.datetime.now() - datetime.datetime.strptime(evento.fecha_hora, "%d/%m/%Y %H:%M:%S")).seconds > 30:
            evento.nombre_oficial = nombre_oficial
            evento.numero_parte = random.randint(1000, 9999)
            evento.estado = 'Por aprobar'
            evento.fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"Evento aprobado: {evento}")
        else:
            print("El evento no se puede aprobar porque no esta en estado Abierto o no han pasado 30 segundos desde su creacion.")
    else:
        print("El evento no existe.")

def completar_evento(codigo, nombre_juzgado, numero_registro):#fucntion for complete a event 
    if not verificar_acceso(['Oficina del Juzgado']):
        return
    if codigo in eventos and eventos[codigo].estado == 'Por aprobar':
        evento = eventos[codigo]
        evento.nombre_juzgado = nombre_juzgado
        evento.numero_registro = numero_registro
        evento.estado = 'Completo'
        evento.fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        guardar_evento_archivo(evento)
        print(f"Evento completado: {evento}")
    else:
        print("El evento no existe o no esta en estado Por aprobar.")

def mostrar_eventos(usuario):#this function is used to show the events
    print('Eventos')
    for evento in eventos.values():
        fecha_hora = datetime.datetime.strptime(evento.fecha_hora,"%d/%m/%Y %H:%M:%S")
        segundos_diferencia = datetime.datetime.now() - fecha_hora

        if usuario.tipo_usuario == 'Ciudadano' and usuario.cedula == evento.usuario:
            print(evento)
        elif usuario.tipo_usuario == 'Oficial de Transito' and evento.estado == 'Abierto' and segundos_diferencia.total_seconds() >= 30:
            print(evento)
        elif usuario.tipo_usuario == 'Oficina del Juzgado' and evento.estado == 'Por aprobar':
            print(evento)

def guardar_evento_archivo(evento):#this function is used to save the ass a file 
    with open("eventos_completos.txt", "a") as archivo:
        archivo.write(f"{evento}\n")

def generar_reporte_archivo():#fucntion for  generate a report
    with open("reporte_eventos.txt", "w") as archivo:
        archivo.write("Eventos registrados:\n")
        for evento in eventos.values():
            archivo.write(f"{evento}\n")
    print("Reporte generado en reporte_eventos.txt")

#function that contains menu options 
def menu_principal():
    menus = {
        '1': menu_provincias_cantones,
        '2': menu_usuarios,
        '3': menu_vehiculos,
        '4': menu_eventos,
        '5': menu_reportes,
        '6': cambiar_usuario
    }
    while True:
        print("\n--- Menu Principal ---")
        print("1. Administrar Provincias y Cantones")
        print("2. Administrar Usuarios")
        print("3. Administrar Vehiculos")
        print("4. Administrar Eventos")
        print("5. Reportes")
        print("6. Cambiar Usuario")
        print("7. Salir")
        opcion = input("Seleccione una opcion: ")
        if opcion == '7':
            break
        elif opcion in menus:
            menus[opcion]()
        else:
            print("Opcion no valida.")

# Submenus
def menu_provincias_cantones():#menu that contains options for the administration
    if not verificar_acceso(['Administrador']):
        return
    while True:
        print("\n--- Administrar Provincias y Cantones ---")
        opcion = input("1. Agregar Provincia\n2. Eliminar Provincia\n3. Agregar Canton\n4. Eliminar Canton\n5. Volver al Menu Principal\nSeleccione una opcion: ")
        if opcion == '1':
            agregar_provincia(input("Ingrese el nombre de la provincia: "))
        elif opcion == '2':
            eliminar_provincia(input("Ingrese el nombre de la provincia: "))
        elif opcion == '3':
            agregar_canton(input("Ingrese el nombre de la provincia: "), input("Ingrese el nombre del canton: "))
        elif opcion == '4':
            eliminar_canton(input("Ingrese el nombre de la provincia: "), input("Ingrese el nombre del canton: "))
        elif opcion == '5':
            break
        else:
            print("Opcion no valida.")

def validar_sexo():#function for validade sex 
    while True:
        sexo_usuario = input("Ingrese el sexo (M/F): ").upper()
        if sexo_usuario == "M" or sexo_usuario == "F":
            return sexo_usuario
        print("El sexo elegido es incorrecto.")


def menu_usuarios():#function that contains data for add new users
    if not verificar_acceso(['Administrador']):
        return
    while True:
        print("\n--- Administrar Usuarios ---")
        opcion = input("1. Agregar Usuario\n2. Eliminar Usuario\n3. Modificar Usuario\n4. Mostrar Usuarios\n5. Volver al Menu Principal\nSeleccione una opcion: ")
        if opcion == '1':
            try:
                agregar_usuario(Usuario(
                    cedula=input("Ingrese la cedula: "),
                    nombre=input("Ingrese el nombre: "),
                    fecha_nacimiento=input("Ingrese la fecha de nacimiento (dd/mm/yyyy): "),
                    sexo=validar_sexo(),
                    residencia=seleccionar_provincia_canton("Seleccione el lugar de residencia"),
                    tipo_usuario=selecionar_tipo_usuario(),
                    contrasena=input("Ingrese la contraseña: ")
                ))
            except Exception as e:
                print(f"Error al agregar usuario: {e}")
        elif opcion == '2':
            eliminar_usuario(input("Ingrese la cedula del usuario a eliminar: "))
        elif opcion == '3':
            modificar_usuario(
                cedula=input("Ingrese la cedula del usuario a modificar: "),
                nombre=input("Ingrese el nuevo nombre (o presione Enter para mantener el actual): ") or None,
                fecha_nacimiento=input("Ingrese la nueva fecha de nacimiento (dd/mm/yyyy) (o presione Enter para mantener la actual): ") or None,
                sexo=validar_sexo(),
                residencia=seleccionar_provincia_canton("Seleccione el lugar de residencia"),
                contrasena=input("Ingrese la nueva contraseña (o presione Enter para mantener la actual): ") or None
            )
        elif opcion == '4':
            mostrar_usuarios()
        elif opcion == '5':
            break
        else:
            print("Opcion no valida.")

def menu_vehiculos():#menu that contains data for vehicle
    if not verificar_acceso(['Ciudadano']):
        return
    while True:
        print("\n--- Administrar Vehiculos ---")
        opcion = input("1. Agregar Vehiculo\n2. Eliminar Vehiculo\n3. Modificar Vehiculo\n4. Mostrar Vehiculo\n5. Volver al Menu Principal\nSeleccione una opcion: ")
        if opcion == '1':
            try:
                agregar_vehiculo(Vehiculo(
                    cedula_propietario=input("Ingrese la cedula del propietario: "),
                    placa=input("Ingrese la placa: ").upper(),
                    anio=input("Ingrese el año: "),
                    marca=input("Ingrese la marca: "),
                    color=input("Ingrese el color: "),
                    tipo=validar_tipo_vehiculo()
                ))
            except Exception as e:
                print(f"Error al agregar vehiculo: {e}")
        elif opcion == '2':
            eliminar_vehiculo(input("Ingrese la placa del vehiculo a eliminar: ").upper())
        elif opcion == '3':
            modificar_vehiculo(
                placa=input("Ingrese la placa del vehiculo a modificar: ").upper(),
                cedula_propietario=input("Ingrese la nueva cedula del propietario (o presione Enter para mantener la actual): ") or None,
                anio=input("Ingrese el nuevo año (o presione Enter para mantener el actual): ") or None,
                marca=input("Ingrese la nueva marca (o presione Enter para mantener la actual): ") or None,
                color=input("Ingrese el nuevo color (o presione Enter para mantener el actual): ") or None,
                tipo=validar_tipo_vehiculo()
            )
        elif opcion == '4':
            mostrar_vehiculos()
        elif opcion == '5':
            break
        else:
            print("Opcion no valida.")

def menu_eventos():#menu that contains options about the events
    if verificar_acceso(['Ciudadano', 'Oficial de Transito', 'Oficina del Juzgado']):
        while True:
            print("\n--- Administrar Eventos ---")
            opcion = input("1. Agregar Evento\n2. Eliminar Evento\n3. Modificar Evento\n4. Aprobar Evento\n5. Completar Evento\n6. Mostrar Evento\n7. Volver al Menu Principal\nSeleccione una opcion: ")
            if opcion == '1':
                if verificar_acceso(['Ciudadano']):
                    agregar_evento(
                        usuario_actual.cedula,
                        seleccionar_provincia_canton("Seleccione el lugar del incidente"),
                        input("Ingrese la placa del vehiculo: ").upper()
                    )
            elif opcion == '2':
                if verificar_acceso(['Ciudadano']):
                    eliminar_evento(entrada_entero("Ingrese el codigo del evento a eliminar: "))
            elif opcion == '3':
                if verificar_acceso(['Ciudadano']):
                    modificar_evento(
                        entrada_entero("Ingrese el codigo del evento a modificar: "),
                        lugar=seleccionar_provincia_canton("Seleccione el lugar del incidente"),
                        placa=input("Ingrese la nueva placa del vehiculo (o presione Enter para mantener la actual): ") or None,
                        multa=entrada_entero("Ingrese la nueva multa (o presione Enter para mantener la actual): ") or None
                    )
            elif opcion == '4':
                if verificar_acceso(['Oficial de Transito']):
                    aprobar_evento(entrada_entero("Ingrese el codigo del evento a aprobar: "), input("Ingrese el nombre del oficial de transito: "))
            elif opcion == '5':
                if verificar_acceso(['Oficina del Juzgado']):
                    completar_evento(
                        entrada_entero("Ingrese el codigo del evento a completar: "),
                        input("Ingrese el nombre de la persona de la oficina del juzgado: "),
                        entrada_entero("Ingrese el numero de registro: ")
                    )
            elif opcion == '6':
                mostrar_eventos(usuario_actual)
            elif opcion == '7':
                break
            else:
                print("Opcion no valida.")

def menu_reportes():#menu for view data about reports 
    if verificar_acceso(['Administrador']):
        while True:
            print("\n--- Reportes ---")
            opcion = input("1. Generar reporte en archivo\n2. Cantones ordenados alfabeticamente\n3. Personas registradas ordenadas por edad\n4. Cantidad de hombres y mujeres\n5. Cantidad de hombres por provincia\n6. Cantidad de mujeres por canton\n7. Vehiculos ordenados por tipo\n8. Eventos con multas mayores a 45,000 colones (estado Por aprobar)\n9. Eventos completos, ordenados por fecha\n10. Eventos abiertos antes de una hora especifica\n11. Provincia con mas y menos incidentes\n12. Volver al Menu Principal\nSeleccione una opcion: ")
            if opcion == '1':
                generar_reporte_archivo()
            elif opcion == '2':
                reporte_cantones_alfabeticamente()
            elif opcion == '3':
                reporte_personas_por_edad()
            elif opcion == '4':
                reporte_hombres_mujeres()
            elif opcion == '5':
                reporte_hombres_por_provincia()
            elif opcion == '6':
                reporte_mujeres_por_canton()
            elif opcion == '7':
                reporte_vehiculos_por_tipo()
            elif opcion == '8':
                reporte_multas_mayores()
            elif opcion == '9':
                reporte_eventos_completos()
            elif opcion == '10':
                hora = input("Ingrese la hora (HH:MM): ")
                reporte_eventos_abiertos_antes_hora(hora)
            elif opcion == '11':
                reporte_provincias_incidentes()
            elif opcion == '12':
                break
            else:
                print("Opcion no valida.")

# Funciones para los reportes
def reporte_cantones_alfabeticamente():#function to see the cantons alphabetically
    cantones_ordenados = sorted([(provincia, canton) for provincia in provincias for canton in provincias[provincia]], key=lambda x: x[1])
    for provincia, canton in cantones_ordenados:
        print(f"{canton} - {provincia}")

def reporte_personas_por_edad():#function to view user by age 
    personas_ordenadas = sorted(usuarios.values(), key=lambda x: x.edad, reverse=True)
    for persona in personas_ordenadas:
        print(f"{persona.nombre} - {persona.edad} años")

def reporte_hombres_mujeres():#function to view reports for mans and womans 
    hombres = sum(1 for usuario in usuarios.values() if usuario.sexo == 'M')
    mujeres = sum(1 for usuario in usuarios.values() if usuario.sexo == 'F')
    print(f"Hombres: {hombres}, Mujeres: {mujeres}")

def reporte_hombres_por_provincia():#function to see how many men exist per province
    hombres_por_provincia = {}
    for usuario in usuarios.values():
        if usuario.sexo == 'M':
            provincia_canton = usuario.residencia.split(' / ')
            provincia = provincia_canton[0]
            hombres_por_provincia[provincia] = hombres_por_provincia.get(provincia, 0) + 1
    for provincia, cantidad in hombres_por_provincia.items():
        print(f"{provincia}: {cantidad} hombres")

def reporte_mujeres_por_canton():#function to see how many womans exist per canton
    mujeres_por_canton = {}
    for usuario in usuarios.values():
        if usuario.sexo == 'F':
            provincia_canton = usuario.residencia.split(' / ')
            canton = provincia_canton[1]
            mujeres_por_canton[canton] = mujeres_por_canton.get(canton, 0) + 1
    for canton, cantidad in mujeres_por_canton.items():
        print(f"{canton}: {cantidad} mujeres")

def reporte_vehiculos_por_tipo():#This function is responsible for generating a report that categorizes vehicles based on their type
    vehiculos_por_tipo = {
        'moto' : [],
        'carro': [],
        'bus' : [],
        'camion' : []
    }
    for vehiculo in vehiculos.values():
            vehiculos_por_tipo[vehiculo.tipo].append(vehiculo)
    for tipo, tipo_vehiculos in vehiculos_por_tipo.items():
        print(f"Tipo: {tipo}")
        for vehiculo in tipo_vehiculos:
            print(f"Placa: {vehiculo.placa}, Marca:{vehiculo.marca}")

def reporte_multas_mayores():#This function is responsible for generating a report that lists all events where the multa is greater than 45,000 colones and the event is still in the 'Por aprobar' state.
    eventos_multas_mayores = [evento for evento in eventos.values() if evento.multa > 45000 and evento.estado == 'Por aprobar']
    for evento in eventos_multas_mayores:
        print(f"{evento.fecha_hora}: Codigo: {evento.codigo}, Usuario: {evento.usuario}, Multa: {evento.multa} colones")

def reporte_eventos_completos():#unction, which is responsible for generating a report that lists all completed events.
    eventos_completos = []
    with open("eventos_completos.txt", 'r') as archivo:
            for line in archivo:
                valores = {}
                datos = line.split(', ')
                for dato in datos:
                    info = dato.split(': ')
                    valores[info[0]] = info[1]
                
                evento = Evento(
                    valores['Nombre de usuario'],
                    valores['Lugar del incidente'],
                    valores['Placa'],
                    False
                )
                evento.codigo = int(valores['Codigo'])
                evento.estado = valores['Estado']
                evento.fecha_hora = valores['Fecha']
                evento.numero_parte = valores['Numero de parte']

                eventos_completos.append(evento)


    eventos_completos.sort(key=lambda x: datetime.datetime.strptime(x.fecha_hora, "%d/%m/%Y %H:%M:%S"))
    for evento in eventos_completos:
        print(f"{evento.fecha_hora}: {evento.codigo} - Estado: {evento.estado}, Cedula: {evento.usuario}, Numero de Parte: {evento.numero_parte}, Lugar de choque: {evento.lugar}")

def reporte_eventos_abiertos_antes_hora(hora):# This function is responsible for generating a report that lists all open events that occurred before a specific time.
    try:
        hora_especifica = datetime.datetime.strptime(hora, "%H:%M").time()
        eventos_abiertos = [evento for evento in eventos.values() if evento.estado == 'Abierto']
        for evento in eventos_abiertos:
            evento_hora = datetime.datetime.strptime(evento.fecha_hora.split(" ")[1], "%H:%M:%S").time()
            if evento_hora < hora_especifica:
                print(f"{evento.fecha_hora}: {evento.codigo} - {evento.estado}")
    except ValueError:
        print("Hora invalida. Por favor, use el formato HH:MM.")

def reporte_provincias_incidentes():#This function is responsible for generating a report that categorizes incidents (events) based on the province where they occurred.
    incidentes_por_provincia = {}
    for evento in eventos.values():
        provincia = evento.lugar.split(' / ')[0]
        incidentes_por_provincia[provincia] = incidentes_por_provincia.get(provincia, 0) + 1
    max_incidentes = max(incidentes_por_provincia.values())
    min_incidentes = min(incidentes_por_provincia.values())
    provincia_max_incidentes = [prov for prov, inc in incidentes_por_provincia.items() if inc == max_incidentes]
    provincia_min_incidentes = [prov for prov, inc in incidentes_por_provincia.items() if inc == min_incidentes]
    print(f"Provincia(s) con mas incidentes: {', '.join(provincia_max_incidentes)} con {max_incidentes} incidentes")
    print(f"Provincia(s) con menos incidentes: {', '.join(provincia_min_incidentes)} con {min_incidentes} incidentes")

# Ejecucion del programa
if __name__ == "__main__":
    usuario_actual = admin  # Iniciar sesion como el administrador
    cargar_info_multas()
    menu_principal()
