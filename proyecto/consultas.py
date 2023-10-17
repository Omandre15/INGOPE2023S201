import sqlite3


def registrar(conn=None, producto=None):
    exito = True
    msg = 'Operación exitosa'
    id = -1
    sql = '''
        INSERT INTO producto 
        (
            sku,
            nombre,
            cantidad,
            unidad,
            precio,
            costo_unitario,
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
        update producto 
        set
            sku = ?,
            nombre = ?,
            cantidad = ?,
            unidad = ?,
            precio = ?,
            costo_unitario = ?,
            estado = ?
        where
            producto_id = ?;
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
        delete from producto 
        where producto_id = ?;
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
          producto_id 
        , sku
        , nombre
        , cantidad
        , unidad
        , precio
        , costo_unitario
        , disponible
        , reservado
        , estado
    from 
        producto
    where
        estado in ('activo', 'inactivo')
    order by
        nombre, sku
    ''').fetchall()

    return resultados


def listar_todos(conn=None):
    resultados = conn.execute('''
    select
          producto_id 
        , sku
        , nombre
        , fecha_registro
        , fecha_ultimo_registro
        , cantidad
        , unidad
        , precio
        , costo_unitario
        , disponible
        , reservado
        , estado
    from 
        producto
    ''').fetchall()

    return resultados


def cargar(conn=None, id=-1):
    resultado = conn.execute('''
    select
          producto_id 
        , sku
        , nombre
        , fecha_registro
        , fecha_ultimo_registro
        , cantidad
        , unidad
        , precio
        , costo_unitario
        , disponible
        , reservado
        , estado
    from 
        producto
    where
        producto_id = ?
    ''', (id,)).fetchone()

    return resultado
