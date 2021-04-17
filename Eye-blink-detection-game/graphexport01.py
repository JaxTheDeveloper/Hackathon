import graphexport
import blink_detect
from blink_detect import df6
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df6["Start_string"]=df6["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df6["End_string"]=df6["End"].dt.strftime("%Y-%m-%d %H:%M:%S")
df6["Pos_Str"]=df6["Face Pos Str"]
df6["Pos_End"]=df6["Face Pos End"]

cds=ColumnDataSource(df6)

p=figure(x_axis_type='datetime',height=50, width=500, sizing_mode = "scale_width", title="Affirmative Graph")
p.yaxis.minor_tick_line_color=None
p.yaxis.ticker.desired_num_ticks = 1

hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string"),('Start Position',"@Pos_Str"),('End Position' ,"@Pos_End")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1,color="green",source=cds)

output_file("Graph2.html")
show(p)
