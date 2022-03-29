import dash
from waitress import serve
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import io_util as io
import ui_constants as ui
import layout as l
import sys

fig = px.line()
fastqc_output_path = ""  # io.get_fastqc_output_path()
__data = []  # io.read_fastqc_data(fastqc_output_path)
__available_files = []
app = dash.Dash()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fastqc_output_path = str(sys.argv[1])
        __data = io.read_fastqc_data(fastqc_output_path)
        available_files = io.get_available_files(__data)
        app.layout = l.get_layout(fig, available_files)
        #serve(app.server, host='0.0.0.0', port=8000)
        app.run_server(debug=True)
    else:
        print("Please provide path")
        # raise FileNotFoundError


@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='file_selection1_dropdown', component_property='value'),
     Input(component_id='file_selection2_dropdown', component_property='value'),
     Input(component_id='plot_selection_dropdown', component_property='value')]
)
def update_graph(file_selection1_dropdown, file_selection2_dropdown, plot_selection_dropdown):
    # global fig
    print(file_selection1_dropdown, plot_selection_dropdown)

    file1 = __data[file_selection1_dropdown][plot_selection_dropdown]

    plot_file = file1
    if file_selection1_dropdown != file_selection2_dropdown:
        file2 = __data[file_selection2_dropdown][plot_selection_dropdown]
        plot_file = file2 - file1

    if plot_selection_dropdown in ui.table_ids:
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

    elif plot_selection_dropdown in ui.boxplot_ids:
        fig = px.line(plot_file, x=plot_file.iloc[:, 0], y=plot_file.iloc[:, 1],
                      labels=dict(x=plot_file.columns[0], y=plot_file.columns[1]))

        traces = []

        df = plot_file.iloc[:, 2:7].transpose()
        df.columns = plot_file.iloc[:, 0]
        for col in df:
            fig.add_trace(
                go.Box(y=df[col].values, name=df[col].name, line=dict(color='black'), fillcolor='rgba(255,255,0,0.5)'))
            # fig.add_trace(go.Box(y=df2[col].values, name=df2[col].name, line=dict(color='red')))

    elif plot_selection_dropdown in ui.tileplot_ids:
        unique_index = plot_file['Tile'].unique()
        unique_base = plot_file['Base'].unique()
        # unique_index_rev = np.flipud(unique_index)
        data = []
        for index in unique_index:
            t = plot_file[plot_file['Tile'] == index]
            dat = []

            for base in unique_base:
                dat.append(t[t['Base'] == base]['Mean'].values[0])

            data.append(dat)

        fig = go.Figure(data=go.Heatmap(z=data, x=unique_base, y=unique_index, colorscale='teal'))

        # fig = px.imshow(data, x = unique_base, y = unique_index)

        fig.update_layout(xaxis=dict(tickmode='linear'),
                          yaxis=dict(tickmode='linear'))

        fig.update_layout(yaxis=dict(scaleanchor='x'))
    #
    elif plot_selection_dropdown in ui.graph_ids:
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
    fig.update_layout(
        title={'text': ui.plotting_options[plot_selection_dropdown]['label'], 'font': {'size': 28}, 'x': 0.5,
               'xanchor': 'center'})
    return fig
