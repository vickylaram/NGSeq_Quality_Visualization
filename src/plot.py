import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def table(data: pd.DataFrame, selection_id: int) -> go.Figure:
    """Plots the basic statistics or overrepresented sequences module as a table

    :param data: data from FastQC 'Basic Statistics' or 'Overrepresented sequences' result module as a Pandas DataFrame
    :param selection_id: exact id of selection for correct plotting
    :return: Plotly Graph Objects/Table figure filled with data provided in params
    """

    if selection_id == 0:
        return go.Figure(data=[go.Table(
            header=dict(values=list(data.columns),
                        fill_color='indigo',
                        font=dict(color='white', size=18),
                        align='left'),
            cells=dict(values=[data.Measure, data.Value],
                       fill_color='lavender',
                       font=dict(size=13),
                       align='left'))
        ])

    if selection_id == 10:
        print(data.columns)
        return go.Figure(data=[go.Table(
            header=dict(values=list(data.columns),
                        fill_color='indigo',
                        font=dict(color='white', size=18),
                        align='left'),
            cells=dict(values=[data.Sequence, data.Count, data.Percentage, data['Possible Source']],
                       fill_color='lavender',
                       font=dict(size=13),
                       align='left'))
        ])


def boxplot(data: pd.DataFrame) -> go.Figure:
    """Plots the per base sequence quality module (Boxplot)

    :param data: data from FastQC 'Per base sequence quality' result module as a Pandas DataFrame
    :return: Plotly Graph Objects boxplot figure filled with data provided in params
    """

    fig = px.line(data, x=data.iloc[:, 0], y=data.iloc[:, 1],
                  labels=dict(x=data.columns[0], y=data.columns[1]))

    df = data.iloc[:, 2:7].transpose()
    df.columns = data.iloc[:, 0]
    for col in df:
        fig.add_trace(
            go.Box(y=df[col].values, name=df[col].name, line=dict(color='black'), fillcolor='rgba(255,255,0,0.5)'))
        # fig.add_trace(go.Box(y=df2[col].values, name=df2[col].name, line=dict(color='red')))
    fig.update_layout(
        xaxis_title="Position in read (bp)"
    )

    # Quality scored across all bases /Sanger /Illumina 1.9 encoding

    return fig


def tile(data: pd.DataFrame) -> go.Figure:
    """Plots the per tile sequence quality module (tile plot/heatmap)

    :param data: data from FastQC 'Per tile sequence quality' result module as a Pandas DataFrame
    :return: Plotly heatmap figure filled with data provided in params
    """
    unique_index = data['Tile'].unique()
    unique_base = data['Base'].unique()
    # unique_index_rev = np.flipud(unique_index)
    data = []
    for index in unique_index:
        t = data[data['Tile'] == index]
        dat = []

        for base in unique_base:
            dat.append(t[t['Base'] == base]['Mean'].values[0])

        data.append(dat)

    fig = go.Figure(data=go.Heatmap(z=data, x=unique_base, y=unique_index, colorscale='teal'))

    # fig = px.imshow(data, x = unique_base, y = unique_index)

    fig.update_layout(xaxis=dict(tickmode='linear'),
                      yaxis=dict(tickmode='linear'))

    fig.update_layout(yaxis=dict(scaleanchor='x'))

    fig.update_layout(
        xaxis_title="Position in read (bp)"
    )
    return fig


def line(data: pd.DataFrame, selection_id: int) -> go.Figure:
    """Plots any module that is supposed to be a line plot (see ui_constants.py),
    depending on the selection. (Some line plots are based on two columns, some
    on more.)

    :param data: Pandas dataframe of FastQC result module
    :param selection_id: exact id of selection for correct plotting
    :return: Plotly line plot figure filled with data provided in params
    """

    # Assumption: data from params usually only have two columns present (x,y)...
    fig = px.line(data, x=data.iloc[:, 0], y=data.iloc[:, 1],
                  labels=dict(x=data.columns[0], y=data.columns[1]))

    if selection_id == 6:
        #
        fig.update_layout(
            xaxis_title="Position in read (bp)"
        )

    # Average quality per read
    if selection_id == 3:
        fig.update_layout(
            xaxis_title="Mean Sequence Quality (Phred Score)"
        )

    if selection_id == 5:
        #
        # Label. GC count per read
        fig.update_layout(
            xaxis_title="Mean GC content (%)"
        )

        # __calculate_dist(data, fig)
        # print("Normal Distribution")

    # ...but certain modules have more than two columns, meaning the selection_id needs to be checked
    # ID = 4: Per base sequence content
    if selection_id == 4:
        # Sequence content across all bases
        fig = px.line(data, x=data.iloc[:, 0],
                      y=[data.iloc[:, 1], data.iloc[:, 2], data.iloc[:, 3], data.iloc[:, 4]],
                      labels={
                          "G": "%G",
                          "A": "%A",
                          "T": "%T",
                          "C": "%C"
                      }
                      )
        fig.update_layout(
            xaxis_title="Position in read (bp)"
        )

    if selection_id == 7:
        #
        #Sequence length
        fig.update_layout(
            xaxis_title="Sequence Length (bp)"
        )

    # ID = 8: Sequence Duplication Levels
    if selection_id == 8:
        # - 37.25 %
        #Deduplicated sequences - Total sequences
        fig = px.line(data, x=data.iloc[:, 0],
                      y=[data.iloc[:, 1], data.iloc[:, 2]],
                      labels=dict(x=data.columns[0], y=data.columns[1]))
        fig.update_layout(
            xaxis_title="Sequence Duplication level"
        )

    # ID = 9: Adapter Content
    if selection_id == 9:
        fig = px.line(data, x=data.iloc[:, 0],
                      y=[data.iloc[:, 1], data.iloc[:, 2], data.iloc[:, 3], data.iloc[:, 4],
                         data.iloc[:, 5]],
                      labels=dict(x=data.columns[0], y=data.columns[1]))
    fig.update_layout(
        xaxis_title="Position in read (bp)"
    )
    #Labels: die geräte

    return fig


"""
# Source: https://github.com/s-andrews/FastQC/blob/master/uk/ac/babraham/FastQC/Modules/PerSequenceGCContent.java
def __calculate_dist(gc_dist, fig):
    Because the GC module doesn't provide the needed data for the theoretical distribution
    I basically stole the logic and converted it into Python


    :param data:
    :param fig:
    :return:
    
    # gc_dist = np.empty(len(gc_dist.iloc[:, 1]))
    theoretical_dist = np.empty(len(gc_dist.iloc[:, 1]))

    max = 0
    x_categories = np.empty(len(gc_dist.iloc[:, 1]))

    total_count = 0

    first_mode = 0
    mode_count = 0

    x_categories = gc_dist.iloc[:, 0].copy()
    total_count = gc_dist.iloc[:, 1].sum()
    max = gc_dist.iloc[:, 1].max()

    mode = 0
    mode_duplicates = 0

    fell_off_top = True

    temp = gc_dist.iloc[first_mode:len(gc_dist), 1]

    fell_off_bottom = True

    if fell_off_bottom or fell_off_top:
        mode = first_mode
    else:
        mode /= mode_duplicates

    std_dev = 0  # double

    # mode equals mean
    std_dev /= total_count - 1
    std_dev = math.sqrt(std_dev)

    deviation_percent = 0

    stdev = np.std(std_dev)

    deviation_percent = 0  # double

    probabilities = __get_z_score_for_value(values, stdev, mode)
    theoretical_dist = probabilities*total_count
    max = theoretical_dist.max()

    deviation_percent += abs(theoretical_dist-gc_dist)

    deviation_percent /= total_count
    deviation_percent *= 100

    return True


def __get_z_score_for_value(value: float, stdev: float, mean: float):

    lhs = float(1) / (math.sqrt(2 * math.pi * stdev * stdev))
    rhs = math.pow(math.e, 0 - (math.pow(value - mean, 2) / (2 * stdev * stdev)))

    return lhs * rhs
"""
