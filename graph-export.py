from blink_detect import df3
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df3["Start_string"]=df3["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df3["End_string"]=df3["End"].dt.strftime("%Y-%m-%d %H:%M:%S")


cds=ColumnDataSource(df3)

p=figure(x_axis_type='datetime',height=100, width=500, sizing_mode = "scale_width", title="Motion Graph")
p.yaxis.minor_tick_line_color=None
# p.ygrid[0].ticker.desired_num_ticks=1
p.yaxis.ticker.desired_num_ticks = 1

hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="green",source=cds)

output_file("Graph1.html")
show(p)
