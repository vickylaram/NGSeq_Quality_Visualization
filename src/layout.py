from dash import dcc, html
import ui_constants as ui

def __get_label(text):
    return html.P([text], style={'font-weight': 'bold', "text-align": "center"})


def get(fig, files):
    default_file_value = 0

    if len(files) > 0:
        default_file_value = files[0]['value']  # next(iter(files.values()))

    dropdown1 = dcc.Dropdown(id='file_selection1_dropdown',
                             options=files,
                             value=default_file_value,
                             placeholder='Select file 1...',
                             optionHeight=60,
                             multi=False,
                             clearable=False,
                             searchable=True)

    dropdown2 = dcc.Dropdown(id='file_selection2_dropdown',
                             options=files,
                             value=default_file_value,
                             placeholder='Select file 2...',
                             optionHeight=60,
                             multi=False,
                             clearable=False,
                             searchable=True)

    dropdown3 = dcc.Dropdown(id='plot_selection_dropdown',
                             options=ui.plotting_options,
                             placeholder='Select plot type...',
                             value=0,
                             optionHeight=60,
                             multi=False,
                             clearable=False)
    empty_div = html.Div(className='four columns div-user-controls',
                         children=[], style={'marginBottom': 5, 'marginTop': 5})

    return html.Div(children=[
        html.Div(className='row',  # Define the row element
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[__get_label('File 1'), dropdown1, __get_label('File 2'), dropdown2, __get_label('Plot selection'), dropdown3]),
                     # Define the left element
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  html.Div([dcc.Graph(id='the_graph', figure=fig)])
                              ]
                              ),
                     # Define the right element
                 ])
    ])
