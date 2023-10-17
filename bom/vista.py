from bom.consultas import *
from config.botones import *


def crear_ventana_listado(conn=None):
    encabezado = ['Id', 'SKU', 'Nombre', 'Versión', 'Tipo Receta',
                  'Estado', 'Ct. Cptes', 'Ct. Mat. Pr.', 'Ct. Optvo']

    data_values = list(cargar_tabla(conn))

    col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    layout = [
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
                      key='evt:bom;det:list;act:list')
        ],
        [
            psg.Text(
                'PARA AGREGAR UNA EXPLOSION DE MATERIALES, ' + \
                'PRIMERO REGISTRE UN BOM. ' + \
                'PARA AGREGAR MATERIALES O COMPONENTES, ' + \
                'USE LA OPCION DE EDITAR',
                key='Texto', justification='center', expand_x=True, expand_y=True, background_color='yellow')
        ],
        crear_botones_crud_salir('bom', 'Explosión de materiales'),
        [psg.Input(visible=False, key='-cmd-', default_text='crud-bom')]
    ]

    w = psg.Window(
        'Listado de explosión de materiales',
        layout,
        finalize=True,
        resizable=True,
        # size=(None, None),
        modal=True
    )
    # w.Maximize()

    return w


def crear_ventana_registro():
    # ancho_etiqueta = 15
    # ancho_contenido = 55
    # unidades = ['unidad', 'gramos', 'cc', 'cm']
    encabezado = ['Id', 'SKU', 'Nombre', 'Estado']

    # data_values = [[]]
    col_anchos = [2, 4, 25, 5]
    layout = [
        [
            psg.Frame('PASO 01: Buscar el producto',
                      [
                          [
                              psg.Text('SKU: ', size=(15, 1)),
                              psg.Input('', key='sku', expand_x=True)
                          ],
                          [
                              psg.Text('Nombre: ', size=(15, 1)),
                              psg.Input('', key='nombre', expand_x=True)
                          ],
                          [
                              crear_boton_buscar_peq('bom', det='create', act='prod_find')
                          ]
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso01')
        ],
        [
            psg.Frame('PASO 02: Seleccionar el producto',
                      [
                          [
                              psg.Table(values=[],
                                        headings=encabezado,
                                        # size = (800, 600),
                                        max_col_width=30,
                                        num_rows=5,
                                        col_widths=col_anchos,
                                        justification='center',
                                        # col_widths=[4, 6, 20, 6, 6, 6, 6, 6, 6],
                                        auto_size_columns=False,
                                        enable_events=True,
                                        select_mode=psg.TABLE_SELECT_MODE_BROWSE,
                                        expand_x=True,
                                        expand_y=True,
                                        key='evt:bom;det:create;act:prod_list')
                          ],
                          [
                              crear_boton_agregar_peq('bom', disabled=True, det='create', act='prod_add')
                          ]
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso02',
                      visible=False)
        ],
        [
            psg.Frame('PASO 03: Detallar información de la explosión de materiales',
                      [

                          [
                              psg.Input('', key='producto_id', visible=False),
                              psg.Text('SKU: ', size=(20, 1)),
                              psg.Text('', key='producto_sku', expand_x=True)
                          ],
                          [
                              psg.Text('Producto: ', size=(20, 1)),
                              psg.Text('', key='producto_nombre', expand_x=True)
                          ],
                          [
                              psg.Text('Version: ', size=(20, 1)),
                              psg.Input('', key='version', expand_x=True)
                          ],
                          [
                              psg.Text('Tipo de receta: ', size=(20, 1)),
                              psg.Radio('Principal', 'receta', key='receta-principal', expand_x=True, default=True),
                              psg.Radio('Alterna', 'receta', key='receta-alterna', expand_x=True)
                          ],
                          [
                              psg.Text('Comentario: ', size=(20, 1)),
                              psg.Multiline(autoscroll=True, expand_x=True, expand_y=True, key='comentario',
                                            size=(3, 3))
                          ],
                          [
                              psg.Text('Costo operativos: ', size=(20, 1)),
                              psg.Input('', key='costo-operativo', expand_x=True)
                          ],
                          [
                              psg.Text('Duración: ', size=(20, 1)),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-horas'),
                              psg.Text('h', justification='left'),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-minutos'),
                              psg.Text('m', justification='left'),
                              psg.Spin([i for i in range(0, 60)], initial_value=0, size=3, key='duracion-segundos'),
                              psg.Text('s', justification='left')
                          ],
                          [
                              psg.Text('Estado: ', size=(20, 1)),
                              psg.Radio('Activo', 'estado', key='estado-activo', expand_x=True, default=True),
                              psg.Radio('Inactivo', 'estado', key='estado-inactivo', expand_x=True)
                          ]
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso03',
                      visible=False)
        ],
        crear_botones_aceptar_cancelar('bom', 'Registrar producto', 'create', 'ok', disabled=True)
    ]

    w = psg.Window('Registrar una explosión de materiales',
                   layout,
                   finalize=True,
                   resizable=True,
                   # size=(None, None),
                   modal=True)
    # w.Maximize()
    return w


def crear_ventana_actualizacion_compacta(dato=None, componentes=None, materias_primas=None):
    ancho_etiqueta = 25
    ancho_contenido = 55

    treedata = psg.TreeData()
    treedata.insert('', 'raiz', dato[3], [0, 0, 0])
    treedata.insert('raiz', 'comp', 'Componentes', [0, 0, 0])
    for componente in componentes:
        treedata.insert('comp', 'comp:{}'.format(componente[0]), componente[5],
                        [componente[6], componente[8], componente[6] * componente[8]])

    treedata.insert('raiz', 'mp', 'Materias primas', [0, 0, 0])
    for materia_prima in materias_primas:
        treedata.insert('mp', 'matpri:{}'.format(materia_prima[0]), materia_prima[5],
                        [materia_prima[6], materia_prima[8], materia_prima[6] * materia_prima[8]])
    encabezado = ['Id', 'SKU', 'Nombre', 'Estado']

    # data_values = [[]]
    col_anchos = [2, 4, 25, 5]

    frame_arbol = psg.Frame('Árbol de explosión de materiales',
                            [
                                [
                                    psg.Tree(data=treedata,
                                             headings=['Ctd. Un.', 'Costo Un.', 'Costo Total'],
                                             auto_size_columns=True,
                                             num_rows=10,
                                             col0_width=25,
                                             key='-TREE-',
                                             show_expanded=True,
                                             enable_events=False,
                                             select_mode=psg.TABLE_SELECT_MODE_BROWSE,
                                             expand_x=True,
                                             expand_y=True,
                                             )
                                ],
                            ],
                            expand_x=True,
                            expand_y=True)

    frame_control_bom = psg.Frame('Edición explosión de materiales',
                                  [
                                      [
                                          crear_boton_modificar_med(evt='bom', det='detail-bom', act='update')
                                      ],
                                      [
                                          crear_boton_eliminar_med(evt='bom', det='detail-bom', act='delete')
                                      ],
                                  ],
                                  expand_x=True,
                                  expand_y=True)

    frame_control_elemento = psg.Frame('Edición Componentes / Materias primas',
                                       [
                                           [
                                               crear_boton_agregar_med(evt='bom', det='detail-bom-root', act='add')
                                           ],
                                           [
                                               crear_boton_modificar_med(evt='bom', det='detail-bom-root', act='update')
                                           ],
                                           [
                                               crear_boton_eliminar_med(evt='bom', det='detail-bom-root',
                                                                        act='delete')
                                           ],
                                       ],
                                       expand_x=True,
                                       expand_y=True)

    frame_bom_info = psg.Frame('Información general',
                               [
                                   [
                                       psg.Input(default_text=dato[0], key='id', expand_x=True, visible=False)
                                   ],
                                   [
                                       psg.Text('SKU', size=(ancho_etiqueta, 1), background_color='white',
                                                text_color='black'),
                                       psg.Text(dato[2], key='sku-producto', size=(ancho_contenido, 1),
                                                expand_x=True, background_color='white', text_color='black'),
                                       crear_boton_informacion_peq(evt='bom')
                                   ],
                                   [
                                       psg.Text('Nombre', size=(ancho_etiqueta, 1), background_color='white',
                                                text_color='black'),
                                       psg.Text(dato[3], key='sku-producto', size=(ancho_contenido, 1),
                                                expand_x=True, background_color='white', text_color='black'),
                                   ]
                               ],
                               expand_x=True,
                               expand_y=True)

    layout_col_izquierda = \
        [
            [
                frame_arbol
            ],
            [
                frame_bom_info
            ]
        ]

    layout_col_derecha = \
        [
            [
                frame_control_bom
            ],
            [
                frame_control_elemento
            ],
            [
                crear_boton_salir_med()
            ]
        ]

    layout = [
        [
            psg.Column(layout_col_izquierda,
                       expand_x=True,
                       expand_y=True),
            psg.Column(layout_col_derecha,
                       expand_x=True,
                       expand_y=True)
        ],

    ]

    w = psg.Window('Modificar una explosión de materiales',
                   layout,
                   finalize=True,
                   resizable=True,
                   # , size=(None, None),
                   modal=True)
    # w.Maximize()
    return w


def crear_ventana_bom_edicion(conn=None, dato=None):
    ancho_etiqueta = 25
    ancho_contenido = 55

    layout = [
        [
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Text(dato[2], key='sku-producto', size=(ancho_contenido, 1),
                     expand_x=True)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Text(dato[3], key='nombre-producto', size=(ancho_contenido, 1),
                     expand_x=True)
        ],
        [
            psg.Text('Versión', size=(ancho_etiqueta, 1)),
            psg.Input(key='version-producto', size=(ancho_contenido, 1), expand_x=True,
                      default_text=dato[4])
        ],
        [
            psg.Text('Comentario', size=(ancho_etiqueta, 1)),
            psg.Multiline(key='comentario-producto', size=(ancho_contenido, 3), expand_x=True,
                          default_text=dato[6], )
        ],
        [
            psg.Text('Costo operativos', size=(ancho_etiqueta, 1)),
            psg.Input(key='costo-operativos-producto', size=(ancho_contenido, 1),
                      expand_x=True,
                      default_text=dato[9])
        ],
        [
            psg.Text('Tipo Receta', key='receta-lbl', size=(ancho_etiqueta, 1)),
            psg.Radio('Primaria', 'receta', default='Receta principal' == dato[5],
                      key='receta-primaria-producto',
                      expand_x=True),
            psg.Radio('Alternativa', 'receta', default='Receta alterna' == dato[5],
                      key='receta-alternativa-producto',
                      expand_x=True)
        ],
        [
            psg.Text('Estado', key='estado-lbl', size=(ancho_etiqueta, 1)),
            psg.Radio('Activo', 'estado', default='Activo' == dato[12],
                      key='estado-activo-producto',
                      expand_x=True),
            psg.Radio('Inactivo', 'estado', default='Inactivo' == dato[12],
                      key='estado-inactivo-producto',
                      expand_x=True)
        ],
        [
            crear_boton_modificar(evt='bom'),
            crear_boton_eliminar(evt='bom')
        ]
    ]

    w = psg.Window(
        'Edición de explosión de materiales',
        layout,
        finalize=True,
        resizable=True,
        # size=(None, None),
        modal=True
    )

    return w


def crear_ventana_bom_eliminar(conn=None, dato=None):
    ancho_etiqueta = 25
    ancho_contenido = 55

    layout = [
        [
            psg.Text('SKU', size=(ancho_etiqueta, 1)),
            psg.Text(dato[2], key='sku-producto', size=(ancho_contenido, 1),
                     expand_x=True)
        ],
        [
            psg.Text('Nombre', size=(ancho_etiqueta, 1)),
            psg.Text(dato[3], key='nombre-producto', size=(ancho_contenido, 1),
                     expand_x=True)
        ],
        [
            psg.Text('Versión', size=(ancho_etiqueta, 1)),
            psg.Text(dato[4], expand_x=True)
        ],
        [
            psg.Text('Comentario', size=(ancho_etiqueta, 1)),
            psg.Text(dato[6], expand_x=True)
        ],
        [
            psg.Text('Costo operativos', size=(ancho_etiqueta, 1)),
            psg.Text(dato[9], expand_x=True)
        ],
        [
            psg.Text('Tipo Receta', key='receta-lbl', size=(ancho_etiqueta, 1)),
            psg.Text(dato[5], expand_x=True)
        ],
        [
            psg.Text('Estado', key='estado-lbl', size=(ancho_etiqueta, 1)),
            psg.Text(dato[12], expand_x=True)
        ],
        [
            crear_boton_modificar(evt='bom'),
            crear_boton_eliminar(evt='bom')
        ]
    ]

    w = psg.Window(
        'Edición de explosión de materiales',
        layout,
        finalize=True,
        resizable=True,
        # size=(None, None),
        modal=True
    )

    return w


def crear_ventana_registro_bom_componente_materia_prima(conn=None, dato=None):
    ancho_etiqueta = 15
    ancho_contenido = 55
    encabezado = ['Id', 'SKU', 'Nombre', 'Versión', 'Tipo Receta',
                  'Estado', 'Ct. Cptes', 'Ct. Mat. Pr.', 'Ct. Optvo']

    # data_values = list(cargar_tabla(conn))
    print(dato)
    data_values = []

    col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    layout = [
        [
            psg.Frame('PASO 01: Seleccionar tipo componente o producto',
                      [
                          [
                              psg.Input(dato[0],key='id',visible=False)
                          ],
                          [
                              psg.Column([
                                  [
                                      psg.Radio('Componente', group_id='seleccion', key='seleccion-componente',
                                                expand_x=True, default=True)
                                  ],
                                  [
                                      psg.Radio('Materia prima', group_id='seleccion', key='seleccion-mp',
                                                expand_x=True)
                                  ]
                              ]
                              )
                          ],
                          [
                              crear_boton_buscar_peq('bom', det='comp-matprima', act='select')
                          ]
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso01')
        ],
        [
            psg.Frame('PASO 02: Seleccionar componente o producto',
                      [
                          [
                              psg.Table(values=data_values,
                                        headings=encabezado,
                                        # size = (800, 600),
                                        max_col_width=30,
                                        num_rows=10,
                                        col_widths=col_widths,
                                        justification='center',
                                        # col_widths=[4, 6, 20, 6, 6, 6, 6, 6, 6],
                                        auto_size_columns=False,
                                        enable_events=False,
                                        select_mode=psg.TABLE_SELECT_MODE_BROWSE,
                                        key='evt:bom;det:list;act:list')
                          ],
                          [
                              crear_boton_buscar_peq('bom', det='create', act='prod_find')
                          ]
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso02',
                      visible=dato[1]>0)
        ],
        [
            psg.Frame('PASO 03: Detallar información del componente o materia prima',
                      [

                          [
                              psg.Input('', key='producto_id', visible=False),
                              psg.Text('SKU: ', size=(20, 1)),
                              psg.Text('', key='sku', expand_x=True)
                          ],
                          [
                              psg.Text('Nombre: ', size=(20, 1)),
                              psg.Text('', key='nombre', expand_x=True)
                          ],
                          [
                              psg.Text('Cantidad: ', size=(20, 1)),
                              psg.Input('', key='cantidad', expand_x=True)
                          ],
                      ],
                      title_location=psg.TITLE_LOCATION_TOP,
                      expand_x=True,
                      expand_y=True,
                      key='paso03',
                      visible=dato[1]>1)
        ],
        crear_botones_aceptar_cancelar('bom', 'Registrar producto', 'create', 'ok', disabled=dato[1]>0)
    ]

    w = psg.Window('Registrar un componente o materia prima en la explosión de materiales',
                   layout,
                   finalize=True,
                   resizable=True,
                   # size=(None, None),
                   modal=True)
    # w.Maximize()
    return w


def crear_ventana_edicion_bom_componente_materia_prima(conn=None, dato=None):
    ancho_etiqueta = 15
    ancho_contenido = 55
    encabezado = ['Id', 'SKU', 'Nombre', 'Versión', 'Tipo Receta',
                  'Estado', 'Ct. Cptes', 'Ct. Mat. Pr.', 'Ct. Optvo']

    # data_values = list(cargar_tabla(conn))

    data_values = []

    col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    layout = [

        [

            [
                psg.Input('', key='producto_id', visible=False),
                psg.Text('SKU: ', size=(20, 1)),
                psg.Text('', key='sku', expand_x=True)
            ],
            [
                psg.Text('Nombre: ', size=(20, 1)),
                psg.Text('', key='nombre', expand_x=True)
            ],
            [
                psg.Text('Cantidad: ', size=(20, 1)),
                psg.Input('', key='cantidad', expand_x=True)
            ],

        ],
        crear_botones_aceptar_cancelar('bom', 'Registrar producto', 'create', 'ok', disabled=True)
    ]

    w = psg.Window('Registrar un componente o materia prima en la explosión de materiales',
                   layout,
                   finalize=True,
                   resizable=True,
                   # size=(None, None),
                   modal=True)
    # w.Maximize()
    return w


def crear_ventana_eliminacion_bom_componente_materia_prima(conn=None, dato=None):
    ancho_etiqueta = 15
    ancho_contenido = 55
    encabezado = ['Id', 'SKU', 'Nombre', 'Versión', 'Tipo Receta',
                  'Estado', 'Ct. Cptes', 'Ct. Mat. Pr.', 'Ct. Optvo']

    # data_values = list(cargar_tabla(conn))

    data_values = []

    col_widths = [max(map(lambda x: len(x) + 7, (map(str, col)))) for col in zip(*data_values)]
    layout = [

        [

            [
                psg.Input('', key='producto_id', visible=False),
                psg.Text('SKU: ', size=(20, 1)),
                psg.Text('', key='sku', expand_x=True)
            ],
            [
                psg.Text('Nombre: ', size=(20, 1)),
                psg.Text('', key='nombre', expand_x=True)
            ],
            [
                psg.Text('Cantidad: ', size=(20, 1)),
                psg.Text('', key='cantidad', expand_x=True)
            ],

        ],
        crear_botones_aceptar_cancelar('bom', 'Registrar producto', 'create', 'ok', disabled=True)
    ]

    w = psg.Window('Registrar un componente o materia prima en la explosión de materiales',
                   layout,
                   finalize=True,
                   resizable=True,
                   # size=(None, None),
                   modal=True)
    # w.Maximize()
    return w
