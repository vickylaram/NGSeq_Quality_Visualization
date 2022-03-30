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

# Initialize needed variables
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
    """Updates graph according to user selection

    :param file1_selection: first file selection, taken from component of the same name (dropdown)
    :param file2_selection: second file selection
    :param plot_selection: plot type to be created
    :return: figure of selected input params
    """

    file1 = __data[file1_selection][plot_selection]

    plot_file = file1

    # To be able to compare two files it has to made sure that the input doesn't get compared to itself
    # thus resulting in 0
    if file1_selection != file2_selection:
        file2 = __data[file2_selection][plot_selection]
        plot_file = file2 - file1

    # Plot according to selection, see plot.py and ui_constants.py for more information
    if plot_selection in ui.table_ids:
        fig = plot.basic_statistics(plot_file)

    elif plot_selection in ui.boxplot_ids:
        fig = plot.boxplot(plot_file)

    elif plot_selection in ui.tileplot_id:
        fig = plot.tile(plot_file)

    elif plot_selection in ui.graph_ids:
        fig = plot.line(plot_file, plot_selection)

    # Add title to plot
    fig.update_layout(
        title={'text': ui.plotting_options[plot_selection]['label'], 'font': {'size': 28}, 'x': 0.5,
               'xanchor': 'center'})
    return fig


# Application entry point
if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Take path from programs params
        fastqc_output_path = str(sys.argv[1])
        # Read data from provided path
        __data = io.read_fastqc_data(fastqc_output_path)
        # Create a list of available files for UI
        available_files = io.get_available_files(__data)
        # Assemble layout
        app.layout = layout.get(fig, available_files)
        # Run waitress server since Flask's default server is not recommended for production use
        serve(app.server, host='0.0.0.0', port=8000)
    else:
        print('Please provide path')
        # raise FileNotFoundError
