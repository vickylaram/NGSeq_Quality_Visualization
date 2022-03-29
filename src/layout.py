from dash import dcc, html
import ui_constants as ui


def get_layout(fig, files):
    dropdown1 = dcc.Dropdown(id='file_selection1_dropdown',
                             options=files,
                             value=0,
                             optionHeight=60,
                             multi=False,
                             clearable=False,
                             searchable=True)

    dropdown2 = dcc.Dropdown(id='file_selection2_dropdown',
                             options=files,
                             value=0,
                             optionHeight=60,
                             multi=False,
                             clearable=False,
                             searchable=True)

    dropdown3 = dcc.Dropdown(id='plot_selection_dropdown',
                             options=ui.plotting_options,
                             value=0,
                             optionHeight=60,
                             multi=False,
                             clearable=False)
    div = html.Div(className='four columns div-user-controls',
                   children=[])

    return html.Div(children=[
        html.Div(className='row',  # Define the row element
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[dropdown1, div, dropdown2, div, dropdown3]),  # Define the left element
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  html.Div([dcc.Graph(id='the_graph', figure=fig)])
                              ]
                              ),
                     # Define the right element
                 ])
    ])