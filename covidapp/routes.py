from covidapp import app
from flask import render_template,jsonify
import pandas as pd
from scripts.wrangle import data_wrangling,return_fig,return_data

import plotly.graph_objs as go
import plotly, json



@app.route('/')
@app.route('/index')
def index():
    figs,t_case,states,cases,districtfor = return_fig()
    d_tot,stat_confirmed,stat_active,stat_deaths,stat_recover,stat_state = return_data()
    fat = round(int(d_tot[2])/int(d_tot[0])*100,2)
    return render_template('index.html', 
            tot = d_tot,
            all_states = stat_state,
            all_cases = stat_confirmed,
            all_recover = stat_recover,
            all_active= stat_active,
            all_death = stat_deaths,
            district = districtfor ,
            fat = fat
            )

@app.route('/visual')
def visual():
    figs,t_case,states,cases,districtfor = return_fig()
    d_tot,stat_confirmed,stat_active,stat_deaths,stat_recover,stat_state = return_data()
    fat = round(int(d_tot[2])/int(d_tot[0])*100,2)
    ids= ['figure-{}'.format(i) for i, _ in enumerate(figs)]
    figureJSON = json.dumps(figs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('visual.html',ids=ids, 
            figureJSON = figureJSON,
            t_case = t_case,
            tot = d_tot,
            fat = fat
            )

@app.route('/worldmap')
def worldmap():
    # figs,world_tot = map_fig()
    # fat = round((world_tot[1]/world_tot[0])*100,2)
    # ids= ['figure-{}'.format(i) for i, _ in enumerate(figs)]
    # figureJSON = json.dumps(figs, cls=plotly.utils.PlotlyJSONEncoder)
    # return render_template('map.html',ids=ids, 
    #         figureJSON = figureJSON,
    #         world_tot = world_tot,
    #         fat = fat
    #         )
    return render_template('devlop.html')