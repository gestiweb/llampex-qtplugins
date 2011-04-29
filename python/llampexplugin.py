#!/usr/bin/env python

from PyQt4 import QtGui, QtDesigner
from llampexwidgets import FLClock, FLFieldDB, FLTableDB
from base64 import b64decode
clock32png = QtGui.QPixmap()
clock32png.loadFromData(
                b64decode(
                'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9sDBBQBG/S+WMoAAAnBSURBVFjDrZd7bNzVlcc/9/eYp98e'
                'x488ICXEtCFBiLZUPMxuy4aAIFRii3ZDSBQVxCNt1YjuH5sSqWIflbKbtixNoZCtQ5pQtYVkNwm4LE0DoRCHtEkd4yQmiu3YiSe2xzOe8Xjm95jfPfvHYG/SGrpo90jn9zs6Ouee7z333nPuhT9DN910E6+88sofq+MbNmy44bnn'
                'nluxdevW5Y8++ugywLjU4Pnnn+f/TC+88MKM/NBDDy3r7Oz86enTp51MJiOO41zG4+Pj0tvbm+rs7Hx68eLFjdN+mzdv/uSBH3jgAUQEgNWrV1/T1dV1cmpqSpxiUTzPEdGeTmcmdHIkJcMXU1IqObpUcsV1i1IsFiWbzcqxY8fe'
                'AKoAOjo6uO222/53wR977LEZee/evVuy2awUi0UR7ekLF8b1P37vdXnqX34lv9h/TM70j8q582nZ+N39svmZ38jWbW9LsVjQvufoYrEoqVRKdu7cuQbgzJkz3H333R8f/MEHH5yROzs73/E8T3zf1SOjE/prf/+K/OtzB2Ukk5eL'
                '43npPDEoyVReDnedk6HRSUmm8jI0MiHfffqA/PP3fy068LTjFLXjONLR0fEjgOPHj388gOm0HzlypNP3fREJ9PafvScbvvMfMpyalN5zaTk5kJaTAxnpHczKr4+clXe6LsipcxNyciAjJ/vT8sFgWs4lM/KNb++R4yeGdKnkat/3'
                '5bXXXnsa4KWXXrospjkttLe3c/311/Pqq69uaWtr+4ppmvL0tneUNjR3r7iOVNbF8cEpCY4vFD1NOBJDmRZFT+P4guNrCq4mX/C58YYFvP7maRWLRNTcxgq5cuGnvjB37twT69atO71p0yYOHToEgAJYuHAh/f39rFq16upt27Z9'
                'EI1GZMfLf1CZ/CTXLV1I3gOUgSij7PDhd5Ycllk06IA5VTa//M/f8/iaW+SKudUqnU7T0NBwmbMBsH37dgCefPLJPdFohFzeZ/vuTppa5jAw5jCW8xnL+qSyHmNZj7Gs+xHsMZb1GcuVSE0GnByc5MYbF/HNp/YpwzAkkUhw+PDh'
                'HwOsX7/+8qmsXbv20+3t7SeVUvLX63epv7j5KopE0GYIlEnYDAgE3MDENNSf20zlTOgAI/Bwsynqa2p4bNXnmJiYoLa2dmYAIx6PA7Bhw4YnlFLkCwG9A0mGxn2SEz4XMx7JjMvpCw5XNlYQNgP6kpMkMw7JdPFDdso8rcu4JDNu'
                '2XfCYyqw+Nn+4wBSU1PD7t27vzoNwMrn8yilqKur+wrA1pc61aJPNXA+4xJYBpgaARSKnx4c5I4bmrhmvsGR02nEsFDq8hN0KSkBtIftewTaoftsWi29qo7W1tb7gX8HsFR5BCuRSFQB/Ne7pwlXxsjlPbRtgqFn1kkp2Pe7Cyxb'
                'WE9zYwVnL2T4YNSlOhYiHi4vjdbCNBZBULqE4XqEYlH2v3mKpVfdTGVl5a0zGQB4+OGHW6PRKJ7ny8XxjNKuJpyIIdoCM0BrIe8GTDo+makS3ckJ6msrMIBEFbxzcgRCJqZlUBm1qQgbxEIWEdtE6QBcnwtD49w0NVnuZPF49DIA'
                'S5YsSQBkckX1T9+8i7d7zrPzdyPk7QAvEEqBlLeroSAC5x1NlXa547oWmuriaBsOD+YJECYCj4mCwJSABnSJtpYQP9j8N4yP5wCIRCIANuBbAK7rBo5TxLZNftvVz3v9KRxDKJolsA0MVBmAKv+1QFVtiHzg0TtWom9yCuKqbCLl'
                'Q6BEIQjighVR7HrjBJOpLPfdvuzSolHOQHd3dzKTyeC6vrx1rE8dy+Qxm5swYoIY/M/slUIpg5gSlrY28MbZMSolYCRsYIYViEZEUBoQjdKCGVK8NZTizaEhnrjnZgLfJZkcBijNFKKdO3eedV2Pxvpq1dRUR9gsYYQCjAgYFQZG'
                'pcKoNDCrLYIKuO/z8zg+VaC2yqRbAqz6MKrWQlVbGFUmZqVR9qswUGGNHdJYlGhorCE3OUmx6IxeVgkBCoXCQCCKO269Fl2YxFQ+ZlhjxsCsNDGrLFSNxdJ5lbjVIRKVBn8wSkQbI9h1NlZtmc2aaRBm2TekMXHxpjy+fOtiDNPC'
                'cZzf/AmA8fHxXYZp8fDyVnH9EJZfxDJKWDEwK0ysGotSWPira+fiaJ83giIVzTGs+jBmfRirPoxVZ2NV21jVJmaFgRURLOVhFAosvbaVq5vjYlk2J06c2DFTKy6pG1WZTCZbXRGTDduPqJ90/Ap7yZVIUy2qJoYfsbmzoR7DNtk7'
                'NUksEkYZqryTtAY/QEoB4pTA9WHKRWfyGBfSTPz+LK99/1v8ZWstI6NjesGCBeZlGejp6QHI9fX17dHKVD946FaxVC12KkuToYjbBguiNp9JVPGW6TGvuZr6RIy6RIz6RIz6+jh1iTi1dTFqayNUx20qTJhvGBjJMb54yy3csaxZ'
                'LDvE+++//3cAK1eunLWvhjOZjFNTXc0HY458eeMLak5rPeNzqrmqpY5z1WEqE1WosIVhmUzXYdGClAJ0waOUK+CPTuIOpogNpXCyNl0/XCciooaGhtJXXHFF/Z+040uu0e6ePXvu0yIsnhPlJ5vWSdfhQaL9Y+TGC8z1DRp8RbOy'
                'aTJDNIfCtNhhmk2bRkwSPtTmSsRH81hnkiSHNe/+2zoBKBaLbNy48bMAq1atYrY9QE9PD0uWLKGjo+MfVqxY8SQgw1Oa5Zt+ruIyQeO1C6mYnyBcG8eKh2nJOfQpIRqP4OUdnFSO3MAo/V3nuPqaz7D3idsFUL7v097evvKRRx7Z'
                't2PHDtasWTM7gOmuppRi3759m+68886nTNMEkGePjqhn9x8lPpWiqaUG3zD43t+2sePtHnrTUzjpLAMjBRrmzefb93+BL82PCaAKhQIvvvjiyscff3zfoUOHaGtr+/i7xKJFi2Za65YtW24fGRmRS0i/lxPZ/G5Snn39fXn23UH5'
                '+u4e+er2I/LjrrQMlco208Z9fX0j99xzz0KAAwcOfLLHydGjR2fkAwcObB4bG7sUiDiOJ4V8QZypgvwxnT9/3nn55ZfXT/tv3br1kwVfu3btrPpdu3bdf+rUqV9evHjxfD6fn3mW5XI5PTw8fKa7u3vbM88888XZfJcvXz7rmB95'
                'uVu9erXd0tKSiMViEa116OjRo2Yul6vp7e29MpVKJYBqoOZD8wkgP2fOnKzjOEPz5s0bb2trC2zbdnO5XGFwcHD44MGDpdniWB8FYGBgoOQ4Tjoej1tBEJjDw8NmyffHqqqqhvP5fIXv+6EgCAxAGYahQ6HQVDQaLRSLRRfwPM8L'
                'gEAp5du2XfpES3DXXXfx/0333nvvrPr/BoWlTx10OZEsAAAAAElFTkSuQmCC')
            ,"png")
            
class FLClockPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):
        super(FLClockPlugin, self).__init__(parent)

        self.initialized = False

    # The initialize() and isInitialized() methods allow the plugin to set up
    # any required resources, ensuring that this can only happen once for each
    # plugin.
    def initialize(self, core):

        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):

        return self.initialized

    # This factory method creates new instances of our custom widget with the
    # appropriate parent.
    def createWidget(self, parent):
        return FLClock(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "FLClock"

    # Returns the name of the group in Qt Designer's widget box that this
    # widget belongs to.
    def group(self):
        return "Llampex Widgets"

    # Returns the icon used to represent the custom widget in Qt Designer's
    # widget box.
    def icon(self):
        return QtGui.QIcon(clock32png)

    # Returns a short description of the custom widget for use in a tool tip.
    def toolTip(self):
        return ""

    # Returns a short description of the custom widget for use in a "What's
    # This?" help message for the widget.
    def whatsThis(self):
        return ""

    # Returns True if the custom widget acts as a container for other widgets;
    # otherwise returns False. Note that plugins for custom containers also
    # need to provide an implementation of the QDesignerContainerExtension
    # interface if they need to add custom editing support to Qt Designer.
    def isContainer(self):
        return False

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "llampexwidgets"
        

class FLFieldDBPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):
        super(FLFieldDBPlugin, self).__init__(parent)

        self.initialized = False

    # The initialize() and isInitialized() methods allow the plugin to set up
    # any required resources, ensuring that this can only happen once for each
    # plugin.
    def initialize(self, core):

        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):

        return self.initialized

    # This factory method creates new instances of our custom widget with the
    # appropriate parent.
    def createWidget(self, parent):
        return FLFieldDB(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "FLFieldDB"

    # Returns the name of the group in Qt Designer's widget box that this
    # widget belongs to.
    def group(self):
        return "Llampex Widgets"

    # Returns the icon used to represent the custom widget in Qt Designer's
    # widget box.
    def icon(self):
        return QtGui.QIcon(clock32png)

    # Returns a short description of the custom widget for use in a tool tip.
    def toolTip(self):
        return ""

    # Returns a short description of the custom widget for use in a "What's
    # This?" help message for the widget.
    def whatsThis(self):
        return ""

    # Returns True if the custom widget acts as a container for other widgets;
    # otherwise returns False. Note that plugins for custom containers also
    # need to provide an implementation of the QDesignerContainerExtension
    # interface if they need to add custom editing support to Qt Designer.
    def isContainer(self):
        return False

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "llampexwidgets"
        

class FLTableDBPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):

    # The __init__() method is only used to set up the plugin and define its
    # initialized variable.
    def __init__(self, parent=None):
        super(FLTableDBPlugin, self).__init__(parent)

        self.initialized = False

    # The initialize() and isInitialized() methods allow the plugin to set up
    # any required resources, ensuring that this can only happen once for each
    # plugin.
    def initialize(self, core):

        if self.initialized:
            return

        self.initialized = True

    def isInitialized(self):

        return self.initialized

    # This factory method creates new instances of our custom widget with the
    # appropriate parent.
    def createWidget(self, parent):
        return FLTableDB(parent)

    # This method returns the name of the custom widget class that is provided
    # by this plugin.
    def name(self):
        return "FLTableDB"

    # Returns the name of the group in Qt Designer's widget box that this
    # widget belongs to.
    def group(self):
        return "Llampex Widgets"

    # Returns the icon used to represent the custom widget in Qt Designer's
    # widget box.
    def icon(self):
        return QtGui.QIcon(clock32png)

    # Returns a short description of the custom widget for use in a tool tip.
    def toolTip(self):
        return ""

    # Returns a short description of the custom widget for use in a "What's
    # This?" help message for the widget.
    def whatsThis(self):
        return ""

    # Returns True if the custom widget acts as a container for other widgets;
    # otherwise returns False. Note that plugins for custom containers also
    # need to provide an implementation of the QDesignerContainerExtension
    # interface if they need to add custom editing support to Qt Designer.
    def isContainer(self):
        return False

    # Returns the module containing the custom widget class. It may include
    # a module path.
    def includeFile(self):
        return "llampexwidgets"

