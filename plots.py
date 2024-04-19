import plotly.graph_objs as go

def create_heatmap(correlation_matrix):
    # Convert correlation matrix to a list of lists
    correlation_values = correlation_matrix.values.tolist()

    # Create x and y labels
    column_names = correlation_matrix.columns.tolist()

    # Create the heatmap
    heatmap = go.Heatmap(z=correlation_values, x=column_names, y=column_names,
                         colorscale='rdbu_r', zmid=0, colorbar=dict(title="Correlation"))

    # Create layout
    layout = go.Layout(title='Correlation Matrix')

    # Create figure
    fig = go.Figure(data=[heatmap], layout=layout)

    return fig
