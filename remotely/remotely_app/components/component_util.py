from dash import dash_table


def create_table(id):
    table = dash_table.DataTable(
        id=id,
        columns=None,
        data=None,
        row_selectable='single',
        editable=True,
        css=[
            {
                'selector': '.dash-spreadsheet td div',
                'rule': '''
                        line-height: 20px;
                        max-height: 40px; min-height: 40px; height: 40px;
                        display: block;
                        overflow-y: hidden;
                    '''
            }
        ],
        style_table={"maxWidth": "800px", "margin": "0 auto"},
        style_cell={
            "textAlign": "center",
            "fontFamily": "Helvetica",
            "padding": "10px",
            "fontSize": "14px",
            "backgroundColor": "#f2f2f2",
            "border": "none",
        },
        style_cell_conditional=[
            {"if": {"column_id": "name"}, "width": "33.33%"},
            {"if": {"column_id": "age"}, "width": "33.33%"},
            {"if": {"column_id": "country"}, "width": "33.33%"},
        ],
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "white"},
            {
                'if': {'state': 'selected'},
                'backgroundColor': 'rgba(0, 116, 217, 0.3)'
            }
        ],
        style_header={
            "backgroundColor": "#4285f4",
            "color": "white",
            "fontWeight": "bold",
            "border": "none",
        },
    )
    return table
