# Written by Jonathan Saewitz, released August 17th, 2016 for Statisti.ca
# Released under the MIT License (https://opensource.org/licenses/MIT)

import csv, plotly.plotly as plotly, plotly.graph_objs as go
from collections import Counter

LEAGUE_SIZE_TO_ANALYZE=10 #the size of the league (number of teams) to analyze (e.g. leagues with 10 teams)

#initialize counters
c=Counter()
number_teams_c=Counter()

with open('ff_draft_picks.csv', 'r') as f:
	reader=csv.reader(f)
	reader.next() #skip the header row
	for row in reader: #loop through every row
		try: #try to get the number of teams in each league
			number_teams=int(row[2]) #row[2] is the number of teams
			number_teams_c[number_teams]+=1 #increment the number of teams in each league counter
		except ValueError:
			continue
		if number_teams==LEAGUE_SIZE_TO_ANALYZE:
			pick=int(row[1]) #row[1] is the pick
			if not pick>number_teams: #only include the pick if it was done in the first round
									  #(i.e., winning team didn't trade first round pick for a higher round)
				c[pick]+=1 #increment the counter for the pick number

#create the graph
trace = go.Bar(
    x = c.keys(),
    y = c.values()
)

layout=go.Layout(
	title="Fantasy Football Wins By Pick #",
	xaxis=dict(
		title="Pick #",
	),
	yaxis=dict(
		title="# Wins",
	)
)

data=[trace]
fig=dict(data=data, layout=layout)
# plotly.plot(fig)

trace = go.Bar(
    x = c.keys(),
    y = c.values()
)

layout=go.Layout(
	title="Fantasy Football Wins By Pick #",
	xaxis=dict(
		title="Pick #",
	),
	yaxis=dict(
		title="# Wins",
	)
)

data=[trace]
fig=dict(data=data, layout=layout)
plotly.plot(fig)

#number of teams in each league:
fig = {
	'data':
			[{'labels': number_teams_c.keys(),
			  'values': number_teams_c.values(),
			  'type': 'pie'}],
	'layout': {'title': "Number of Teams in ESPN Fantasy Football Leagues"}
}

plotly.plot(fig)
