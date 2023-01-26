from nicegui import ui
from json import loads
from numpy.random import random


# with open("data.json","r") as data_json:
#     data_dict = loads(data_json.read())

# main_id_list = []
#
# for device in data_dict["devices"]:
#     main_id_list.append({"id": device["main-id"]})


ui.label('Inteligentne podlewanie').classes('text-h5')

ui.tree([
    {'id': 'Main_ID', 'children': [
        {'id': '10', 'children': [
            {'id': 'Sensor_ID', 'children': [
                {'id': '9'}
            ]},
            {'id': 'Valve_ID', 'children': [
                {'id': '1'}
            ]},
        ]},
        {'id': '11', 'children': [
            {'id': 'Sensor_ID', 'children': [
                {'id': '8'}
            ]},
            {'id': 'Valve_ID', 'children': [
                {'id': '2'}
            ]},
        ]}
        ]
     }
],
label_key='id', on_select=lambda e: ui.notify(e.value))


chart = ui.chart({
    'title': False,
    'chart': {'type': 'bar'},
    'xAxis': {'categories': ['Sensor Node']},
    'series': [
        {'name': 'Air Temperature [C]', 'data': [0]},
        {'name': 'Air Humidity [%]', 'data': [0]},
        {'name': 'Soil Moisture [%]', 'data': [0]},
        {'name': 'Battery Level [%]', 'data': [0]}
    ]
}).classes('w-full h-64')


def chart_update():
    chart.options['series'][0]['data'][:] = 50 * random(1)
    chart.options['series'][1]['data'][:] = 100 * random(1)
    chart.options['series'][2]['data'][:] = 100 * random(1)
    chart.options['series'][3]['data'][:] = 100 * random(1)
    chart.update()


ui.button('Update', on_click = chart_update)

# chart = ui.chart({
#     'title': False,
#     'chart': {'type': 'bar'},
#     'xAxis': {'categories': ['A', 'B']},
#     'series': [
#         {'name': 'Alpha', 'data': [0.1, 0.2]},
#         {'name': 'Beta', 'data': [0.3, 0.4]},
#     ],
# }).classes('w-full h-64')
#
# def update():
#     chart.options['series'][0]['data'][:] = random(2)
#     chart.update()
#
# ui.button('Update', on_click=update)

ui.run(title='Roszczepantek są supi')
