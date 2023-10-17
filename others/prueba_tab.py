import PySimpleGUI as sg

tab1 = sg.Tab('Tab 1', [[sg.Text('Contenido del Tab 1')]], key='tab1')
tab2 = sg.Tab('Tab 2', [[sg.Text('Contenido del Tab 2')]], key='tab2')
tab3 = sg.Tab('Tab 3', [[sg.Text('Contenido del Tab 3')]], key='tab3')
tabsGroup = sg.TabGroup([
    [tab1],
    [tab2],
    [tab3]
], key='-TABGROUP-',enable_events=True)
layout = [
    [tabsGroup],
    [sg.Button('Seleccionar Tab 2', key='-SELECT-TAB-2-')]
]

window = sg.Window('Ejemplo de Selección de Tab', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-SELECT-TAB-2-':
        tab_group = window['-TABGROUP-']
        # tab2.select()


        tab_group.Widget.select(tab_group.Widget.tabs()[1])  # Selecciona el segundo tab (índice 1)
        tab_group.Widget.tabs()[0].update()
window.close()
