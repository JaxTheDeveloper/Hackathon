import graphexport01
from blink_detect import df5
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
qart"].dt.strftime("%Y-%m-%d %H:%M:%S")
df5["End_string"]=df5["End"].dt.strftime("%Y-%m-%d %H:%M:%S")
df5["Pos_Str"]=df5["Face Pos Str"]
df5["Pos_End"]=df5["Face Pos End"]

cds=ColumnDataSource(df5)

p=figure(x_axis_type='datetime',height=50, width=500, sizing_mode = "scale_width", title="Khoang thoi gian nham mat")
p.yaxis.minor_tick_line_color=None
p.yaxis.ticker.desired_num_ticks = 1

hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string"),('Start Position',"@Pos_Str"),('End Position' ,"@Pos_End")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="orange",source=cds)

output_file("Graph3.html")
show(p)
