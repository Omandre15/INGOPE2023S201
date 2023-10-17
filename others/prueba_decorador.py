import PySimpleGUI as psg


def cambiar_color(buton):
    buton.update(button_color=('red','green'))
    return buton

b = psg.Button('asfa', button_color=('red','green'))

layout = [
    [
        psg.Text(text='Hello World',
                 font=('Arial Bold', 20),
                 size=20,
                 expand_x=True,
                 justification='center')
    ],
    [
        psg.Button('Texto', key='x'),
        b
    ]
]
window = psg.Window('HelloWorld', layout, size=(715, 250), finalize=True)
cambiar_color(window['x'])
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
window.close()
