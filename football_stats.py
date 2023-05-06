import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

pd.set_option('display.max_colwidth', None)

base_path = './data/'
get_team_stats = pd.read_csv(base_path+"29 April Football Analysis - Team Stats.csv")
print(get_team_stats)

get_overall_stats = pd.read_csv(base_path+"29 April Football Analysis - Overall Stats.csv")
print(get_overall_stats)

game_number_option = st.selectbox(
    'Game #',
    ('1', '2', '3'))

st.write('You selected:', game_number_option)


re_order_cols = []
game_team_stats_filtered = get_team_stats[get_team_stats['Game'] == int(game_number_option)]
game_team_stats_filtered_transposed = game_team_stats_filtered.set_index('Team').T
game_team_stats_filtered_transposed = game_team_stats_filtered_transposed.fillna(0)
game_team_stats_filtered_transposed = game_team_stats_filtered_transposed.astype('int')
game_team_stats_filtered_transposed['Stats'] = game_team_stats_filtered_transposed.index
game_team_stats_filtered_transposed['#'] = np.arange(len(game_team_stats_filtered_transposed))
game_team_stats_filtered_transposed = game_team_stats_filtered_transposed.set_index('#')

for cols in game_team_stats_filtered_transposed.columns:
    re_order_cols.append(cols)
re_order_cols.remove('Stats')
re_order_cols.insert(1,'Stats')

game_team_stats_filtered_transposed = game_team_stats_filtered_transposed[re_order_cols]
st.write(game_team_stats_filtered_transposed)

get_overall_stats_filtered = get_overall_stats[get_overall_stats['Game'] == int(game_number_option)]
get_overall_stats_filtered = get_overall_stats_filtered.fillna(0)
#get_overall_stats_filtered = get_overall_stats_filtered.astype('int')
for (colname,colval) in get_overall_stats_filtered.items():
    #print(colname, get_overall_stats_filtered.dtypes[colname])
    if get_overall_stats_filtered.dtypes[colname] == 'float64':
        get_overall_stats_filtered[colname] = get_overall_stats_filtered[colname].astype(int)


get_overall_stats_filtered_summed = get_overall_stats_filtered.groupby(['Team']).sum()
get_overall_stats_filtered_summed = get_overall_stats_filtered_summed[['Passes','Success Pass','Interception']]
get_overall_stats_filtered_summed['Team'] = get_overall_stats_filtered_summed.index
get_overall_stats_filtered_summed['#'] = np.arange(len(get_overall_stats_filtered_summed))
get_overall_stats_filtered_summed = get_overall_stats_filtered_summed.set_index('#')
#st.write(get_overall_stats_filtered_summed)
cols = st.columns([1, 1])
get_max_passes = get_overall_stats_filtered.nlargest(1,'Passes')['Team Players'].values.tolist()[0]
get_overall_stats_filtered_summed_max_player = get_overall_stats_filtered[get_overall_stats_filtered['Team Players'] == get_max_passes]

get_max_success_passes = get_overall_stats_filtered.nlargest(1,'Success Pass')['Team Players'].values.tolist()[0]
get_overall_stats_filtered_summed_success_max_player = get_overall_stats_filtered[get_overall_stats_filtered['Team Players'] == get_max_success_passes]
get_max_intercept_passes = get_overall_stats_filtered.nlargest(1,'Interception')['Team Players'].values.tolist()[0]
get_overall_stats_filtered_summed_interception_max_player = get_overall_stats_filtered[get_overall_stats_filtered['Team Players'] == get_max_intercept_passes]

st.write(get_overall_stats_filtered_summed_max_player)

with cols[0]:
    st.metric("Player With the Most Pass: "+get_max_passes,str(get_overall_stats_filtered_summed_max_player['Passes'].values.tolist()[0]))
    st.metric("Player With the Most Success Pass: "+get_max_success_passes,str(get_overall_stats_filtered_summed_success_max_player['Success Pass'].values.tolist()[0]))
    st.metric("Player With the Most Interception Pass: "+get_max_intercept_passes,str(get_overall_stats_filtered_summed_interception_max_player['Interception'].values.tolist()[0]))
    


with cols[1]:
    stats_type = st.selectbox('Stats', ['Passes', 'Success Pass', 'Interception'])
    fig = px.pie(get_overall_stats_filtered_summed, values=stats_type, names='Team',
                 title=f'Total % of {stats_type}',
                 height=300, width=400, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Overall Game Stats"):
    st.write(get_overall_stats_filtered)
