import pandas as pd
import plotly.express as px


wikiurl_pop = 'https://en.wikipedia.org/wiki/Demographics_of_Metro_Vancouver'
wikiurl_stn = 'https://en.wikipedia.org/wiki/List_of_Vancouver_SkyTrain_stations'
table_class="wikitable"

# get a single table of municipal populations
pops = pd.read_html(wikiurl_pop,
                   match='Metro Vancouver member populations')[0]
pops = pops[['Member', 'Population (2021)']]
pops = pops.rename(columns={'Member': 'Municipality', 'Population (2021)': 'Population'}).set_index('Municipality')


# This wiki page has 3 tables, the second is the current stations, the third is the future stations
stns = pd.read_html(wikiurl_stn)
current_stns = stns[1]
future_stns = stns[2]

# setting up to concatenate them into a long dataframe by adding a status column
current_stns['Status'] = 'Current'
future_stns['Status'] = 'Future'
stns = pd.concat([current_stns[['Municipality', 'Station', 'Status']], future_stns[['Municipality', 'Station', 'Status']]], ignore_index=True)

# fixing an inconsistency
stns.loc[ stns['Municipality'] == 'Richmond / YVR', 'Municipality'] = 'Richmond'

# count the number of stations per municipality
stns = (stns
        .groupby(['Municipality', 'Status'])
        .count()
        .rename(columns={'Station': 'Number of Stations'}))

# build the plot dataframe with an inner join between stations and municipality populations
plot_df = stns.join(pops)
plot_df.Population = plot_df.Population.astype(int)
plot_df['Stations per 100k'] = plot_df['Number of Stations'] / (plot_df['Population'] / 100000)

# take the wide plot_df and make it long - this supports letting plotly facet the plot
plot_long = plot_df.reset_index().melt(id_vars=['Municipality', 'Status', 'Population'], value_vars=['Number of Stations', 'Stations per 100k'])

fig = px.bar(plot_long.reset_index(), y="Municipality", x="value", color="Status", 
             title="Skytrain Stations<br><sup>Absolute number of stations and stations per 100k people</sup>",
             facet_col="variable", orientation='h')
fig.show()
