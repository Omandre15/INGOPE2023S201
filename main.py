import bom.controlador as bom_controlador
import bom.vista as bom_vista
import materia_prima.controlador as materia_prima_controlador
import materia_prima.vista as materia_prima_vista
import producto.controlador as producto_controlador
import producto.vista as producto_vista
import main.vista as vista_principal
import config.db as db
import PySimpleGUI as psg
import random


def main():
    conn = db.crear_conexion()
    if db.verificar_base_nueva(conn):
        db.crear_tablas(conn)
        salida = psg.popup_yes_no('Se acaba de crear una base de datos','¿Desea cargar datos de prueba?',title='Datos por defecto')
        if 'Yes' == salida:
            db.carga_datos_prueba(conn)

    main_window = vista_principal.create_main_window()
    secondary_window = None
    aux_window = None

    while True:
        window, event, values = psg.read_all_windows()
        print(event)
        print(values)
        if event is not None and event.startswith('evt:'):
            cmd = dict([tuple(part.split(':')) for part in event.split(';')])
            if cmd['evt'] == 'product':
                aux_window = producto_controlador.procesar(cmd=cmd,
                                                           valores=values,
                                                           conn=conn,
                                                           ventana_secundaria=secondary_window,
                                                           ventana_auxiliar=aux_window,
                                                           ventana_actual=window)
            if cmd['evt'] == 'mat_pri':
                aux_window = materia_prima_controlador.procesar(cmd=cmd,
                                                           valores=values,
                                                           conn=conn,
                                                           ventana_secundaria=secondary_window,
                                                           ventana_auxiliar=aux_window,
                                                           ventana_actual=window)
            elif cmd['evt'] == 'bom':
                aux_window = bom_controlador.procesar(cmd=cmd,
                                                      valores=values,
                                                      conn=conn,
                                                      ventana_secundaria=secondary_window,
                                                      ventana_auxiliar=aux_window,
                                                      ventana_actual=window)
        elif event == psg.WIN_CLOSED or event == 'Salir':
            window.close()
            if window == aux_window:
                aux_window = None
            elif window == secondary_window:
                secondary_window = None
            elif window == main_window:
                break
        ###########################################
        # OPCIONES EL MENU
        elif event == 'Nuevo proyecto':
            pass
        elif event == 'Explosión de materiales (BOM)':
            secondary_window = bom_vista.crear_ventana_listado(conn)
            pass
        elif event == 'Materias Primas':
            secondary_window = materia_prima_vista.crear_ventana_listado(
                conn)
        elif event == 'Productos':
            secondary_window = producto_vista.crear_ventana_listado(conn)
        elif event == 'Reporte de productos':
            pass
        elif event == 'Reporte de materias primas':
            pass
        elif event == 'Reporte de BOM':
            pass
        elif event == 'Reporte de proyectos':
            pass
        elif event == 'Información de la aplicación, Terminos de uso y Licencia':
            text = '''
Es importante tener en cuenta los términos y condiciones establecidos en la 
licencia Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International (CC BY-NC-SA 4.0). Esta licencia permite compartir, copiar, 
redistribuir, adaptar y construir sobre el material siempre y cuando se 
cumplan ciertas condiciones.

1. Atribución (Attribution): Debe proporcionarse un crédito apropiado, incluir 
   un enlace a la licencia y señalar si se realizaron cambios al material 
   original. Esto debe hacerse de manera razonable, sin sugerir que el 
   licenciante respalda su uso.

2. No comercial (NonCommercial): No se puede utilizar el material con fines 
   comerciales.

3. Compartir igual (ShareAlike): Si se remezcla, transforma o se crea a partir 
   del material original, se deben distribuir las contribuciones bajo la misma 
   licencia que el original.

4. No hay restricciones adicionales (No additional restrictions): No se pueden 
   aplicar términos legales o medidas tecnológicas que restrinjan legalmente a 
   otros de hacer todo lo que la licencia permite.

Además, el software proporcionado tiene restricciones y condiciones adicio-
nales establecidas por la Universidad de Costa Rica y el cuerpo docente del 
curso Ingeniería de Operaciones II-0703. 

Estas restricciones incluyen:

1. El uso del software es bajo la responsabilidad del usuario final.
2. El software es de tipo "AS-IS" y no tiene soporte para múltiples usuarios, 
   conexiones concurrentes o manejo de usuarios.
3. El usuario final es responsable de administrar la seguridad de acceso al 
   archivo de bases de datos y realizar respaldos adecuados.
4. El software es de uso gratuito para las empresas participantes en el 
   curso II-0703, siempre y cuando cumplan con su parte de colaborar con el 
   estudiantado.
5. No se permite cobrar por el uso de este software.
6. La universidad, cuerpo docente y el estudiantado no tienen responsabilidad 
   sobre la implementación de cambios, correcciones, ajustes o soporte a 
   este software.
7. Las empresas pueden realizar ajustes al software, pero deben cumplir con 
   las condiciones de la licencia Creative Commons y notificarlo por correo 
   electrónico a los autores base.

El desarrollo de la versión base del software fue realizado por 
Mauricio Andrés Zamora Hernández, Sofía Castrillo Sánchez y 
Alberto Godínez Alvarado, y se considera a estos autores de la
versión base así como parte del software en todas las versiones 
derivadas.

Si tienes alguna pregunta adicional o necesitas  más información, 
no dudes en preguntar.
  SOFIA CASTRILLO SANCHEZ 
    (SOFIA.CASTRILLO@UCR.AC.CR)
  ALBERTO GODINEZ ALVARADO 
    (ALBERTO.GODINEZALVARADO@UCR.AC.CR)
  MAURICIO ANDRES ZAMORA HERNANDEZ 
    (MAURICIO.ZAMORAHERNANDEZ@UCR.AC.CR)
    
Se les agradece se agradece por el apoyo a este software a los
profesores:
  David Gerardo Alfaro Víquez
  (david.alfaro@ucr.ac.cr)
  Johnny Araya
  (@ucr.ac.cr)
  Luis Carlos Naranjo Zeledón
  (LUIS.NARANJOZELEDON@ucr.ac.cr)
    
VERSION 2023.01 (alfa)
            '''
            psg.popup_scrolled(text, title='Información de la aplicación, Terminos de uso y Licencia', size=(80, 25))
        elif event == 'Color':
            theme_name_list = psg.theme_list()
            theme = random.choice(theme_name_list)
            psg.theme(theme)
            psg.popup(random.choice(theme_name_list),
                      title='Tema seleccionado', keep_on_top=True)
        else:
            print('ADVERTENCIA NO SE ESTA PROCESANDO EL EVENTO')
    window.close()


if '__main__' == __name__:
    # psg.theme('LightGrey')
    psg.theme('Material2')
    psg.set_options(font=('Courier New', 10))
    main()
