import plotly.express as px
import plotly.graph_objects as go


def basic_statistics(data):
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
    fig = px.line(data, x=data.iloc[:, 0], y=data.iloc[:, 1],
                  labels=dict(x=data.columns[0], y=data.columns[1]))

    if selection_id == 4:
        fig = px.line(data, x=data.iloc[:, 0],
                      y=[data.iloc[:, 1], data.iloc[:, 2], data.iloc[:, 3], data.iloc[:, 4]],
                      labels=dict(x=data.columns[0], y=data.columns[1]))

    if selection_id == 8:
        fig = px.line(data, x=data.iloc[:, 0],
                      y=[data.iloc[:, 1], data.iloc[:, 2]],
                      labels=dict(x=data.columns[0], y=data.columns[1]))
    if selection_id == 9:
        fig = px.line(data, x=data.iloc[:, 0],
                      y=[data.iloc[:, 1], data.iloc[:, 2], data.iloc[:, 3], data.iloc[:, 4],
                         data.iloc[:, 5]],
                      labels=dict(x=data.columns[0], y=data.columns[1]))

    return fig
