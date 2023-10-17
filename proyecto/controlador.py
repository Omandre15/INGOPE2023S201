import producto.vista as vistas
import producto.consultas as consultas
import utils.validaciones as utils_validacion

import PySimpleGUI as psg


def listar_mensajes_errores_actualizacion():
    # debe corresponder a lista de validación
    return ('Revise SKU', 'Revise el nombre', 'Revise la cantidad', 'Revise la unidad', 'Revise el precio',
            'Revise el costo unitario', 'Revise el estado', 'Revisar: costo por encima del precio')


def validar_condiciones_actualizacion(producto=()):
    if producto:
        # valida los elementos en este orden
        validacion = (
            not utils_validacion.validar_texto_vacio(producto[0]),  # sku
            not utils_validacion.validar_texto_vacio(producto[1]),  # nombre
            utils_validacion.validar_numero_real(producto[2]),  # cantidad
            not utils_validacion.validar_texto_vacio(producto[3]),  # unidad
            utils_validacion.validar_numero_real(producto[4]),  # precio
            utils_validacion.validar_numero_real(producto[5]),  # costo_unitario
            not utils_validacion.validar_texto_vacio(producto[6]),  # estado
            True if utils_validacion.validar_numero_real(producto[5]) and utils_validacion.validar_numero_real(producto[4]) and float(
                producto[4]) >= float(producto[5]) else False
        )
        return validacion
    else:
        return ()


def validar_actualizacion(producto=()):
    if producto:
        validacion = validar_condiciones_creacion(producto)
        return all(validacion)
    else:
        return False


def listar_mensajes_errores_creacion():
    # debe corresponder a lista de validación
    return ('Revise SKU', 'Revise el nombre', 'Revise la cantidad', 'Revise la unidad', 'Revise el precio',
            'Revise el costo unitario', 'Revise el estado', 'Revisar: costo por encima del precio')


def validar_condiciones_creacion(producto=()):
    if producto:
        # valida los elementos en este orden
        # (sku, nombre, cantidad, unidad, precio, costo_unitario, estado)
        validacion = (
            not utils_validacion.validar_texto_vacio(producto[0]),  # sku
            not utils_validacion.validar_texto_vacio(producto[1]),  # nombre
            utils_validacion.validar_numero_real(producto[2]),  # cantidad
            not utils_validacion.validar_texto_vacio(producto[3]),  # unidad
            utils_validacion.validar_numero_real(producto[4]),  # precio
            utils_validacion.validar_numero_real(producto[5]),  # costo_unitario
            not utils_validacion.validar_texto_vacio(producto[6]),  # estado
            True if utils_validacion.validar_numero_real(producto[5]) and utils_validacion.validar_numero_real(producto[4]) and float(
                producto[4]) >= float(producto[5]) else False
        )
        return validacion
    else:
        return ()


def validar_creacion(producto=()):
    if producto:
        validacion = validar_condiciones_creacion(producto)
        return all(validacion)
    else:
        return False


def procesar(
        ventana_actual=None,
        ventana_secundaria=None,
        ventana_auxiliar=None,
        cmd=None,
        valores=None,
        conn=None
):
    ventana = None
    if cmd['evt'] != 'product':
        psg.popup_error('Intentando procesar un evento de producto, pero se envió otro evento', 'Error de programación')
    else:
        if cmd['det'] == 'list' and cmd['act'] == 'create':
            ventana = vistas.crear_ventana_registro()
        elif cmd['det'] == 'list' and cmd['act'] == 'update':
            nombre_tabla = 'evt:product;det:list;act:list'
            table = ventana_secundaria[nombre_tabla]
            table_values = table.Values
            data_selected = [table_values[row] for row in valores[nombre_tabla]]
            if data_selected:
                selected = int(data_selected[0][0])
                producto = consultas.cargar(conn=conn, id=selected)
                ventana = vistas.crear_ventana_actualizacion(producto)
            else:
                psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')


        elif cmd['det'] == 'list' and cmd['act'] == 'delete':
            nombre_tabla = 'evt:product;det:list;act:list'
            table = ventana_secundaria[nombre_tabla]
            table_values = table.Values
            data_selected = [table_values[row] for row in valores[nombre_tabla]]
            if data_selected:
                selected = int(data_selected[0][0])
                producto = consultas.cargar(conn=conn, id=selected)
                ventana = vistas.crear_ventana_eliminacion(producto)
            else:
                psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')


        elif cmd['det'] == 'create' and cmd['act'] == 'ok':
            sku = valores['sku']
            nombre = valores['nombre']
            cantidad = valores['cantidad']
            unidad = valores['cantidad-unidad']
            precio = valores['precio']
            costo_unitario = valores['costo-unitario']
            estado = 'activo'
            producto = (sku, nombre, cantidad, unidad, precio, costo_unitario, estado)
            if validar_creacion(producto):
                exito, msg, id = consultas.registrar(conn=conn, producto=producto)
                if exito:
                    ventana_actual.close()
                    ventana_actual = None
                    datos = consultas.cargar_tabla(conn)
                    ventana_secundaria['evt:product;det:list;act:list'].update(values=datos)
                    ventana = ventana_secundaria
                else:
                    msg = msg.replace('UNIQUE constraint failed:',
                                      'Se intenta registrar un valor duplicado (que no es permitido) para:')
                    psg.popup_error(msg, title='Error')

            else:
                mensajes_error = listar_mensajes_errores_creacion()
                indicadores_error = validar_condiciones_creacion(producto)
                mensaje = '\n'.join(
                    [i[1] for i in filter(lambda x: not x[0], list(zip(indicadores_error, mensajes_error)))])
                psg.popup_error(mensaje, title='Revise para continuar')


        elif cmd['det'] == 'update' and cmd['act'] == 'ok':
            id = valores['id']
            sku = valores['sku']
            nombre = valores['nombre']
            cantidad = valores['cantidad']
            unidad = valores['cantidad-unidad']
            precio = valores['precio']
            costo_unitario = valores['costo-unitario']
            estado_activo = valores['estado-activo']
            estado_inactivo = valores['estado-inactivo']

            if estado_activo:
                estado = 'activo'
            elif estado_inactivo:
                estado = 'inactivo'
            else:
                estado = ''

            producto = (
                sku,
                nombre,
                cantidad,
                unidad,
                precio,
                costo_unitario,
                estado,
                id
            )

            if validar_actualizacion(producto):
                exito, msg, id = consultas.modificar(conn=conn, producto=producto)
                if exito:
                    ventana_actual.close()
                    ventana_actual = None
                    datos = consultas.cargar_tabla(conn)
                    ventana_secundaria['evt:product;det:list;act:list'].update(values=datos)
                    ventana = ventana_secundaria
                else:
                    msg = msg.replace('UNIQUE constraint failed:',
                                      'Se intenta registrar un valor duplicado (que no es permitido) para:')
                    psg.popup_error(msg, title='Error')
            else:
                mensajes_error = listar_mensajes_errores_actualizacion()
                indicadores_error = validar_condiciones_actualizacion(producto)
                mensaje = '\n'.join(
                    [i[1] for i in filter(lambda x: not x[0], list(zip(indicadores_error, mensajes_error)))])
                psg.popup_error(mensaje, title='Revise para continuar')

        elif cmd['det'] == 'delete' and cmd['act'] == 'ok':
            id = valores['id']

            respuesta = psg.popup_yes_no('¿Desea continuar?',
                                         title='Confirmación')

            # Verificar la respuesta del usuario
            if respuesta == 'Yes':
                consultas.eliminar(conn, int(id))

            ventana_actual.close()
            ventana_actual = None
            datos = consultas.cargar_tabla(conn)
            ventana_secundaria['evt:product;det:list;act:list'].update(values=datos)
            ventana = ventana_secundaria

    return ventana
