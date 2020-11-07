import pandas as pd
import os
import arrow
import requests
import functools
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from flask import Flask, json
from dash import Dash
from dash.dependencies import Input, Output, State
import random
import dash_table
import dash
import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from flask import send_file
import io
import flask
import pandas as pd
import difflib
import xlrd
import numpy as np
from flask import send_file
from main import runMain
import dash_bootstrap_components as dbc
app_name = 'Cloud Selection'
server = Flask(app_name)



def create_header(some_string):
    header_style = {
        'backgroundColor':  '#333',
        'padding': '1.5rem',
        'color':'#fff'
    }
    header = html.Header(html.H1(children=some_string, style=header_style))
    return header


external_js = [
    # jQuery, DataTables, script to initialize DataTables
    'https://code.jquery.com/jquery-3.2.1.slim.min.js',
    'https://cdn.datatables.net/1.10.15/js/jquery.dataTables.min.js',
    'https://codepen.io/jackdbd/pen/bROVgV.js',
]

external_css = [
    # dash stylesheet
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css?family=Raleway',
    # 'https://fonts.googleapis.com/css?family=Lobster',
    'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://cdn.datatables.net/1.10.15/css/jquery.dataTables.min.css',
]


app = dash.Dash(__name__,    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
                external_scripts=external_js,
                external_stylesheets=external_css)

#app.scripts.config.serve_locally = True
#app.css.config.serve_locally = True
app.title = 'CustomCloud'
app.config['suppress_callback_exceptions'] = True

for js in external_js:
    app.scripts.append_script({'external_url': js})

for css in external_css:
    app.css.append_css({'external_url': css})



app.layout = html.Div([
    create_header("CustomCloud"), 

    html.Div(
     
  
                children=[
            html.H6("Step 1: Download the file and fill your preferences"),
             html.A(html.Button('Download Excel'),
    href='/download_excel/'),

            html.H6("Step 2: Upload the input file to check the best Cloud Service provider based on your preferance.") , 
                   
 ], className="ten columns offset-by-two"
    ),
    
    html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),],className="eight columns offset-by-two"),
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            x,node,performance=runMain(df)
            df=pd.DataFrame(x)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5("Best Node is "+str(node)),
        html.H6("Performance: "+str(performance)),

        dash_table.DataTable(
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    },
    style_cell_conditional=[
        {
            'textAlign': 'center'
        } for c in ['Node', 'Results']
    ],

            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        # horizontal line

        # For debugging, display the raw contents provided by the web browser
        
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.server.route('/download_excel/')
def download_excel():
    #Create DF
    #d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.read_excel('sample_input.xlsx')

    #Convert DF
    strIO = io.BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
    df.to_excel(excel_writer, sheet_name="sheet1")
    excel_writer.save()
    excel_data = strIO.getvalue()
    strIO.seek(0)

    return send_file(strIO,
                     attachment_filename='Sample.xlsx',
                     as_attachment=True)

if __name__ == '__main__':
    app.run_server(debug=True)

