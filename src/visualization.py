import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import io_util as io

import io_util as io

fig = px.line()

app = dash.Dash()

table_ids = [0]
boxplot_ids = [1]
tileplot_ids = [2]
graph_ids = [3, 4, 5, 6, 7, 9]

available_files = []

plotting_options = [{'label': 'Basic Statistics', 'value': 0},
                    {'label': 'Per base sequence quality', 'value': 1, 'disabled': True},
                    {'label': 'Per tile sequence quality',
                     'value': 2, 'disabled': True},
                    {'label': 'Per sequence quality scores', 'value': 3},
                    {'label': 'Per base sequence content',
                     'value': 4},
                    {'label': 'Per sequence GC content',
                     'value': 5},
                    {'label': 'Per base N content', 'value': 6},
                    {'label': 'Sequence Length Distribution',
                     'value': 7},
                    {'label': 'Sequence Duplication Levels',
                     'value': 8, 'disabled': True},
                    {'label': 'Adapter Content', 'value': 9}]

dropdown1 = dcc.Dropdown(id='file_selection1_dropdown',
                         options=available_files,
                         value=0,
                         optionHeight=60,
                         multi=False,
                         clearable=False,
                         searchable=True)

dropdown2 = dcc.Dropdown(id='file_selection2_dropdown',
                         options=available_files,
                         value=0,
                         optionHeight=60,
                         multi=False,
                         clearable=False,
                         searchable=True)

dropdown3 = dcc.Dropdown(id='plot_selection_dropdown',
                         options=plotting_options,
                         value=0,
                         optionHeight=35,
                         multi=False,
                         clearable=False)
div = html.Div(className='four columns div-user-controls',
               children=[])


def init():
    fastqc_output_path = io.get_fastqc_output_path()
    if fastqc_output_path is not None:
        __data = io.read_fastqc_data(fastqc_output_path)
        __get_available_files(__data)
    else:
        print('Non existant output directory! Please run pipeline first')
        exit(-1)


def run_app():
    init()
    app.run_server(debug=True)


colors = {
    'background': '#FC0AB3',
    'text': '#FFFFFF'
}

app.layout = html.Div(children=[
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='four columns div-user-controls',
                          children=[dropdown1, div, dropdown2, div, dropdown3]),  # Define the left element
                 html.Div(className='eight columns div-for-charts bg-grey',
                          children=[
                              html.Div([dcc.Graph(id='the_graph', figure=fig)])
                          ]
                          )  # Define the right element
             ])
])


@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='file_selection1_dropdown', component_property='value'),
     Input(component_id='file_selection2_dropdown', component_property='value'),
     Input(component_id='plot_selection_dropdown', component_property='value')]
)
def update_graph(file_selection1_dropdown, file_selection2_dropdown, plot_selection_dropdown):
    # global fig
    file1 = __data[file_selection1_dropdown][plot_selection_dropdown]
    plot_file = file1
    if (file_selection1_dropdown != file_selection2_dropdown):
        file2 = __data[file_selection2_dropdown][plot_selection_dropdown]
        plot_file = file2 - file1

    if plot_selection_dropdown in table_ids:
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(plot_file.columns),
                        fill_color='indigo',
                        font=dict(color='white', size=18),
                        align='left'),
            cells=dict(values=[plot_file.Measure, plot_file.Value],
                       fill_color='lavender',
                       font=dict(size=13),
                       align='left'))
        ])

    elif plot_selection_dropdown in boxplot_ids:
        fig = px.box(plot_file, x="Lower Quartile", y="Upper Quartile")
    elif plot_selection_dropdown in tileplot_ids:
        fig = px.line(plot_file, x=plot_file.iloc[:, 0], y=plot_file.iloc[:, 1])
    elif plot_selection_dropdown in graph_ids:
        fig = px.line(plot_file, x=plot_file.iloc[:, 0], y=plot_file.iloc[:, 1],
                      labels=dict(x=plot_file.columns[0], y=plot_file.columns[1]))
        if plot_selection_dropdown == 4:
            fig = px.line(plot_file, x=plot_file.iloc[:, 0],
                          y=[plot_file.iloc[:, 1], plot_file.iloc[:, 2], plot_file.iloc[:, 3], plot_file.iloc[:, 4]],
                          labels=dict(x=plot_file.columns[0], y=plot_file.columns[1]))
        if plot_selection_dropdown == 7:
            print(plot_file)

    # fig.update_traces(textinfo='percent+label')
    fig.update_layout(title={'text': plotting_options[plot_selection_dropdown]['label'], 'font': {'size': 28}, 'x': 0.5,
                             'xanchor': 'center'})
    return fig


def __get_available_files(__data):
    for entry in __data:
        available_files.append({'label': entry, 'value': entry})
