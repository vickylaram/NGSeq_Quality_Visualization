import plotly.express as px
import plotly.graph_objects as go


def basic_statistics(data):
    """Plots the basic statistics module as a table

    :param data: data from FastQC 'Basic Statistics' result module as a Pandas DataFrame
    :return: Plotly Graph Objects/Table figure filled with data provided in params
    """
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


def boxplot(data):
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

    return fig


def tile(data):
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

    return fig


def line(data, selection_id):
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

    # ...but certain modules have more than two columns, meaning the selection_id needs to be checked
    # ID = 4: Per base sequence content
    if selection_id == 4:
        fig = px.line(data, x=data.iloc[:, 0],
                      y=[data.iloc[:, 1], data.iloc[:, 2], data.iloc[:, 3], data.iloc[:, 4]],
                      labels=dict(x=data.columns[0], y=data.columns[1]))

    # ID = 8: Sequence Duplication Levels
    if selection_id == 8:
        fig = px.line(data, x=data.iloc[:, 0],
                      y=[data.iloc[:, 1], data.iloc[:, 2]],
                      labels=dict(x=data.columns[0], y=data.columns[1]))

    # ID = 9: Adapter Content
    if selection_id == 9:
        fig = px.line(data, x=data.iloc[:, 0],
                      y=[data.iloc[:, 1], data.iloc[:, 2], data.iloc[:, 3], data.iloc[:, 4],
                         data.iloc[:, 5]],
                      labels=dict(x=data.columns[0], y=data.columns[1]))

    return fig
