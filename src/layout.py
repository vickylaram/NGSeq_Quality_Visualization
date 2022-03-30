from dash import dcc, html
import ui_constants as ui


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
                         children=[])

    div_1 = html.P(['File 1'], style={'font-weight': 'bold'})

    div_2 = html.P(['File 2'], style={'font-weight': 'bold', "text-align": "center"})

    div_3 = html.P(['Plot selection'], style={'font-weight': 'bold', "text-align": "center"})

    div1 = html.Div(className='four columns div-user-controls',
                    children=[empty_div, div_1], style={'marginBottom': 5, 'marginTop': 5})

    div2 = html.Div(className='four columns div-user-controls',
                    children=[empty_div, div_2], style={'marginBottom': 5, 'marginTop': 5})

    div3 = html.Div(className='four columns div-user-controls',
                    children=[empty_div, div_3], style={'marginBottom': 5, 'marginTop': 5})

    return html.Div(children=[

        html.H1(id='FastQC Data Visualisation', style={'text-align': 'center'}),

        html.Div(className='row',  # Define the row element
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[div1, dropdown1, div2, dropdown2, div3, dropdown3]),
                     # Define the left element
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  html.Div([dcc.Graph(id='the_graph', figure=fig)])
                              ]
                              ),
                     # Define the right element
                 ])
    ])
