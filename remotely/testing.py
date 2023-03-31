import dash
import dash_table
import pandas as pd

# Create a DataFrame with nested data
data = {
    'id': [1, 2],
    'name': ['Alice', 'Bob'],
    'details': [
        {'age': 25, 'location': 'New York'},
        {'age': 30, 'location': 'London'}
    ]
}
df = pd.DataFrame(data)

# Define the columns for the data_table
columns = [
    {'name': 'ID', 'id': 'id'},
    {'name': 'Name', 'id': 'name'},
    {
        'name': 'Details',
        'id': 'details',
        'type': 'text',
        'presentation': 'markdown',
        'format': lambda value: (
            dash_table.DataTable(
                columns=[
                    {'name': 'Age', 'id': 'age'},
                    {'name': 'Location', 'id': 'location'}
                ],
                data=[value],
                style_cell={
                    'textAlign': 'left',
                    'paddingLeft': '30px'
                },
                style_table={
                    'width': '100%',
                    'margin': '0px'
                },
                style_data={
                    'border': 'none'
                },
                merge_duplicate_headers=True
            ).to_string(index=False)
        )
    }
]

# Create the Dash app and layout
app = dash.Dash(__name__)
app.layout = dash_table.DataTable(
    columns=columns,
    data=df.to_dict('records'),
    style_cell={
        'textAlign': 'center',
        'padding': '10px',
        'whiteSpace': 'normal',
        'height': 'auto',
        'minWidth': '180px'
    },
    style_header={
        'fontWeight': 'bold'
    },
    style_table={
        'width': '100%',
        'borderCollapse': 'collapse',
        'margin': '0px'
    },
    merge_duplicate_headers=True
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)