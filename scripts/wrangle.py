import pandas as pd
import requests
import plotly.graph_objs as go


def data_wrangling(dataset):
    """Clean world bank data for a visualizaiton dashboard

    Keeps data range of dates in keep_columns variable and data for the top 10 economies
    Reorients the columns into a year, country and value
    Saves the results to a csv file

    Args:
        dataset (str): name of the csv data file

    Returns:
        None

    """
    url = dataset
    r = requests.get(url)
    data = r.json()
    return data

def return_data():

    '''
    Take the data  from  the covid19 india api

    Args:
        none

    Returns:
        The data of the covid19 api feature
    '''
    url = "https://api.covid19india.org/data.json"
    r = requests.get(url)
    alldata = r.json()
    df_state = pd.DataFrame(alldata['statewise'])
    d_tot = [df_state.confirmed.tolist()[0],df_state.active.tolist()[0],df_state.deaths.tolist()[0],df_state.recovered.tolist()[0]]
    stat_confirmed = df_state.confirmed.tolist()[1:]
    stat_active = df_state.active.tolist()[1:]
    stat_deaths = df_state.deaths.tolist()[1:]
    stat_recover = df_state.recovered.tolist()[1:]
    stat_state = df_state.state.tolist()[1:]
    return d_tot,stat_confirmed,stat_active,stat_deaths,stat_recover,stat_state

def map_fig():
    '''
    Funtion return the fig of the place effected in map

    arguments: 
          none
    return:
        map figure object
    '''

    world = data_wrangling('https://bing.com/covid/data')
    world = pd.DataFrame(world)
    world_tot = [world.totalConfirmed.tolist()[0],world.totalDeaths.tolist()[0],world.totalRecovered.tolist()[0]]
    data_country = pd.DataFrame(world['areas'].tolist())
    just=[]
    l=[]
    for i in range(len(data_country['areas'])):
        for d in range(len(data_country['areas'][i])):
            if len(data_country['areas'][i][d]['areas']) == 0:
                just.append(data_country['areas'][i][d])
            for j in data_country['areas'][i][d]['areas']:
                l.append(j)
    data_left =  pd.DataFrame(just)
    data_state = pd.DataFrame(l)
    data_state= data_state.append(data_left)
    graph_map=[]
    graph_map.append(go.Scattermapbox(
        lat=data_state['lat'],
        lon=data_state['long'],
        mode='markers',
        
        marker=go.scattermapbox.Marker(
            size=8
        ),
    text = "Place: "+data_state.displayName.map(str)+"<br>"+"TotalCase: "+data_state.totalConfirmed.map(str)+"<br>"+"TotalRecovered: " +data_state.totalRecovered.map(str)+"<br>"+"TotalDeaths: "+data_state.totalDeaths.map(str),
    ))

    layout_map=dict(hovermode='closest',
   
    mapbox=dict(
        autosize=False,
    width=500,
    height=1000,
        accesstoken='pk.eyJ1Ijoibm90aWtlODc3IiwiYSI6ImNrNWFxcmZmczEyeTgzbHAzYnRicmhxeWEifQ.xRoAbQ4k6NQ35Dw2AGaeBA',
        bearing=0,
        style='outdoors',
        pitch=0,
        zoom=5,
    ))
    
    map_fig=[]
    map_fig.append(dict(data=graph_map, layout=layout_map))
    return map_fig,world_tot

def return_fig():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations
        list (list): for the no. of cases in the states

    """
    graph_1= []

    data=data_wrangling("https://api.covid19india.org/state_district_wise.json")
    state_list = [i for i in data]
    rows=[]
    for state in state_list:
        district = list(data[state]['districtData'].keys())
        case_d = list(data[state]['districtData'].values())
        for district,case_d in zip(district,case_d):
            row={}
            row['district'] = district
            row['state'] = state
            row['cases'] = case_d['confirmed']  
            rows.append(row)
    
    df_india = pd.DataFrame(rows).sort_values(by=['cases'],ascending=False)
    
    t_case = df_india['cases'].sum()
    districtfor = [[d,s,c] for d,s,c in zip(df_india['district'],df_india['state'],df_india['cases'])]
    state_wise_case = df_india.groupby('state')['cases'].sum().sort_values(ascending=False)
    state_wise_case = state_wise_case.to_frame().reset_index()
    x_val = state_wise_case.state.tolist()
    y_val = state_wise_case.cases.tolist()
    graph_1.append(go.Bar(
            x = x_val,
            y = y_val
        ))

    layout_1 = dict(title='Covid19 cases state wise ',
    xaxis = dict(title='State',),
    yaxis = dict(title='Population'),
    )


    graph_2 =[]
    graph_2.append(go.Pie(
            labels = x_val,
            values = y_val
        ))

    layout_2 = dict(title='Covid19 cases state wise ')


    data_all = data_wrangling('https://api.covid19india.org/data.json')
    df_cases = pd.DataFrame(data_all['cases_time_series'])
    graph_3 = []
    graph_3.append(go.Scatter(
        x=df_cases['date'], 
        y=df_cases['totalconfirmed'],
        mode = 'lines'
        ))
    layout_3 = dict(title= 'Total cases',
               xaxis = dict(title='date/month',),
               yaxis = dict(title='No. of cases'),
               )

    figs=[]
    figs.append(dict(data=graph_1, layout=layout_1))
    figs.append(dict(data=graph_2, layout=layout_2))            
    figs.append(dict(data=graph_3, layout=layout_3))

    return figs,t_case,x_val,y_val,districtfor