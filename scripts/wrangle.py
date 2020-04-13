import pandas as pd
import requests
import plotly.graph_objs as go
import plotly.express as px

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
    
    df_india = pd.DataFrame(rows)
    
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


    graph_2 = []
    graph_2.append(go.Pie(
            labels = x_val,
            values = y_val
        ))

    layout_2 = dict(title='Covid19 cases state wise ')





    figs=[]
    figs.append(dict(data=graph_1, layout=layout_1))
    figs.append(dict(data=graph_2, layout=layout_2))            

    return figs,t_case,x_val,y_val,districtfor