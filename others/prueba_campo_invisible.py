import PySimpleGUI as sg

layout = [
    [sg.Text('Nombre')],
    [sg.Input(key='nombre')],
    [sg.Text('Apellido')],
    [sg.Input(key='apellido')],
    [sg.CalendarButton('Seleccionar Fecha', target='fecha_input', format='%Y-%m-%d', key='fecha_button')],
    [sg.Input(key='fecha_input', disabled=True)],
    [sg.Text('Campo Invisible', visible=False, key='campo_invisible')],
    [sg.Button('Mostrar Campo Invisible'), sg.Button('Ocultar Campo Invisible'), sg.Button('Salir')]
]

window = sg.Window('Ejemplo de Campo Invisible', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Salir':
        break
    elif event == 'Mostrar Campo Invisible':
        window['campo_invisible'].update(visible=True)
    elif event == 'Ocultar Campo Invisible':
        window['campo_invisible'].update(visible=False)

window.close()
