import dash
from waitress import serve
from dash.dependencies import Input, Output
import io_util as io
import plotly.graph_objects as go
import plotly.express as px
import ui_constants as ui
import plot
import layout
import sys

fig = go.Figure()
fastqc_output_path = ''
__data = []
__available_files = []
app = dash.Dash()


@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='file1_selection', component_property='value'),
     Input(component_id='file2_selection', component_property='value'),
     Input(component_id='plot_selection', component_property='value')]
)
def update_graph(file1_selection, file2_selection, plot_selection):
    # global fig
    file1 = __data[file1_selection][plot_selection]

    plot_file = file1
    if file1_selection != file2_selection:
        file2 = __data[file2_selection][plot_selection]
        plot_file = file2 - file1

    if plot_selection in ui.table_ids:
        fig = plot.basic_statistics(plot_file)

    elif plot_selection in ui.boxplot_ids:
        fig = plot.boxplot(plot_file)

    elif plot_selection in ui.tileplot_id:
        fig = plot.tile(plot_file)

    elif plot_selection in ui.graph_ids:
        fig = plot.line(plot_file, plot_selection)

    fig.update_layout(
        title={'text': ui.plotting_options[plot_selection]['label'], 'font': {'size': 28}, 'x': 0.5,
               'xanchor': 'center'})
    return fig


if __name__ == '__main__':
    if len(sys.argv) > 1:
        fastqc_output_path = str(sys.argv[1])
        __data = io.read_fastqc_data(fastqc_output_path)
        available_files = io.get_available_files(__data)
        app.layout = layout.get(fig, available_files)
        app.run_server(debug=True)
    else:
        print('Please provide path')
        # raise FileNotFoundError
