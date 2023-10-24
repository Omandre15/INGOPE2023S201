from config.botones import *
from config.iconos import *
from materia_prima.consultas import *
import PySimpleGUI as psg

def crear_ventana_listado(conn=None):


    encabezado = ['Id', 'SKU', 'Nombre', 'Cantidad', 'Disponible', 'Reservado', 'Unidad',
                  'Costo Un.','Estado','Vida útil']

    data_values = list(cargar_tabla(conn))

    col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    layout = [
        # [
        #     psg.Column(
        #         [[psg.Text('Filtros:', expand_x=True, expand_y=True, justification='right', background_color='red')]],
        #         expand_x=True, expand_y=True),
        #     psg.Column([[psg.Input(expand_x=True)], [psg.Input()]], expand_x=True, expand_y=True),
        # ],
        [
            psg.Table(values=data_values,
                      headings=encabezado,
                      # size = (800, 600),
                      max_col_width=30,
                      num_rows=25,
                      col_widths=col_widths,
                      justification='center',
                      # col_widths=[4, 6, 20, 6, 6, 6, 6, 6, 6],
                      auto_size_columns=False,
                      enable_events=True,
                      select_mode=psg.TABLE_SELECT_MODE_BROWSE,
                      key='evt:mat_pri;det:list;act:list')
        ],
        crear_botones_crud_salir('mat_pri','materia_prima'),
        [psg.Input(visible=False, key='-cmd-', default_text='crud-mat_pri')]
    ]

    w = psg.Window(
        'Listado de materias primas'
        , layout
        , finalize=True
        , resizable=True
        , size=(None, None)
        , modal=True
    )
    # w.Maximize()

    return w


def crear_ventana_registro():
    ancho_etiqueta = 20
    ancho_contenido = 55
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    layout = [
        [
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Input(key='sku', size=(ancho_contenido, 1), expand_x=True)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Input(key='nombre', size=(ancho_contenido, 1), expand_x=True)
        ],

        [
            psg.Text('Unidades', size=(ancho_etiqueta, 1)),
            psg.Combo(unidades, key='unidad', size=(10, 1), readonly=True, default_value=unidades[0],
                      expand_x=True)
        ],
        [
            psg.Text('Cantidad', size=(ancho_etiqueta, 1)),
            psg.Input(key='cantidad', expand_x=True)
        ],
        [
            psg.Text('Disponible', size=(ancho_etiqueta, 1)),
            psg.Input(key='disponible', expand_x=True)
        ],
        [
            psg.Text('Reservado', size=(ancho_etiqueta, 1)),
            psg.Input(key='reservado', expand_x=True),

        ],
        [
            psg.Text('Días de vida útil', size=(ancho_etiqueta, 1)),
            psg.Input(key='dias-vida-util', expand_x=True),
        ],
        [
            psg.Text('Costo unitario', size=(ancho_etiqueta, 1)),
            psg.Input(key='costo-unitario', size=(ancho_contenido, 1), expand_x=True)
        ],

        [
            psg.Text('Estado', key='estado-lbl', size=(ancho_etiqueta, 1)),
            psg.Radio('Activo', 'estado', default=True, key='estado-activo', expand_x=True),
        ],
        crear_botones_aceptar_cancelar('mat_pri','Registrar materia prima','create','ok')
    ]

    w = psg.Window('Registrar una materia prima'
                   , layout
                   , finalize=True
                   , resizable=True
                   , size=(None, None)
                   , modal=True)
    # w.Maximize()
    return w


def crear_ventana_actualizacion(dato=None):
    ancho_etiqueta = 25
    ancho_contenido = 55
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    estado = dato[11]
    layout = [
        [
            psg.Text('ID interno', size=(ancho_etiqueta, 1), visible=True, key='id-lbl'),
            psg.Text(dato[0], visible=True, key='id-txt', expand_x=True),
            psg.Input(visible=False, key='id', default_text=dato[0])
        ],
        [
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Input(key='sku', size=(ancho_contenido, 1), expand_x=True, default_text=dato[1])
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Input(key='nombre', size=(ancho_contenido, 1), expand_x=True, default_text=dato[2])
        ],
        # [psg.Text('Fecha', size=(ancho_etiqueta, 1)), psg.Input(key='fecha_input', size=(ancho_contenido,1), disabled=True), psg.CalendarButton('Seleccionar Fecha', target='fecha_input', format='%Y-%m-%d', key='fecha_button')],
        [
            psg.Text('Cantidad', size=(ancho_etiqueta, 1)),
            psg.Input(key='cantidad', expand_x=True, default_text=dato[5]),
            # , default_text=producto[6]
            psg.Combo(unidades, key='cantidad-unidad', size=(10, 1), readonly=True, default_value=unidades[0],
                      expand_x=True)
        ],
        [
            psg.Text('Precio', size=(ancho_etiqueta, 1)),
            psg.Input(key='precio', size=(ancho_contenido, 1), expand_x=True, default_text=dato[7])
        ],
        [
            psg.Text('Costo unitario', size=(ancho_etiqueta, 1)),
            psg.Input(key='costo-unitario', size=(ancho_contenido, 1), expand_x=True, default_text=dato[8])
        ],
        [
            psg.Text('Disponible', key='disponible-lbl', size=(ancho_etiqueta, 1)),
            psg.Input(key='disponible', size=(ancho_contenido, 1), expand_x=True, default_text=dato[9],
                      readonly=True, text_color='black')
        ],
        [
            psg.Text('Reservado', key='reservado-lbl', size=(ancho_etiqueta, 1)),
            psg.Input(key='reservado', size=(ancho_contenido, 1), expand_x=True, default_text=dato[10],
                      readonly=True, text_color='black')
        ],
        [
            psg.Text('Fecha creación', key='creacion-lbl', size=(ancho_etiqueta, 1)),
            psg.Text(dato[3], key='creacion', expand_x=True)
        ],
        [
            psg.Text('Fecha modificado', key='modificado-lbl', size=(ancho_etiqueta, 1)),
            psg.Text(dato[4], key='modificado', expand_x=True)
        ],
        [
            psg.Text('Estado', key='estado-lbl', size=(ancho_etiqueta, 1)),
            psg.Radio('Activo', 'estado', default=estado == 'activo', key='estado-activo', expand_x=True),
            psg.Radio('Inactivo', 'estado', default=estado == 'inactivo', key='estado-inactivo', expand_x=True)
        ],
        crear_botones_aceptar_cancelar('mat_pri', 'Modificar materia prima', 'update', 'ok')
    ]

    w = psg.Window('Modificar una materia prima'
                   , layout
                   , finalize=True
                   , resizable=True
                   , size=(None, None)
                   , modal=True)
    # w.Maximize()
    return w


def crear_ventana_eliminacion(dato=None):
    ancho_etiqueta = 25
    ancho_contenido = 55
    unidades = ['unidad', 'gramos', 'cc', 'cm']

    layout = [
        [
            psg.Text('ID interno', size=(ancho_etiqueta, 1), visible=True, key='id-lbl'),
            psg.Text(dato[0], visible=True, key='id-txt', expand_x=True),
            psg.Input(key='id', visible=False, default_text=dato[0])
        ],
        [
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Text(dato[1], key='sku', size=(ancho_contenido, 1), expand_x=True)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Text(dato[2], key='nombre', size=(ancho_contenido, 1), expand_x=True)
        ],
        [
            psg.Text('Fecha creación', key='creacion-lbl', size=(ancho_etiqueta, 1)),
            psg.Text(dato[3], key='creacion', expand_x=True)
        ],
        [
            psg.Text('Fecha modificado', key='modificado-lbl', size=(ancho_etiqueta, 1)),
            psg.Text(dato[4], key='modificado', expand_x=True)
        ],
        [
            psg.Button('', tooltip='Eliminar', key='evt:mat_pri;det:delete;act:ok', expand_x=True,
                       image_data=icon_general_aceptar,
                       button_color='DodgerBlue'),
            psg.Button('', tooltip='Salir', expand_x=True, key='Salir', image_data=icon_general_cancelar,
                       button_color='tomato')
        ]
    ]

    w = psg.Window('Eliminar una materia prima'
                   , layout
                   , finalize=True
                   , resizable=True
                   , size=(None, None)
                   , modal=True)
    # w.Maximize()
    return w
