import pandas as pd
from random import randint
import bokeh.plotting as bp
from bokeh.models import HoverTool, Legend
from bokeh.layouts import column

plots = []

# Config
bp.output_file('fantasy_data.html', title='940 24 St. Ballers Report')
width = 960
height = 800

# Load Fantasy Data
data = pd.read_csv('fantasy_scores.csv')
names = data.columns.values.tolist()[1:]
x = data['Week'].tolist()

# Get colors for plot traces
def get_colors(names):

	colors = {}
	
	for name in names:
		r = randint(0,200)
		g = randint(0,200)
		b = randint(0,200)
		
		colors[name] = (r,g,b)
		
	return colors
	
colors = get_colors(names)

# Plot Weekly Scores
fig = bp.figure(
	plot_width=width,
	plot_height=height,
	title="940 24 St. Ballers - Weekly Scores",
	toolbar_location="above")

fig.toolbar.active_drag = None
fig.xaxis.axis_label = "Week"
fig.yaxis.axis_label = "Score"

legend_items = []

for team in data.ix[:,1:]:
	y = data[[team]]
	lines = fig.line(x, y, color=colors[team], line_width=2)
	dots = fig.circle(x, y, color=colors[team], fill_color="white", size=8)
	
	tooltips=[
		('Team', '%s' % team),
		('Week', '@x'),
		('Score', '@y')]
	
	hov = HoverTool(renderers=[dots], tooltips=tooltips)
	fig.add_tools(hov)

	legend_items.append((team, [lines, dots]))
	
legend = Legend(items=legend_items, location=(0, -30))
fig.add_layout(legend, 'right')
	
plots.append(fig)


# Plot Cumulative Scores
fig = bp.figure(
	plot_width=width,
	plot_height=height,
	title="940 24 St. Ballers - Cumulative Weekly Scores",
	toolbar_location="above")

fig.toolbar.active_drag = None
fig.xaxis.axis_label = "Week"
fig.yaxis.axis_label = "Score"

legend_items = []
	
cum_data = data.ix[:,1:].cumsum()
	
for team in cum_data:
	y = cum_data[[team]]
	lines = fig.line(x, y, color=colors[team], line_width=2)
	dots = fig.circle(x, y, color=colors[team], fill_color="white", size=8)
	
	tooltips=[
		('Team', '%s' % team),
		('Week', '@x'),
		('Score', '@y')]
	
	hov = HoverTool(renderers=[dots], tooltips=tooltips)
	fig.add_tools(hov)
	
	legend_items.append((team, [lines, dots]))
	
legend = Legend(items=legend_items, location=(0, -30))
fig.add_layout(legend, 'right')
	
plots.append(fig)

# Plot Rolling Mean
fig = bp.figure(
	plot_width=width,
	plot_height=height,
	title="940 24 St. Ballers - Rolling Weekly Means",
	toolbar_location="above")

fig.toolbar.active_drag = None
fig.xaxis.axis_label = "Week"
fig.yaxis.axis_label = "Score"

legend_items = []
	
for team in cum_data:
	y = cum_data[team] / data['Week']
	
	lines = fig.line(x, y, color=colors[team], line_width=2)
	dots = fig.circle(x, y, color=colors[team], fill_color="white", size=8)
	
	tooltips=[
		('Team', '%s' % team),
		('Week', '@x'),
		('Score', '@y')]
	
	hov = HoverTool(renderers=[dots], tooltips=tooltips)
	fig.add_tools(hov)
	
	legend_items.append((team, [lines, dots]))
	
legend = Legend(items=legend_items, location=(0, -30))
fig.add_layout(legend, 'right')

plots.append(fig)


# Plot Deviation from Mean
fig = bp.figure(
	plot_width=width,
	plot_height=height,
	title="940 24 St. Ballers - Weekly Difference from Mean Score",
	toolbar_location="above")

fig.toolbar.active_drag = None
fig.xaxis.axis_label = "Week"
fig.yaxis.axis_label = "Score"

legend_items = []
	
mean_data = data.ix[:,1:].mean()
mean_data = data.ix[:,1:] - mean_data

for team in mean_data:
	y = mean_data[[team]]
	lines = fig.line(x, y, color=colors[team], line_width=2)
	dots = fig.circle(x, y, color=colors[team], fill_color="white", size=8)
	
	tooltips=[
		('Team', '%s' % team),
		('Week', '@x'),
		('Score', '@y')]
	
	hov = HoverTool(renderers=[dots], tooltips=tooltips)
	fig.add_tools(hov)
	
	legend_items.append((team, [lines, dots]))
	
legend = Legend(items=legend_items, location=(0, -30))
fig.add_layout(legend, 'right')

plots.append(fig)

bp.save(column(plots))