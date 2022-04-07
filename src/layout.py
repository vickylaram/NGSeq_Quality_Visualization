from dash import dcc, html
import plotly.graph_objects as go
import ui_constants as ui


def __get_label(text: str) -> html.P:
    """Convenience method to create a text label

    :param text: text to be put in label
    :return: HTML text label
    """
    return html.P([text], style={'font-weight': 'bold', 'text-align': 'center'})


def __get_empty_div() -> html.Div:
    """Convenience method for empty section

    :return: empty (child-less) HTML div
    """
    return html.Div(className='four columns div-user-controls',
                    children=[])


def get(fig: go.Figure, files: list[dict[str, str]]) -> html.Div:
    """Convenience method to assemble application layout

    :param fig: empty Plotly GO object
    :param files: list of available files for the file selection dropdowns
    :return: entire, ready to use HTML layout
    """
    default_file_value = 0

    # Check if list of available files is not empty, so the first element can be extracted for
    # the default dropdown value
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
                             options=ui.PLOTTING_OPTIONS,
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
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  html.Div([dcc.Graph(id='the_graph', figure=fig)])
                              ]
                              ),
                 ])
    ])
