import blink_detect

from blink_detect import df3
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df3["Start_string"]=df3["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df3["End_string"]=df3["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df3)

p=figure(x_axis_type='datetime',height=50, width=500, sizing_mode = "scale_width", title="Khoang thoi gian khong xuat hien mat")
p.yaxis.minor_tick_line_color = None
p.yaxis.ticker.desired_num_ticks = 1

hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="maroon",source=cds)

output_file("Graph1.html")
show(p)