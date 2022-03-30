from dash import dcc, html
import ui_constants as ui


def __get_label(text):
    return html.P([text], style={'font-weight': 'bold', 'text-align': 'center'})


def __get_empty_div():
    return html.Div(className='four columns div-user-controls',
                    children=[])


def get(fig, files):
    default_file_value = 0

    if len(files) > 0:
        default_file_value = files[0]['value']

    dropdown1 = dcc.Dropdown(id='file1_selection',
                             options=files,
                             value=default_file_value,
                             placeholder='Select file 1...',
                             optionHeight=60,
                             multi=False,
                             clearable=False,
                             searchable=True)

    dropdown2 = dcc.Dropdown(id='file2_selection',
                             options=files,
                             value=default_file_value,
                             placeholder='Select file 2...',
                             optionHeight=60,
                             multi=False,
                             clearable=False,
                             searchable=True)

    dropdown3 = dcc.Dropdown(id='plot_selection',
                             options=ui.plotting_options,
                             placeholder='Select plot type...',
                             value=0,
                             optionHeight=60,
                             multi=False,
                             clearable=False)

    return html.Div(children=[
        html.Div(className='row',  # Define the row element
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[__get_label('File 1'), dropdown1, __get_label('File 2'), dropdown2,
                                        __get_label('Plot selection'), dropdown3]),
                     # Define the left element
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  html.Div([dcc.Graph(id='the_graph', figure=fig)])
                              ]
                              ),
                     # Define the right element
                 ])
    ])
