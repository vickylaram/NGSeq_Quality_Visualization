import dash
from waitress import serve
from dash.dependencies import Input, Output
import io_util as io
import plotly.graph_objects as go

import ui_constants
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
def update_graph(file1_selection: str, file2_selection: str, plot_selection: int) -> go.Figure:
    """Updates graph according to user selection

    :param file1_selection: first file selection, taken from component of the same name (dropdown)
    :param file2_selection: second file selection
    :param plot_selection: plot type to be created
    :return: figure of selected input params
    """

    # Handle the case if Overrepresented Sequences are present
    table_ids = ui.table_ids_without_overrep

    selection_id = plot_selection

    if len(__data[file1_selection]) == 10 and plot_selection == 10:
        plot_selection = plot_selection - 1

    if len(__data[file1_selection]) == 11:
        table_ids = ui.table_ids_with_overrep

        if plot_selection == 9:
            selection_id = plot_selection + 1

        if plot_selection == 10:
            selection_id = plot_selection - 1


    file1 = __data[file1_selection][selection_id][1]

    plot_file = file1

    # To be able to compare two files it has to made sure that the input doesn't get compared to itself
    # thus resulting in 0
    # if file1_selection != file2_selection and plot_selection in ui.graph_ids:
    #    file2 = __data[file2_selection][plot_selection][1]
    #    plot_file = file2 - file1

    # Plot according to selection, see plot.py and ui_constants.py for more information
    if plot_selection in table_ids:
        fig = plot.table(plot_file, plot_selection)

    elif plot_selection in ui.boxplot_ids:
        fig = plot.boxplot(plot_file)

    elif plot_selection in ui.tileplot_id:
        fig = plot.tile(plot_file)

    elif plot_selection in ui.graph_ids:
        fig = plot.line(plot_file, plot_selection)

    # Add title to plot
    fig.update_layout(
        title={'text': ui.PLOTTING_OPTIONS[plot_selection]['label'] + " - " + __get_status_string(
            __data[file1_selection][plot_selection][0]) + __get_plot_subtitle(plot_selection), 'font': {'size': 28},
               'x': 0.5,
               'xanchor': 'center'})
    return fig


def __get_status_string(status: str) -> str:
    """Function to convert FastQC module status into more userfriendly string

    :param status: raw status string
    :return: prettyfied status string
    """
    if status == 'pass':
        return 'Pass ✓'
    if status == 'warn':
        return 'Warn !'
    return "Fail ❌"


def __get_plot_subtitle(plot_selection: int) -> str:
    """Helper function to add subtitles to plots

    :param plot_selection: integer of selected plot
    :return: string of subtitle
    """
    part1 = '<br><sup>'
    part2 = '</sup>'
    if plot_selection == 3:
        return part1 + ui.subtitle_3 + part2
    if plot_selection == 4:
        return part1 + ui.subtitle_4 + part2
    if plot_selection == 5:
        return part1 + ui.subtitle_5 + part2
    if plot_selection == 6:
        return part1 + ui.subtitle_6 + part2
    if plot_selection == 7:
        return part1 + ui.subtitle_7 + part2
    if plot_selection == 8:
        return part1 + ui.subtitle_8 + part2
    if plot_selection == 9:
        return part1 + ui.subtitle_9 + part2
    return ''


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
