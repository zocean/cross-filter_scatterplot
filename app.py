#!/home/yangz6/Software/anaconda3/bin/python
# Programmer : Yang Zhang 
# Contact: zocean636@gmail.com
# Last-modified: 27 Oct 2020 10:08:29 AM

import base64
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px

from dash_extensions import Download
from dash_extensions.snippets import send_data_frame


# init dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# load data
df = pd.read_csv("data_large.tsv", sep = '\t', header = 0)

# get possible column name
column_list = [item for item in df.columns.to_list() if item not in ['chrom', 'start', 'stop', 'size', 'mid']]

# layout
app.layout = html.Div([
    # title
    html.H2("Cross-filter scatterplot tool", style = {'textAlign': 'center'}),
    # description
    html.Div([
        html.Strong("Instruction:"), 
        html.P("There are three scatter plots. You can first choose the data you want to use for X-axis and Y-axis in each plot using the dropdown tool. Then you can choose whether to use the raw signal value or the percentiles of values. To interactively explore the plots, you can try clicking and dragging in any of the plots to filter different regions. Notably, only the intersection of the selections from three plots will be highlighted with a different color. For example, you can select a region on the first plot. The selected points will be highlighted in all three plots. Then, you can further select a subset of points in the second and third plots. To remove a selection for a plot, you can double click at any position in that plot or draw a selection without any points. Finally, you can download the highlighted regions are a bed file by clicking the DOWNLOAD button. A dialog will pop up showing you how many regions are exported."),
        html.P("To use your data, you should firstly prepare a TSV file (i.e., columns are separated by tabs). The first row is the column name. We recommend you to prepare data in bed format with the first three columns as chromosome, start position, and end position. The rest columns can be functional readouts. 'NA' values may cause some problems, so please remove any rows with 'NA' values. Once you upload a new file, the dropdown tool should automatically update to list the available columns that you can choose.")
    ], style = {'textAlign': 'justify', 'marginTop': '15px', 'marginBottom': '30px', 'marginLeft': '20px', 'marginRight': '20px'}),
    # upload data
    html.Div([
        html.H4("Upload TSV file"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '30%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': 'auto'
            },
            # Allow multiple files to be uploaded
            multiple = False
        ),
        html.Div(id='dataframe', style={'display': 'none'})
        #html.Div(id='dataframe')
    ], style = {'width': '97%', 'margin': 'auto', 'boxShadow': '2px 2px 2px lightgrey', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'}),
    # global config
    html.Div([
        html.H4("Global config"),
        html.Label([
            'Figure height',
            dcc.Slider(
                id='height-slider',
                min=450,
                max=800,
                step=50,
                value=600,
                marks={
                    450: '450px',
                    500: '500px',
                    550: '550px',
                    600: '600px',
                    650: '650px',
                    700: '700px',
                    750: '750px',
                    800: '800px'
                }
            )
        ], style = {'width':'40%'})
    ], style = {'width': '97%', 'margin': 'auto', 'boxShadow': '2px 2px 2px lightgrey', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'}),
    # plot config 
    html.Div([
        # first dropdown
        html.Div([
            html.H4("Plot 1 config"),
            html.Label([
                'Select X-axis', 
                #dcc.Dropdown(
                #    id = 'dropdown-first-xaxis-column',
                #    options = [{'label': col, 'value': col} for col in column_list],
                #    value = column_list[0]
                #)
                dcc.Dropdown(
                    id = 'dropdown-first-xaxis-column'
                )
            ], style = {'marginTop': '5px', 'marginBottom': '5px', 'marginLeft': '10px', 'marginRight': '10px'}),
            html.Label([
                'Select Y-axis',
                dcc.Dropdown(
                    id = 'dropdown-first-yaxis-column'
                )
            ], style = {'marginTop': '5px', 'marginBottom': '5px', 'marginLeft': '10px', 'marginRight': '10px'}),
            html.Label([
                'Data transformation',
                dcc.RadioItems(
                    id = 'radio-first',
                    options = [{'label': i, 'value': i} for i in ['raw', 'percentile']],
                    value = 'raw',
                    labelStyle = {'dispaly': 'inline-block'}
                )
            ]),
        ],
        style = {'width': '32%', 'marginTop': '10px', 'marginBottom': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'boxShadow': '2px 2px 2px lightgrey', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'}),
        # second dropdown
        html.Div([
            html.H4("Plot 2 config"),
            html.Label([
                'Select X-axis', 
                dcc.Dropdown(
                    id = 'dropdown-second-xaxis-column'
                )
            ], style = {'marginTop': '5px', 'marginBottom': '5px', 'marginLeft': '10px', 'marginRight': '10px'}),
            html.Label([
                'Select Y-axis',
                dcc.Dropdown(
                    id = 'dropdown-second-yaxis-column'
                )
            ], style = {'marginTop': '5px', 'marginBottom': '5px', 'marginLeft': '10px', 'marginRight': '10px'}),
            html.Label([
                'Data transformation',
                dcc.RadioItems(
                    id = 'radio-second',
                    options = [{'label': i, 'value': i} for i in ['raw', 'percentile']],
                    value = 'raw',
                    labelStyle = {'dispaly': 'inline-block'}
                )
            ]),
        ],
        style = {'width': '32%', 'marginTop': '10px', 'marginBottom': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'boxShadow': '2px 2px 2px lightgrey', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'}),
        # third dropdown
        html.Div([
            html.H4("Plot 3 config"),
            html.Label([
                'Select X-axis', 
                dcc.Dropdown(
                    id = 'dropdown-third-xaxis-column'
                )
            ], style = {'marginTop': '5px', 'marginBottom': '5px', 'marginLeft': '10px', 'marginRight': '10px'}),
            html.Label([
                'Select Y-axis',
                dcc.Dropdown(
                    id = 'dropdown-third-yaxis-column'
                )
            ], style = {'marginTop': '5px', 'marginBottom': '5px', 'marginLeft': '10px', 'marginRight': '10px'}),
            html.Label([
                'Data transformation',
                dcc.RadioItems(
                    id = 'radio-third',
                    options = [{'label': i, 'value': i} for i in ['raw', 'percentile']],
                    value = 'raw',
                    labelStyle = {'dispaly': 'inline-block'}
                )
            ]),
        ],
        style = {'width': '32%', 'marginTop': '10px', 'marginBottom': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'boxShadow': '2px 2px 2px lightgrey', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'})
    ], style = {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center', 'margin': 'auto'}),
    html.Div([
        # first scatter plot
        html.Div([
            html.Label("Plot 1", style = {'textAlign': 'center'}),
            dcc.Graph(id = 'plot_1',  config = {'displayModeBar': True,
            'modeBarButtonsToRemove': ['select2d']})
        ], className = 'scatter_plot', style = {'width': '32%', 'marginTop': '10px', 'marginBottom': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'boxShadow': '2px 2px 2px lightgrey', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'}),
        # second scatter plot
        html.Div([
            html.Label("Plot 2", style = {'textAlign': 'center'}),
            dcc.Graph(id = 'plot_2',  config = {'displayModeBar': True,
            'modeBarButtonsToRemove': ['select2d']})
        ], className = 'scatter_plot', style = {'width': '32%', 'marginTop': '10px', 'marginBottom': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'boxShadow': '2px 2px 2px lightgrey', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'}),
        # third scatter plot
        html.Div([
            html.Label("Plot 3", style = {'textAlign': 'center'}),
            dcc.Graph(id = 'plot_3',  config = {'displayModeBar': True,
            'modeBarButtonsToRemove': ['select2d']})
        ], className = 'scatter_plot', style = {'width': '32%', 'marginTop': '10px', 'marginBottom': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'boxShadow': '2px 2px 2px lightgrey', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'}),
    ], style = {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center',  'margin': 'auto'}),
    # download button
    html.Div([
        html.Button('Download highlighted regions', id = 'download_button', className = 'button-primary', style = {'marginTop': '50px', 'marginBottom': '50px'}),
        Download(id = 'download'),
        html.Div(id = 'download-msg')]
    , style = {'margin': 'auto', 'width': '220px', 'textAlign': 'center'}),
], className = 'row', style = {'backgroundColor': '#f2f2f2', 'marginLeft': '60px', 'marginRight': '60px'})


def get_figure(df, x_col, y_col, selected_points, data_format, figure_height):
    '''
    plot scatterplot given columns and highlighted point
    '''
    # plot 
    if data_format == 'raw':
        fig = px.scatter(df, x=df[x_col], y=df[y_col], text=df.index)
    else:
        fig = px.scatter(df, x=df[x_col].rank(pct = True), y=df[y_col].rank(pct = True), text=df.index)
    # highlight points
    fig.update_traces(selectedpoints = selected_points,
                      customdata = df.index,
                      mode='markers', 
                      marker={ 'color': 'rgba(252,141,89, 0.3)', 'size': 7}, 
                      unselected={'marker': { 'color': 'rgba(44, 123, 182, 0.1)'}})
    # layout
    if figure_height is None:
        figure_height = 600
    if data_format == 'raw':
        fig.update_layout(margin={'l': 20, 'r': 0, 'b': 15, 't': 5}, dragmode='lasso', hovermode=False, xaxis_title = x_col.replace('_', ' '), yaxis_title = y_col.replace('_', ' '), height = figure_height)
    else:
        fig.update_layout(margin={'l': 20, 'r': 0, 'b': 15, 't': 5}, dragmode='lasso', hovermode=False, xaxis_title = x_col.replace('_', ' ')+' %', yaxis_title = y_col.replace('_', ' ')+' %', height = figure_height)
    return fig

def parse_content(file_content, filename, last_modified):
    #
    content_type, content_string = file_content.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Assume that the user uploaded a TSV file
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep = '\t', header = 0)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    # succeed return a dataframe
    #return html.Div(dash_table.DataTable(data=df.to_dict('records'), id='table'))
    return df.to_json(date_format='iso', orient='split')

#####################
# callback funtions
#####################

# update dropdown options
@app.callback(
    [
        Output('dropdown-first-xaxis-column', 'options'),
        Output('dropdown-first-yaxis-column', 'options'),
        Output('dropdown-second-xaxis-column', 'options'),
        Output('dropdown-second-yaxis-column', 'options'),
        Output('dropdown-third-xaxis-column', 'options'),
        Output('dropdown-third-yaxis-column', 'options')
    ], 
    Input('dataframe', 'children')
)
def set_xaxis_options(data_json):
    if data_json is not None:
        data = pd.read_json(data_json, orient='split')
    else:
        data = df
    column_list = [item for item in data.columns.to_list() if item not in ['chrom', 'start', 'stop', 'size', 'mid']]
    option_list = [{'label': i, 'value': i} for i in column_list]
    return [option_list, option_list, option_list, option_list, option_list, option_list]

# update first xaxis value
@app.callback(
    Output('dropdown-first-xaxis-column', 'value'),
    Input('dropdown-first-xaxis-column', 'options')
)
def set_first_xaxis_value(available_options):
    return available_options[0]['value']

# update first yaxis value
@app.callback(
    Output('dropdown-first-yaxis-column', 'value'),
    Input('dropdown-first-yaxis-column', 'options')
)
def set_first_yaxis_value(available_options):
    return available_options[1]['value']

# update second xaxis value
@app.callback(
    Output('dropdown-second-xaxis-column', 'value'),
    Input('dropdown-second-xaxis-column', 'options')
)
def set_second_xaxis_value(available_options):
    return available_options[2]['value']

# update second yaxis value
@app.callback(
    Output('dropdown-second-yaxis-column', 'value'),
    Input('dropdown-second-yaxis-column', 'options')
)
def set_second_yaxis_value(available_options):
    return available_options[3]['value']

# update third xaxis value
@app.callback(
    Output('dropdown-third-xaxis-column', 'value'),
    Input('dropdown-third-xaxis-column', 'options')
)
def set_third_xaxis_value(available_options):
    return available_options[2]['value']

# update third yaxis value
@app.callback(
    Output('dropdown-third-yaxis-column', 'value'),
    Input('dropdown-third-yaxis-column', 'options')
)
def set_third_yaxis_value(available_options):
    return available_options[3]['value']

# update data
@app.callback(
    Output('dataframe', 'children'),
    [
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified')
    ]
)
def upload_data(file_content, filename, last_modified):
    if file_content is not None:
        return parse_content(file_content, filename, last_modified)

# update figure 
@app.callback(
    [
        Output('plot_1', 'figure'),
        Output('plot_2', 'figure'),
        Output('plot_3', 'figure')
    ],
    [   
        Input('dataframe', 'children'),
        Input('plot_1', 'selectedData'),
        Input('plot_2', 'selectedData'),
        Input('plot_3', 'selectedData'),
        Input('dropdown-first-xaxis-column', 'value'),
        Input('dropdown-first-yaxis-column', 'value'),
        Input('dropdown-second-xaxis-column', 'value'),
        Input('dropdown-second-yaxis-column', 'value'),
        Input('dropdown-third-xaxis-column', 'value'),
        Input('dropdown-third-yaxis-column', 'value'),
        Input('radio-first', 'value'),
        Input('radio-second', 'value'),
        Input('radio-third', 'value'),
        Input('height-slider', 'value')
    ]
)
def update_fig(data_json, selection1, selection2, selection3, x_col_1, y_col_1, x_col_2, y_col_2, x_col_3, y_col_3, data_format_1, data_format_2, data_format_3, figure_height):
    if data_json is not None:
        data = pd.read_json(data_json, orient='split')
    else:
        data = df
    selected_points = df.index
    for selected_data in [selection1, selection2, selection3]:
        if selected_data and selected_data['points']:
            selected_points = np.intersect1d(selected_points,
                [p['customdata'] for p in selected_data['points']])
    return [get_figure(data, x_col_1, y_col_1, selected_points, data_format_1, figure_height),
            get_figure(data, x_col_2, y_col_2, selected_points, data_format_2, figure_height),
            get_figure(data, x_col_3, y_col_3, selected_points, data_format_3, figure_height)]

@app.callback(
    [
        Output("download", "data"),
        Output('download-msg', "children")
    ], 
    [
        Input("download_button", "n_clicks"),
        State('plot_1', 'selectedData'),
        State('plot_2', 'selectedData'),
        State('plot_3', 'selectedData')
    ]
)
def download_func(n_nlicks, selection1, selection2, selection3):
    triggered_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'download_button' in triggered_id:
        selected_points = df.index
        for selected_data in [selection1, selection2, selection3]:
            if selected_data and selected_data['points']:
                selected_points = np.intersect1d(selected_points,
                    [p['customdata'] for p in selected_data['points']])
        df_selected = df.iloc[selected_points]
        return [
            send_data_frame(df_selected[['chrom', 'start', 'stop']].to_csv, "highlighed_region.bed", sep = '\t', header = False, index = False),
            dcc.ConfirmDialog(id = 'download-msg', message = "Export %d regions" % (len(selected_points)), displayed = True)
        ]
    else:
        return [None, None]


if __name__ == '__main__':
    app.run_server(host='genome-dev.compbio.cs.cmu.edu', debug=True)
