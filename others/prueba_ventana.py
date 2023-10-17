import PySimpleGUI as psg
from producto.consultas import cargar_tabla
from config.iconos import *
import config.db as db
import sqlite3


def crear_ventana_listado(conn=None):
    encabezado = ['Id', 'SKU', 'Nombre', 'Cantidad', 'Unidad',
                  'Precio', 'Costo Un.', 'Disponible', 'Reservado', 'Estado']

    # data_values = list(cargar_tabla(conn))
    data_values = [['Id', 'SKU', 'Nombre', 'Cantidad', 'Unidad',
                    'Precio', 'Costo Un.', 'Disponible', 'Reservado', 'Estado']]

    col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    largo = sum(col_widths)
    layout_producto = [
        [
            psg.Table(values=data_values,
                      headings=encabezado,
                      # size = (800, 600),
                      max_col_width=30,
                      num_rows=25,
                      col_widths=col_widths,
                      justification='center',
                      # col_widths=[20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
                      auto_size_columns=False,
                      enable_events=True,
                      key='evt:product;det:list;act:list')
        ],
        [
            psg.Input(visible=False, key='-cmd-', default_text='crud-product'),
            psg.Button('', tooltip='Nuevo Producto', key='evt:product;det:list;act:create', expand_x=True,
                       button_color='green', image_data=icon_crud_nuevo, ),
            psg.Button('', tooltip='Modificar Producto', key='evt:product;det:list;act:update', expand_x=True,
                       button_color='orange', image_data=icon_crud_modificar),
            psg.Button('', tooltip='Eliminar Producto', key='evt:product;det:list;act:delete', expand_x=True,
                       button_color='red', image_data=icon_crud_eliminar),
            psg.Button('', tooltip='Salir', key='Salir', expand_x=True, image_data=icon_general_salir)
        ]
    ]

    layout_bom = [

    ]

    tab01 = psg.Tab('Paso 01',layout_producto,background_color='white',key='step01')
    layout_main = [
        [psg.TabGroup([
            [tab01],
            [psg.Tab('Tab 2', [[psg.Text('Contenido de la pestaña 2')]])],
            [psg.Tab('Tab 3', [[psg.Text('Contenido de la pestaña 3')]])]
        ], key='-TABGROUP-', size=(None, None), enable_events=True)],
        [psg.Button('Deshabilitar Tab', key='-DISABLE-TAB-')]
    ]

    w = psg.Window(
        'Listado de productos'
        , layout_main
        , finalize=True
        , resizable=True
        , size=(None, None)
        , modal=True
    )
    # w.Maximize()

    return w



psg.theme('LightGrey')
psg.set_options(font=('Courier New', 10))
window = crear_ventana_listado(None)

while True:
    event, values = window.read()
    if event == psg.WINDOW_CLOSED:
        break
    elif event in ('-TAB1-', '-TAB2-', '-TAB3-'):
        window['-TAB1-CONTENT-'].update(visible=event == '-TAB1-')
        window['-TAB2-CONTENT-'].update(visible=event == '-TAB2-')
        window['-TAB3-CONTENT-'].update(visible=event == '-TAB3-')
        # window['-TAB3-'].update(disabled=True)

window.close()