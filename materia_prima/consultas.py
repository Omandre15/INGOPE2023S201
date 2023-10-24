import sqlite3


def registrar(conn=None, producto=None):
    exito = True
    msg = 'Operación exitosa'
    id = -1
    # (sku, nombre, cantidad, unidad, disponible, reservado, costo_unitario, estado,dias_vida_util)
    sql = '''
        INSERT INTO materia_prima 
        (
            sku,
            nombre,
            cantidad,
            unidad,
            disponible,
            reservado,
            costo_unitario,
            estado,
            dias_vida_util
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
            ?
        );
    '''

    cursor = conn.cursor()
    try:
        cursor.execute(sql, producto)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id

def modificar(conn=None, producto=None):
    exito = True
    msg = 'Operación exitosa'
    id = -1
    sql = '''
        update materia_prima 
        set
            sku = ?,
            nombre = ?,
            fecha_registro = ?,
            unidad = ?,
            costo_unitario = ?,
            cantidad = ?,
            disponible = ?,
            reservado = ?,
            estado = ?,
            dias_vida_util = ?,
        where
            materia_prima_id = ?;
    '''

    cursor = conn.cursor()
    try:
        cursor.execute(sql, producto)
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
        delete from materia_prima 
        where materia_prima_id = ?;
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
    resultados = conn.execute('''
    select
        materia_prima_id,
        sku,
        nombre,
        cantidad,
        disponible,
        reservado,
        unidad,
        costo_unitario,
        estado,
        dias_vida_util
    from 
        materia_prima
    where
        estado in ('activo', 'inactivo')
    order by
        nombre, sku
    ''').fetchall()

    return resultados


def listar_todos(conn=None):
    resultados = conn.execute('''
    select
        materia_prima_id,
        sku,
        nombre,
        fecha_registro,
        unidad,
        costo_unitario,
        cantidad,
        disponible,
        reservado,
        estado,
        dias_vida_util
    from 
        materia_prima
    ''').fetchall()

    return resultados


def cargar(conn=None, id=-1):
    resultado = conn.execute('''
    select
        materia_prima_id,
        sku,
        nombre,
        fecha_registro,
        unidad,
        costo_unitario,
        cantidad,
        disponible,
        reservado,
        estado,
        dias_vida_util
    from 
        materia_prima
    where
        materia_prima_id = ?
    ''', (id,)).fetchone()

    return resultado
