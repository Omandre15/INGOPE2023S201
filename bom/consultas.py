import sqlite3


def cargar_tabla(conn=None):
    resultados = conn.execute('''
SELECT
    b.bom_id,
    p.sku,
    p.nombre,
    b.version,
    CASE b.version_default
    WHEN 1 THEN 'Receta principal'
    WHEN 0 THEN 'Receta alterna'
    END,
    b.estado,
    b.costo_componentes,
    b.costo_materia_prima,
    b.costo_operativos
FROM
    bom as b
JOIN
    producto as p
    on b.producto_id = p.producto_id
WHERE
    b.estado in ('activo','inactivo')
ORDER BY
    p.nombre,
    b.version_default DESC,
    b.estado
    ''').fetchall()

    return resultados


def registrar(conn=None, dato=None):
    exito = True
    msg = 'Operación exitosa'
    id = -1
    sql = '''
INSERT INTO bom
    (
    producto_id,
    version,
    version_default,
    comentario,
    costo_operativos,
    estado
    )
VALUES
(
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
        cursor.execute(sql, dato)
        conn.commit()
    except sqlite3.IntegrityError as e:
        msg = str(e)
        exito = False
        conn.rollback()

    id = cursor.lastrowid

    cursor.close()

    return exito, msg, id


# def listar_todos(conn=None):
#     resultados = conn.execute('''
#     select
#           producto_id
#         , sku
#         , nombre
#         , fecha_registro
#         , fecha_ultimo_registro
#         , cantidad
#         , unidad
#         , precio
#         , costo_unitario
#         , disponible
#         , reservado
#         , estado
#     from
#         bom
#     ''').fetchall()
#
#     return resultados


def listar_por_sku_nombre(conn=None, sku=None, nombre=None):
    if sku is None:
        sku = ''
    if nombre is None:
        nombre = ''
    sku = f'%{sku}%'
    nombre = f'%{nombre}%'
    resultados = conn.execute('''
SELECT
    p.producto_id,
    p.sku,
    p.nombre,
    p.estado
FROM
    producto as p
WHERE
    p.sku like ?
    AND
    p.nombre like ?
    AND
    estado in ('activo', 'inactivo')
    ''', (sku, nombre)).fetchall()

    return resultados


def cargar(conn=None, id=-1):
    resultado = conn.execute('''
SELECT
      b.bom_id
    , b.producto_id
    , p.sku as sku_producto
    , p.nombre as nombre_producto
    , b.version
    , CASE b.version_default
        WHEN 1 THEN 'Receta principal'
        WHEN 0 THEN 'Receta alterna'
      END as version_default
    , b.comentario
    , b.costo_componentes
    , b.costo_materia_prima
    , b.costo_operativos
    , b.fecha_registro
    , b.fecha_ultimo_registro
    , CASE b.estado
        WHEN 'activo' THEN 'Activo'
        WHEN 'inactivo' THEN 'Inactivo'
      END as estado
FROM
    bom as b
JOIN
    producto as p
    on b.producto_id = p.producto_id
WHERE
    b.bom_id = ?
    ''', (id,)).fetchone()

    return resultado


def cargar_componentes(conn=None, id=-1):
    resultado = conn.execute('''
SELECT
      bc.bom_componentes_id
    , bc.bom_id
    , bc.producto_id
    , p.nombre as producto_nombre
    , bc.componente_id
    , c.nombre as componente_nombre
    , bc.cantidad
    , bc.unidad
    , bc.costo
    , bc.lead_time
    , bc.lead_time_unidad
    , bc.nivel
FROM
    bom_componentes as bc
JOIN
    producto as p
    on bc.producto_id = p.producto_id
JOIN
    producto as c
    on bc.componente_id = c.producto_id
WHERE
    bc.bom_id = ?
    ''', (id,)).fetchall()

    return resultado


def cargar_materias_primas(conn=None, id=-1):
    resultado = conn.execute('''
SELECT
      bmp.bom_materias_primas_id
    , bmp.bom_id
    , bmp.producto_id
    , p.nombre as producto_nombre
    , bmp.materia_prima_id
    , mp.nombre as materia_prima_nombre
    , bmp.cantidad
    , bmp.unidad
    , bmp.costo
    , bmp.lead_time
    , bmp.lead_time_unidad
FROM
    bom_materias_primas as bmp
JOIN
    producto as p
    on bmp.producto_id = p.producto_id
JOIN
    materia_prima as mp
    on bmp.materia_prima_id = mp.materia_prima_id
WHERE
    bmp.bom_id = ?
    ''', (id,)).fetchall()

    return resultado

def listar_otros_componentes_bom(conn=None, id=-1):
    resultado = conn.execute('''
SELECT
     p.producto_id
    ,p.sku
    ,p.nombre
FROM
    producto as p
WHERE
    p.producto_id not in (
    SELECT
        bc.componente_id
    FROM
        bom_componentes as bc
    WHERE
        bc.bom_id = ?
    )
    AND
    p.estado = 'activo'
ORDER BY
    p.nombre
    ''', (id,)).fetchall()

    return resultado


def listar_otras_materias_primas_bom(conn=None, id=-1):
    resultado = conn.execute('''
SELECT
     mp.materia_prima_id
    ,mp.sku
    ,mp.nombre
FROM
    materia_prima as  mp
WHERE
    mp.materia_prima_id not in (
    SELECT
        bmp.bom_materias_primas_id
    FROM
        bom_materias_primas as bmp
    WHERE
        bmp.bom_id = 1
    )
    AND
    mp.estado = 'activo'
ORDER BY
    mp.nombre
    ''', (id,)).fetchall()

    return resultado
#asdf