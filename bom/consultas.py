import sqlite3
from typing import Dict, List, Any

from bom.bom import Bom


def registrar(conn=None, dato: Bom = None):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        INSERT INTO bom 
        (
            producto_id,
            version,
            receta_principal,
            comentario,
            costo_acumulado_componentes,
            costo_acumulado_materia_prima,
            costo_operativos,
            costo_total,
            tiempo_fabricacion,
            fecha_registro,
            estado
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        );
    '''

    cursor = conn.cursor()
    try:

        valores = (dato.producto_id, dato.version, dato.receta_principal, dato.comentario,
                   dato.costo_acumulado_componentes, dato.costo_acumulado_materia_prima, dato.costo_operativos,
                   dato.costo_total, dato.tiempo_fabricacion, dato.fecha_registro, dato.estado)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def modificar(conn=None, dato: Bom = None):
    exito = True
    msg = 'Operación exitosa'
    id = -1

    sql = '''
        update bom 
        set
            producto_id,
            version,
            receta_principal,
            comentario,
            costo_acumulado_componentes,
            costo_acumulado_materia_prima,
            costo_operativos,
            costo_total,
            tiempo_fabricacion,
            fecha_registro,
            estado
        where
            bom_id = ?;
    '''

    cursor = conn.cursor()
    try:
        valores = (dato.producto_id, dato.version, dato.receta_principal, dato.comentario,
                   dato.costo_acumulado_componentes, dato.costo_acumulado_materia_prima, dato.costo_operativos,
                   dato.costo_total, dato.tiempo_fabricacion, dato.fecha_registro, dato.estado, dato.bom_id)

        cursor.execute(sql, valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def eliminar(conn=None, id=None):
    exito = True
    msg = 'Operación exitosa'
    # id = -1
    sql = '''
        delete from bom 
        where bom_id = ?;
    '''

    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id,))
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    #  id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


def cargar_tabla(conn=None):
    listado = listar_todos(conn=conn)
    salida = []

    filtro = lambda dato: dato.estado == 'activo' or dato.estado == 'inactivo'
    ordenar = lambda dato: dato.nombre

    listado.sort(key=ordenar)
    listado = list(filter(filtro, listado))

    salida = [(
        dato.materia_prima_id, dato.sku, dato.nombre, dato.cantidad, dato.disponible, dato.reservado, dato.unidad,
        dato.costo_unitario, dato.estado, dato.dias_vida_util) for dato in listado]

    return salida


def listar_todos(conn=None) -> List[Bom]:
    salida = []
    conn.row_factory = sqlite3.Row
    resultados = conn.execute('''
    select
        bom_id,
        producto_id,
        version,
        receta_principal,
        comentario,
        costo_acumulado_componentes,
        costo_acumulado_materia_prima,
        costo_operativos,
        costo_total,
        tiempo_fabricacion,
        fecha_registro,
        estado
    from 
        bom
    ''').fetchall()

    for resultado in resultados:
        salida.append(convertirDictEnObjeto(convertirRowEnDict(resultado)))

    return salida


def cargar(conn=None, id=-1) -> Bom:
    conn.row_factory = sqlite3.Row
    resultado = conn.execute('''
    select
        bom_id,
        producto_id,
        version,
        receta_principal,
        comentario,
        costo_acumulado_componentes,
        costo_acumulado_materia_prima,
        costo_operativos,
        costo_total,
        tiempo_fabricacion,
        fecha_registro,
        estado
    from 
        bom
    where
        bom_id = ?
    ''', (id,)).fetchone()

    return convertirDictEnObjeto(convertirRowEnDict(resultado))


def convertirRowEnDict(row) -> Dict[str, Any]:
    return dict(zip(row.keys(), row))


def convertirDictEnObjeto(datos:Dict) -> Bom:
    objeto = Bom()
    objeto.bom_id = datos['bom_id']
    objeto.producto_id = datos['producto_id']
    objeto.version = datos['version']
    objeto.receta_principal = datos['receta_principal']
    objeto.comentario = datos['comentario']
    objeto.costo_acumulado_componentes = datos['costo_acumulado_componentes']
    objeto.costo_acumulado_materia_prima = datos['costo_acumulado_materia_prima']
    objeto.costo_operativos = datos['costo_operativos']
    objeto.costo_total = datos['costo_total']
    objeto.tiempo_fabricacion = datos['tiempo_fabricacion']
    objeto.fecha_registro = datos['fecha_registro']
    objeto.estado = datos['estado']
    return objeto
