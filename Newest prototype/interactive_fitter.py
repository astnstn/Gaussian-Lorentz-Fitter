import matplotlib.pyplot as plt
from mathfunctions import *
from preset_functions import *
import numpy as np


plt.ion()


class DraggableNode:
    lock = None  # only one can be animated at a time
    composite = False  # determines whether to plot individually or summed
    functions = []  # the functions
    _instances = []  # widget instances

    def __init__(self, x, y, sigma, xspace=None):

        # initialises
        self.node = plt.gca().plot(x, y, 'o', color='red', picker=10)[0]
        self.press = None
        self.background = None
        self.function = Gaussian(y, x, sigma)
        self.xspace = xspace

        DraggableNode.functions.append(self.function)
        self.line = plt.gca().plot(
            xspace, self.function(xspace), color='grey')[0]
        DraggableNode._instances.append(self)

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.node.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.node.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.node.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)
        self.cidpick = self.node.figure.canvas.mpl_connect(
            'pick_event', self.on_pick)

    def on_press(self, event):

        if event.button == 2:
            return

        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.node.axes:
            return
        if DraggableNode.lock is not None:
            return  # if dragging something else then return

        contains, attrd = self.node.contains(event)
        if not contains:
            return  # return if click not in node
        x0, y0 = self.node.get_xdata(), self.node.get_ydata()  # x and y of node
        # stores the coordinates of the node and of the event
        self.press = x0, y0, event.xdata, event.ydata
        DraggableNode.lock = self  # sets the lock to current instance

        # draw everything but the selected func and store the pixel buffer
        canvas = self.node.figure.canvas
        axes = self.node.axes

        # animate only this peak
        if DraggableNode.composite == False:
            self.node.set_animated(True)
            self.line.set_animated(True)

        # animate all peaks
        else:
            [widget.line.set_animated(True)
             for widget in DraggableNode._instances]
            [widget.node.set_animated(True)
             for widget in DraggableNode._instances]

        # store the background
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.node.axes.bbox)
        # now redraw just the peak
        axes.draw_artist(self.node)
        axes.draw_artist(self.line)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if DraggableNode.lock is not self:
            return
        if event.inaxes != self.node.axes:
            return
        x0, y0, xpress, ypress = self.press

        # update node coords
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.node.set_xdata(x0+dx)
        self.node.set_ydata(y0+dy)

        # set params and draw this peak
        if DraggableNode.composite == False:
            self.function[0].params['amp'] = y0 + dy
            self.function[0].params['mean'] = x0 + dx
            self.line.set_ydata(self.function(self.xspace))

        # set params and draw all peaks
        else:
            self.function[0].params['amp'] = (y0 + dy) - (sum([func(self.node.get_xdata(
            )) for func in DraggableNode.functions]) - self.function[0].params['amp'])
            self.function[0].params['mean'] = x0 + dx
            for widget in DraggableNode._instances:
                if widget.line != self.line:
                    widget.line.set_ydata([None])
                    self.node.axes.draw_artist(widget.line)
                if widget.node != self.node:
                    widget.node.set_ydata(
                        sum([func(widget.node.get_xdata()) for func in DraggableNode.functions]))
            self.line.set_ydata(sum([func(self.xspace)
                                for func in DraggableNode.functions]))

        canvas = self.node.figure.canvas
        axes = self.node.axes

        # restore the background region
        canvas.restore_region(self.background)

        # draw peak(s)
        axes.draw_artist(self.node)
        axes.draw_artist(self.line)
        [axes.draw_artist(widget.node) for widget in DraggableNode._instances]

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_pick(self, event):
        if event.artist != self.node:
            return
        self.press = self.node.get_xdata(), self.node.get_ydata(
        ), self.node.get_xdata(), self.node.get_ydata()
        x0, x1 = self.node.axes.get_xlim()
        dx = x1 - x0
        dx = dx/200
        if event.mouseevent.button == "up":
            self.function[0].params['sigma'] += dx
        if event.mouseevent.button == "down":
            self.function[0].params['sigma'] -= dx
        self.on_press(event.mouseevent)
        self.on_motion(event.mouseevent)
        self.on_release(event.mouseevent)

    def on_release(self, event):
        'on release we reset the press data'
        if DraggableNode.lock is not self:
            return

        self.press = None
        DraggableNode.lock = None

        if DraggableNode.composite == True:
            [widget.node.set_animated(False)
             for widget in DraggableNode._instances]

        # turn off the rect animation property and reset the background
        self.node.set_animated(False)
        self.line.set_animated(False)
        self.background = None

        # redraw the full figure
        self.node.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.node.figure.canvas.mpl_disconnect(self.cidpress)
        self.node.figure.canvas.mpl_disconnect(self.cidrelease)
        self.node.figure.canvas.mpl_disconnect(self.cidmotion)


class Window:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(x, y, '.')
        xmin, xmax = self.ax.get_xlim()
        self.xspace = np.linspace(xmin, xmax, 1000)

        self.peaks = []

        plt.show()
        DraggableNode.functions.append(Line(0, 0))

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def on_click(self, event):
        if event.button != 2:
            return
        x0, x1 = self.ax.get_xlim()
        dx = x1 - x0
        dx = dx/15

        peak = DraggableNode(event.xdata, event.ydata, dx, xspace=self.xspace)
        peak.connect()
        self.peaks.append(peak)
        self.fig.canvas.draw()
        return

    def on_key(self, event):
        if event.key == " ":
            DraggableNode.composite = not DraggableNode.composite

            if DraggableNode.composite == False:
                for widget in DraggableNode._instances:
                    widget.line.set_ydata(widget.function(widget.xspace))
                    widget.line.set_animated(False)
                    widget.node.set_ydata([widget.function[0].params['amp']])

                [widget.line.set_color("grey")
                 for widget in DraggableNode._instances]
            if DraggableNode.composite == True:
                [widget.line.set_ydata([None])
                 for widget in DraggableNode._instances]
                DraggableNode._instances[-1].line.set_ydata(
                    sum([widget.function(widget.xspace) for widget in DraggableNode._instances]))
                for widget in DraggableNode._instances:
                    y = sum(wid.function(widget.node.get_xdata())
                            for wid in DraggableNode._instances)
                    widget.node.set_ydata([y[0]])
                    widget.node.set_animated(False)

                [widget.line.set_color('C0')
                 for widget in DraggableNode._instances]
                DraggableNode._instances[-1].line.set_animated(False)
        elif event.key == "a":
            function = join_functions(DraggableNode.functions)
            function.fit(self.x, self.y)

            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            self.ax.cla()
            [self.ax.plot(self.xspace, func(self.xspace), linestyle=':')
             for func in DraggableNode.functions]
            self.ax.plot(self.xspace, function(self.xspace), color='red')
            self.ax.plot(self.x, self.y, '.', color='C0')

            showparams = True
            if showparams:
                plt.axhline(y=0, color='grey', linestyle=':')
                for func in function[1:]:
                    plt.vlines(
                        x=func.params['mean'], ymin=-500, ymax=func.params['amp'], color='grey', linestyle=':')
                    mean = func.params['mean']
                    amp = func.params['amp']
                    std = func.params['sigma']
                    spacing = (ylim[1] - ylim[0])/15
                    texts = [plt.text(mean, amp + spacing, "A: {:.2f} \nμ: {:.2f}\nσ: {:.2f}".format(
                        amp, mean, std), fontsize=8, horizontalalignment='center', weight='bold')]
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)
        self.fig.canvas.draw()


x, y = np.loadtxt("1996quarter.txt", skiprows=1, unpack=True)
window = Window(x, y)
