from PyQt5 import Qt, QtCore
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import ScalarFormatter
import numpy as np
from PyQt5 import sip

def best_x_chart(data_x, data_y, widget, isFullDay = False, Chart2D = False):
    clear_widget(widget)
    figure = Figure()
    canvas = FigureCanvas(figure)
    toolbar = NavigationToolbar(canvas)
    widget.setLayout(create_layout(toolbar, canvas))
    ax = figure.add_subplot(111)
    data_y_np = np.array(data_y)
    #canvas.gca().yaxis.set_minor_formatter(plt.ticker.NullFormatter())
    #ax.ticklabel_format(style='plain')
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(y_fmt))
    if isFullDay == False and Chart2D == False:
        ax.plot(data_x, data_y, '-bo')
        ax.tick_params(axis='x', labelsize=7)
        #myLocator = mpl.ticker.IndexLocator(base = 2, offset=0)
        #ax.xaxis.set_major_locator(myLocator)
    elif Chart2D == True:
        ax.plot(data_x, data_y, '-bo')
        ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(y_fmt))
    else:
        ax.plot(data_x, data_y)
        ax.tick_params(axis='x', labelsize=6)
        #myLocator = mpl.ticker.IndexLocator(base = 2, offset = 0)
        #ax.xaxis.set_major_locator(myLocator)
    #ax.xticks(rotation=90)
    figure.autofmt_xdate(rotation=35)
    canvas.draw()
    #figure = Figure()
    #canvas = FigureCanvas(figure)
    #toolbar = NavigationToolbar(canvas)
    #widget.setLayout(create_layout(toolbar, canvas))
    #ax = figure.add_subplot(111)
    #ax.plot(data_x, data_y)
    #canvas.draw()

def create_layout(toolbar, canvas):
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(toolbar)
    layout.addWidget(canvas)
    return layout

def y_fmt(x, y):
    return '${:2.1e}'.format(x).replace('e', '\\cdot 10^{') + '}$'

def best_3d_chart(data_x, data_y, data_z, widget):
    figure = Figure()
    canvas = FigureCanvas(figure)
    toolbar = NavigationToolbar(canvas)
    widget.setLayout(create_layout(toolbar, canvas))
    ax = figure.add_subplot(111, projection="3d")
    ax.clear()
    data_y_np = np.array(data_y)
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(y_fmt))
    ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(y_fmt))
    ax.zaxis.set_major_formatter(mpl.ticker.FuncFormatter(y_fmt))
    ax.plot(data_x, data_y,data_z, '-bo')
    figure.autofmt_xdate(rotation=45)
    canvas.draw()

def clear_widget(widget):
    for i,d in enumerate(widget.children()):
        sip.delete(d)

