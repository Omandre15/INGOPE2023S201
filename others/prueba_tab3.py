import PySimpleGUI as sg

layout = [
    [
        sg.Column([
            [sg.Button('Tab 1', size=(10, 1), key='-TAB1-', pad=(0, 5), expand_y=True )],
            [sg.Button('Tab 2', size=(10, 1), key='-TAB2-', pad=(0, 5), expand_y=True)],
            [sg.Button('Tab 3', size=(10, 1), key='-TAB3-', pad=(0, 5), expand_y=True, disabled=False)],
        ], element_justification='center', vertical_alignment='top', expand_y=True),
        sg.Column([
            [sg.Text('Contenido de la pestaña 1', key='-TAB1-CONTENT-', size=(30, 10), background_color='red', expand_y=True, visible=False)],
            [sg.Text('Contenido de la pestaña 2', key='-TAB2-CONTENT-', size=(30, 10), background_color='blue', expand_y=True, visible=False)],
            [sg.Text('Contenido de la pestaña 3', key='-TAB3-CONTENT-', size=(30, 10), background_color='green', expand_y=True, visible=False)],
        ])
    ]
]

window = sg.Window('Tabs en el Costado', layout)

while True:
    event, _ = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event in ('-TAB1-', '-TAB2-', '-TAB3-'):
        window['-TAB1-CONTENT-'].update(visible=event == '-TAB1-')
        window['-TAB2-CONTENT-'].update(visible=event == '-TAB2-')
        window['-TAB3-CONTENT-'].update(visible=event == '-TAB3-')
        # window['-TAB3-'].update(disabled=True)

window.close()
