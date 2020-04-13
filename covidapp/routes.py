from covidapp import app
from flask import render_template,jsonify
import pandas as pd
from scripts.wrangle import data_wrangling,return_fig

import plotly.graph_objs as go
import plotly, json



@app.route('/')
@app.route('/index')
def index():
    figs,t_case,states,cases,districtfor = return_fig()
    ids= ['figure-{}'.format(i) for i, _ in enumerate(figs)]
    figureJSON = json.dumps(figs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html',ids=ids, 
            figureJSON = figureJSON,
            all_states = states,
            all_cases = cases,
            t_case = t_case,
            district = districtfor
            )