import bom.vista as vistas
import bom.consultas as consultas
import utils.validaciones as utils_validacion
import utils.ventana as utils_ventana
import producto.consultas as consultas_prod

import PySimpleGUI as psg

from bom.consultas import listar_por_sku_nombre


def listar_mensajes_errores_registro():
    # debe corresponder a lista de validación
    return ('Versión es obligatoria y única por producto', 'El comentario es obligatorio',
            'El costo unitario es obligatorio y númerico', 'El costo debe ser mayor o igual a cero')


def validar_condiciones_registro(dato=()):
    if dato:
        # valida los elementos en este orden
        # (sku, nombre, cantidad, unidad, precio, costo_unitario, estado)
        # ('5', 'version nueva', (True, False), 'comentario', '777', (False, True))
        validacion = (
            not utils_validacion.validar_texto_vacio(dato[1]),  # version
            not utils_validacion.validar_texto_vacio(dato[3]),  # comentario
            utils_validacion.validar_numero_real(dato[4]),  # costo_unitario
            True if utils_validacion.validar_numero_real(dato[4]) and float(
                dato[4]) >= 0 else False
        )
        return validacion
    else:
        return ()


def validar_registro(dato=()):
    if dato:
        validacion = validar_condiciones_registro(dato)
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
    if cmd['evt'] != 'bom':
        psg.popup_error('Intentando procesar un evento de producto, pero se envió otro evento', 'Error de programación')
    else:
        if cmd['det'] == 'list' and cmd['act'] == 'create':
            ventana = vistas.crear_ventana_registro()

        elif cmd['det'] == 'create' and cmd['act'] == 'prod_find':
            sku = valores['sku']
            nombre = valores['nombre']

            datos = listar_por_sku_nombre(conn=conn, sku=sku, nombre=nombre)
            ventana_actual['paso02'].update(visible=True)
            nombre_tabla = 'evt:bom;det:create;act:prod_list'
            ventana_actual[nombre_tabla].update(values=datos)
            ventana_actual['evt:bom;det:create;act:prod_add'].update(disabled=len(datos) == 0)
            utils_ventana.centrar_ventana(ventana_actual)

        elif cmd['det'] == 'create' and cmd['act'] == 'prod_add':
            nombre_tabla = 'evt:bom;det:create;act:prod_list'
            datos_seleccionados = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_actual,
                                                                                 nombre_tabla=nombre_tabla,
                                                                                 valores=valores)
            if datos_seleccionados:
                id_seleccionado = int(datos_seleccionados[0][0])
                dato = consultas_prod.cargar(conn=conn, id=id_seleccionado)
                ventana_actual['evt:bom;det:create;act:prod_find'].update(disabled=True)
                ventana_actual['evt:bom;det:create;act:ok'].update(disabled=False)
                ventana_actual['paso03'].update(visible=True)
                ventana_actual['producto_id'].update(dato[0])
                ventana_actual['producto_sku'].update(dato[1])
                ventana_actual['producto_nombre'].update(dato[2])
                ventana_actual.finalize()
                utils_ventana.centrar_ventana(ventana_actual)

            else:
                psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')

        elif cmd['det'] == 'create' and cmd['act'] == 'ok':
            producto_id = valores['producto_id']
            version = valores['version']
            receta_principal = valores['receta-principal']
            receta_alterna = valores['receta-alterna']
            comentario = valores['comentario']
            costo_operativo = valores['costo-operativo']
            estado_activo = valores['estado-activo']
            estado_inactivo = valores['estado-inactivo']
            dato = (producto_id, version, (receta_principal, receta_alterna), comentario, costo_operativo,
                    (estado_activo, estado_inactivo))

            if validar_registro(dato):
                d = list(dato)
                d[2] = d[2][0]
                d[5] = 'activo' if d[5][0] else 'inactivo'
                exito, msg, id = consultas.registrar(conn, dato=tuple(d))
                if exito:
                    # psg.popup_ok('Se registrado la explisión de materiales', title='Resultado')
                    ventana_actual.close()
                    ventana_actual = None
                    datos = consultas.cargar_tabla(conn)
                    ventana_secundaria['evt:bom;det:list;act:list'].update(values=datos)
                    ventana = ventana_secundaria
                else:
                    psg.popup_error(msg, title='Error')
            else:

                errores = [z[0] for z in zip(listar_mensajes_errores_registro(), validar_condiciones_registro(dato)) if
                           not z[1]]
                psg.popup_error(*errores, title='Revise antes de continuar')

        elif cmd['det'] == 'list' and cmd['act'] == 'update':

            nombre_tabla = 'evt:bom;det:list;act:list'
            data_selected = utils_ventana.obtener_datos_seleccionado_tabla(ventana=ventana_secundaria,
                                                                           nombre_tabla=nombre_tabla, valores=valores)
            if data_selected:
                selected = int(data_selected[0][0])
                dato = consultas.cargar(conn=conn, id=selected)
                componentes = consultas.cargar_componentes(conn=conn, id=dato[0])
                materias_primas = consultas.cargar_materias_primas(conn=conn, id=dato[0])

                ventana = vistas.crear_ventana_actualizacion_compacta(dato=dato, componentes=componentes,
                                                                      materias_primas=materias_primas)
            else:
                psg.popup('No se ha seleccionado un dato', title='Paso obligatorio')

        elif cmd['det'] == 'detail-bom' and cmd['act'] == 'update':
            dato = consultas.cargar(conn=conn, id=int(valores['id']))

            ventana = vistas.crear_ventana_bom_edicion(conn=conn, dato=dato)

        elif cmd['det'] == 'detail-bom' and cmd['act'] == 'delete':
            dato = consultas.cargar(conn=conn, id=int(valores['id']))

            ventana = vistas.crear_ventana_bom_eliminar(conn=conn, dato=dato)

        elif cmd['det'] == 'detail-bom-root' and cmd['act'] == 'add':

            dato = (valores['id'],0,)

            ventana = vistas.crear_ventana_registro_bom_componente_materia_prima(dato=dato)

        elif cmd['det'] == 'detail-bom-root' and cmd['act'] == 'update':
            dato = None

            ventana = vistas.crear_ventana_edicion_bom_componente_materia_prima(dato=dato)

        elif cmd['det'] == 'detail-bom-root' and cmd['act'] == 'delete':
            dato = None

            ventana = vistas.crear_ventana_eliminacion_bom_componente_materia_prima(dato=dato)

        elif cmd['det'] == 'comp-matprima' and cmd['act'] == 'select':
            seleccion_componente = valores['seleccion-componente']
            dato = (valores['id'],1,[1,2,3,4,5,6])
            ventana = vistas.crear_ventana_registro_bom_componente_materia_prima(dato=dato)

    return ventana
