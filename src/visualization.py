import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import io_util as io
import numpy as np

import os
import sys

fig = px.line()
fastqc_output_path = ""  # io.get_fastqc_output_path()
__data = []  # io.read_fastqc_data(fastqc_output_path)
available_files = []
app = dash.Dash()

table_ids = [0]
boxplot_ids = [1]
tileplot_ids = [2]
graph_ids = [3, 4, 5, 6, 7, 8, 9]

plotting_options = [{'label': 'Basic Statistics', 'value': 0},
                    {'label': 'Per base sequence quality', 'value': 1},
                    {'label': 'Per tile sequence quality',
                     'value': 2},
                    {'label': 'Per sequence quality scores', 'value': 3},
                    {'label': 'Per base sequence content',
                     'value': 4},
                    {'label': 'Per sequence GC content',
                     'value': 5},
                    {'label': 'Per base N content', 'value': 6},
                    {'label': 'Sequence Length Distribution',
                     'value': 7},
                    {'label': 'Sequence Duplication Levels',
                     'value': 8},
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


def run_app():
    # __d = io.read_fastqc_data(fastqc_output_path)
    # __data = __d
    # __get_available_files(__data)
    # print(available_files)
    # print(__data)
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
                          ),
                 # Define the right element
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
        fig = px.line(plot_file, x=plot_file.iloc[:, 0], y=plot_file.iloc[:, 1],
                      labels=dict(x=plot_file.columns[0], y=plot_file.columns[1]))
        #fig.add_trace(px.box(plot_file, x=plot_file['Base'], y=plot_file.iloc[:, 3:5].to_numpy()))
        #fig = px.box(plot_file, x="Position in read (bp)")
        df = plot_file.iloc[:, 3:5].transpose()
        df.columns = plot_file.iloc[:, 0]
        for col in df:
            fig.add_trace(go.Box(y=df[col].values, name=df[col].name))

        df2 = plot_file.iloc[:, 5:7].transpose()
        df2.columns = plot_file.iloc[:, 0]

        for col in df2:
            fig.add_trace(go.Box(y=df2[col].values, name=df2[col].name))

        print(df2)


    elif plot_selection_dropdown in tileplot_ids:
        unique_index = plot_file['Tile'].unique()
        unique_base = plot_file['Base'].unique()
        #unique_index_rev = np.flipud(unique_index)
        data = []
        for index in unique_index:
            t = plot_file[plot_file['Tile'] == index]
            dat = []
            print(type(index))

            for base in unique_base:
                print(type(base))
                dat.append(t[t['Base'] == base]['Mean'].values[0])


            data.append(dat)

        fig = go.Figure(data=go.Heatmap(z=data, x = unique_base, y = unique_index, colorscale='teal'))

        #fig = px.imshow(data, x = unique_base, y = unique_index)

        fig.update_layout(xaxis = dict (tickmode='linear'),
                          yaxis = dict (tickmode='linear'))

        fig.update_layout(yaxis = dict(scaleanchor = 'x'))
#
    elif plot_selection_dropdown in graph_ids:
        fig = px.line(plot_file, x=plot_file.iloc[:, 0], y=plot_file.iloc[:, 1],
                      labels=dict(x=plot_file.columns[0], y=plot_file.columns[1]))
        # print(plot_file)
        if plot_selection_dropdown == 4:
            fig = px.line(plot_file, x=plot_file.iloc[:, 0],
                          y=[plot_file.iloc[:, 1], plot_file.iloc[:, 2], plot_file.iloc[:, 3], plot_file.iloc[:, 4]],
                          labels=dict(x=plot_file.columns[0], y=plot_file.columns[1]))
        if plot_selection_dropdown == 8:
            fig = px.line(plot_file, x=plot_file.iloc[:, 0],
                          y=[plot_file.iloc[:, 1], plot_file.iloc[:, 2]],
                          labels=dict(x=plot_file.columns[0], y=plot_file.columns[1]))
        if plot_selection_dropdown == 9:
            fig = px.line(plot_file, x=plot_file.iloc[:, 0],
                          y=[plot_file.iloc[:, 1], plot_file.iloc[:, 2], plot_file.iloc[:, 3], plot_file.iloc[:, 4],
                             plot_file.iloc[:, 5]],
                          labels=dict(x=plot_file.columns[0], y=plot_file.columns[1]))

    # fig.update_traces(textinfo='percent+label')
    fig.update_layout(title={'text': plotting_options[plot_selection_dropdown]['label'], 'font': {'size': 28}, 'x': 0.5,
                             'xanchor': 'center'})
    return fig


def __get_available_files(__data):
    for entry in __data:
        available_files.append({'label': entry, 'value': entry})
