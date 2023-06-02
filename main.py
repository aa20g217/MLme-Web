#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 17:17:42 2021

@author: akshay
"""

from dash import dcc,html
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import dash_table

from app import app
from UI.layouts import preprocessing_content,modelEval_content
from UI.scaling import scalingAlgo
from UI.classifcationAlgo import classAlgo_content
from UI.submit import submit_con
from UI.result import uploadResult_content
from UI.uploadInput import upload_data_content
from UI.autoML import autoML_content


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    
navigation_bar = dbc.Navbar(
    dbc.Container(        [            
            dbc.Col(dbc.NavbarBrand(html.Img(src="assets/logo.png", height="50px")),width=2),

            #dbc.Col(dbc.NavbarBrand(html.I("TOOL NAME"), style={"margin-left": "0px","font-weight": "bold","font-size": "40px","color":"white"}),width=1,align="left"),
            dbc.Col(width=9),
            html.A(dbc.Col(html.Img(src="https://www.unibe.ch/media/logo-unibern-footer@2x.png", height="80px"),align="right"),
                href="https://www.unibe.ch/index_ger.html", target="_blank",
                style={"textDecoration": "none"})

        ],fluid=True,
    ),
   color="#444", 
   dark=True,style={"border-color": "white"}
)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
about=dbc.Card([html.Div([
    dbc.Row(html.H5("MLme",style={"font-weight": "bold","color":"white"})),
    dbc.Row(html.P("Machine learning (ML) has emerged as a vital asset for researchers in analyzing and extracting valuable information from complex datasets. However, developing an effective and robust ML pipeline can present a formidable challenge, demanding considerable time and effort, thereby impeding research progress. Present tools in this landscape requires a profound understanding of ML principles and programming skills. Furthermore, users are required to engage in the comprehensive configuration of their ML pipeline to attain optimal performance.",style={"text-align": "justify"})),
    html.Br(),
    dbc.Row(html.P("To address these challenges, we have developed a novel tool called Machine Learning Made Easy (MLme) that streamlines the use of ML in research, specifically focusing on classification problems at present. By integrating four essential functionalities, namely data exploration, AutoML, CustomML, and visualization, MLme fulfills the diverse requirements of researchers while eliminating the need for extensive coding efforts. To demonstrate the applicability of MLme, we conducted rigorous testing on five distinct datasets, each presenting unique characteristics and challenges. Our results consistently showed promising performance across different datasets, reaffirming the versatility and effectiveness of the tool.",style={"text-align": "justify"})),
    html.Br(),
    dbc.Row(html.H5("Availability",style={"font-weight": "bold","color":"white"})),
    html.Div(["MLme is developed by the ",
             html.A("Functional Urology group", href="http://www.urofun.ch/", target="_blank"),
             " at the ",
             html.A("University of Bern", href="https://www.unibe.ch/index_ger.html", target="_blank"),
             ". The source code and tutorial can be found on the ",
             html.A("MLme GitHub repository.", href="https://github.com/FunctionalUrology/MLme", target="_blank"),
    ],style={"text-align": "justify"}),
    
    html.Br(),
    dbc.Row(html.H5("Contact",style={"font-weight": "bold","color":"white"})),
    html.P("Bug reports and new feature requests can be communicated via:"),
    html.Ul([html.Li(html.Div(["GitHub : ",html.A("https://github.com/FunctionalUrology/MLme/issues", href="https://github.com/FunctionalUrology/MLme/issues", target="_blank")]),)]),
    html.Ul([html.Li("Email : akshay.akshay@unibe.ch , ali.hashemi@unibe.ch")]),
    html.Br(),
    dbc.Row(html.H5("Citation",style={"font-weight": "bold","color":"white"})),
    html.Div(["If MLme helps you in any way, please cite the MLme article."]),
    #html.Ul([html.Li(html.A("", href="", target="_blank"))]),

    ],style={"margin-left": "50px","margin-right": "50px","margin-top": "30px","font-size": "14px"})],
    style={"margin-left": "2px","margin-right": "2px","margin-top": "5px"})



app.css.config.serve_locally = False

 
tabs = dbc.Card(
    [
     dbc.CardHeader(
        dbc.Tabs(
            [
                #dbc.Tab(label="Data Exploration", tab_id="upload_data"),
                dbc.Tab(label="Preprocessing", tab_id="preprocessing"),
                dbc.Tab(label="Classification Algorithms", tab_id="classAlgo"),
                dbc.Tab(label="Model Evaluation ", tab_id="modelEval"),
                dbc.Tab(label="Submit", tab_id="submit"),
                
            ],
            id="tabs",
            active_tab="preprocessing",
            card=True,
        )),
        dbc.CardBody(html.P(id="content", className="mt-3")),
    ],className="mt-3",color="grey", outline=False)


tabs_main = dbc.Card(
    [
     dbc.CardHeader(
        dbc.Tabs(
            [
                dbc.Tab(label="Data Exploration", tab_id="upload_data"),
                dbc.Tab(label="Auto ML", tab_id="autoML"),
                dbc.Tab(label="Custom ML", tab_id="customML"),
                dbc.Tab(label="Visualisation", tab_id="result"),
                dbc.Tab(label="About", tab_id="about")

            ],
            id="tabs_main",
            active_tab="upload_data",
            card=True,
        )),
        dbc.CardBody(html.P(id="content_main", className="mt-3")),
               html.Div(["This webpage is generated by ",
                  html.A("MLme.", href="https://github.com/FunctionalUrology/MLme", target="_blank")],
                 style={"margin-left": "10px","font-size": "11px"}),
    ],className="mt-3",color="grey", outline=False)




a=html.Div([
    dcc.ConfirmDialog(
        id='confirm-danger',
        message="The AutoML functionality on this demonstration server is not available for use with external datasets due to limited computational resources. Please use the provided example input data (https://github.com/aa20g217/MLme-Web/blob/main/example-input-data/data-tab-sep.txt). To fully utilize the AutoML functionality, we recommend running MLme on your local machine or server. Thank you for your understanding.",
    ),
    html.Div(id='output-danger')
])

        


app.layout = html.Div([navigation_bar,
    dcc.Store(id='scaling_tab_data',data={}),
    dcc.Store(id='overSamp_tab_para',data={}),
    dcc.Store(id='underSamp_tab_para',data={}),
    dcc.Store(id='featSel_tab_para',data={}),
    dcc.Store(id='classification_tab_para',data={}),
    dcc.Store(id='modelEval_tab_para',data={}),
    dcc.Store(id='modelEval_metrices_tab_para',data={}),
    dcc.Store(id='refit_Metric',data={}), 
    dcc.Store(id='indepTestSet',data={}),
    tabs_main
    ]) 

#def getActiveAlgo(algoList):
@app.callback(
     Output("btn", "children"),
    Input("MaxAbs Scaler-collapse-button", "n_clicks")
)
def toggle_collapse(n): 
    return n

@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):

    if at == "preprocessing":
        return preprocessing_content 
    elif at == "classAlgo":
        return classAlgo_content
    elif at == "modelEval":
        return modelEval_content
    elif at == "submit":
        return submit_con
    return html.P("This shouldn't ever be displayed...")

@app.callback(Output("content_main", "children"), [Input("tabs_main", "active_tab")])
def switch_tab(at):
    if at == "upload_data":
        return upload_data_content
    elif at == "autoML":
        return autoML_content 
    elif at == "customML":
        return tabs 
    elif at == "result":
        return uploadResult_content 
    
    elif at == "about":
        return about 
    return html.P("This shouldn't ever be displayed...")

# show dialogue box
# =============================================================================
# @app.callback(Output('confirm-danger', 'displayed'), [Input("tabs_main", "active_tab")])
# def switch_tab(at):
#     if at == "autoML":
#         return True 
#     return False
# =============================================================================




import webbrowser as web
web.open_new('http://127.0.0.1:8050/')

if __name__ == '__main__':
    app.run_server(host='127.0.0.1',debug=False,dev_tools_hot_reload=False)    


server = app.server

