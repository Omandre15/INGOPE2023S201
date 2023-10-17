import PySimpleGUI as sg

layout = [
    [sg.TabGroup([
        [sg.Tab('Tab 1', [[sg.Text('Contenido de la pestaña 1')]], key='-t1-')],
        [sg.Tab('Tab 2', [[sg.Text('Contenido de la pestaña 2')]])],
        [sg.Tab('Tab 3', [[sg.Text('Contenido de la pestaña 3')]])]
    ], key='-TABGROUP-', size=(500,200), enable_events=True)],
    [sg.Button('Deshabilitar Tab', key='-DISABLE-TAB-')]
]

window = sg.Window('Deshabilitar Tab', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-DISABLE-TAB-':
        tab_group = window['-TABGROUP-']
        estado = tab_group.Widget.tab(1)['state']
        n_estado = 'normal' if estado == 'disabled' else 'disabled'
        tab_group.Widget.tab(1, state=n_estado)
        #tab_group.Widget.tab(1, state='disabled')

window.close()
