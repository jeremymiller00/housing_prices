import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import output_notebook, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Panel, CategoricalColorMapper
from bokeh.models.widgets import CheckboxGroup, Tabs, Panel
from bokeh.layouts import column, row, WidgetBox
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.palettes import Category20_16
from bokeh.layouts import row, column, gridplot


def hist_hover(dataframe, column, bins=30, log_scale=False, 
               colors=["navy", "orange"], show_plot=True):
    """
    A function for creating a bokeh histogram with hovertool interactivity
    """
    # build histogram data
    hist, edges = np.histogram(dataframe[column], bins = bins)
    hist_df = pd.DataFrame({column: hist,
                             "left": edges[:-1],
                             "right": edges[1:]})
    hist_df["interval"] = ["%d to %d" % (left, right) for left, 
                           right in zip(hist_df["left"], hist_df["right"])]
    # bokeh histogram with hover tool
    if log_scale == True:
        hist_df["log"] = np.log(hist_df[column])
        src = ColumnDataSource(hist_df)
        plot = figure(plot_height = 600, plot_width = 600,
              title = "Histogram of {}".format(column.capitalize()),
              x_axis_label = column.capitalize(),
              y_axis_label = "Log Count")    
        plot.quad(bottom = 0, top = "log",left = "left", 
            right = "right", source = src, fill_color = colors[0], 
            line_color = "black", fill_alpha = 0.7,
            hover_fill_alpha = 1.0, hover_fill_color = colors[1])
    else:
        src = ColumnDataSource(hist_df)
        plot = figure(plot_height = 600, plot_width = 600,
              title = "Histogram of {}".format(column.capitalize()),
              x_axis_label = column.capitalize(),
              y_axis_label = "Count")    
        plot.quad(bottom = 0, top = column,left = "left", 
            right = "right", source = src, fill_color = colors[0], 
            line_color = "black", fill_alpha = 0.7,
            hover_fill_alpha = 1.0, hover_fill_color = colors[1])
               
    # Hover tool referring to our own data field using @ and a position on the graph using $
    hover = HoverTool(tooltips = [('Interval', '@interval'),
                              ('Count', str("@" + column))])
    plot.add_tools(hover)
    if show_plot == True:
        show(plot)
    else:
        return plot

def histotabs(dataframe, features, bins=30, colors=['SteelBlue', 'Tan'], log_scale=False, show_plot=True):
    '''
    Builds tabbed interface for a series of histograms; relies on hist_hover
    '''
    hists = []
    for f in features:
        h = hist_hover(dataframe, f, bins=bins, colors=colors, log_scale=log_scale, show_plot=show_plot)
        p = Panel(child=h, title=f.capitalize())
        hists.append(p)
    t = Tabs(tabs=hists)
    show(t)