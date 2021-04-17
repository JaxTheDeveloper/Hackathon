import graphexport01
from blink_detect import df5
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df5["Start_string"]=df5["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df5["End_string"]=df5["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df5)

p=figure(x_axis_type='datetime',height=100, width=500, sizing_mode = "scale_width", title="No Eye Graph")
p.yaxis.minor_tick_line_color=None
p.yaxis.ticker.desired_num_ticks = 1

hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="orange",source=cds)

output_file("Graph3.html")
show(p)
