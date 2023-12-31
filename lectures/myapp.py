# Server-side Gapminder Visualization
#
# Run this script in an Anaconda Prompt with:
#
#   python -m bokeh serve --show myapp.py
#

import numpy as np
import pandas as pd
import copy
import bokeh.layouts
from bokeh.models import ColumnDataSource, CustomJS, CDSView, GroupFilter
from bokeh.models.widgets import Slider
from bokeh.plotting import figure, curdoc

gapminder = pd.read_csv("../data/gapminder.csv")

# Set up the slider.
lower = gapminder["year"].min()
upper = gapminder["year"].max()
slider = Slider(start = lower, end = upper, value = lower, step = 1,
        title = "Year")

# Set up figure.
p = figure(title = str(lower), width = 800, height = 600, x_range = (0, 10),
        y_range = (10, 100))
p.xaxis.axis_label = "Fertility Rate"
p.yaxis.axis_label = "Life Expectancy"

# Set up data sources.
gapminder["sqrt_population"] = np.sqrt(gapminder["population"]) / 1000
is_year = gapminder["year"] == lower
source = ColumnDataSource(gapminder[is_year])

# Add the plot.
p.scatter("fertility_rate", "life_expectancy", size = "sqrt_population",
        source = source, fill_alpha = 0.2)

# ------------------------------------------------------------
# Set up the Python callback.
years = gapminder["year"].unique()

def callback(attr, old, new):
    # Compute the closest year to the slider year.
    idx = np.abs(years - slider.value).argmin()
    value = years[idx]

    # Subset the data with the year.
    is_year = gapminder["year"] == value
    new_source = ColumnDataSource(gapminder[is_year])

    # Set the title and update the data source.
    p.title.text = str(value)
    source.data = dict(new_source.data)

slider.on_change("value", callback)
# ------------------------------------------------------------

# Finally, set up the layout and show everything.
layout = bokeh.layouts.column(slider, p)
curdoc().add_root(layout)