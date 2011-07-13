#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
import math
class FLFieldDB(QtGui.QFrame):
    searchClicked = QtCore.pyqtSignal()
    enumFieldType = ["auto","string","optionlist","double",
                "number","uint","stringlist","pixmap","unlock",
                "serial","bool","date","time"]
                
    
    """
        AbanQfieldType / PostgreSQL Type        / AbanQWidget 
        'string'       : 'character varying'    : flabel-sbutton-lineedit
        'optionlist'   : 'character varying'    : flabel-combobox/listview
        'double'       : 'double precision'     : flabel-DoubleSpinbox/LineEdit
        'number'       : 'integer' ???          <<  
        'int'          : 'integer',             : flabel-Spinbox/LineEdit
        'uint'         : 'integer',            
        'unit'         : 'smallint',            -------------  >>
        'stringlist'   : 'text',                : flabel-plainTextEdit/textEdit
        'pixmap'       : 'text',                : flabel-graphicsView
        'unlock'       : 'boolean',             : ???? flabel-pushbutton(checkable) ???
        'serial'       : 'serial',              : ???? flabel-spinBox ???
        'bool'         : 'bool',                : checkbox  |  flabel-checkbox
        'date'         : 'date',                : flabel-dateedit(w/ or w/o calendar) / flabel-calendar
        'time'         : 'time',                : flabel-timeedit
        
        
        Several controls or behaviors were impossible for AbanQ:
        
        FieldName Migration:
            - To alter a column name without losing its data.
        
        ReadOnly:
            - Disable VS ReadOnly
            - ColorScheme for ReadOnly
        
        Group Fields by typology:
            - References, codes
            - Basic Descriptions
            - Prices / Costs
            - Options...
        -->>> And associate these groups to stylesheets that may change control colors, like background.
                ... this may help the user find what kind of information the form is requesting
                ---- readonly may add some changes
                ---- required fields may add some changes
                
        MultiFieldControls:
            - Controls that require a group of fields (multilingual, options, multicheckbox)
            
        Mainly a field is composed of:
            - lblFieldName: QLabel with Field Name
            - tbnSearch: QToolButton for search possible values for the field
            - txtField: FieldControl, depending on which fieldtype is.
            
        All controls (label, search button, text field):
            - Enabled :: Child controls get siabled when the parent is disabled too. 
                (so only makes sense for disabling some of them, not all)
            - Size Policy ?
            - Minimum / Maximum Sizes ?
            - Pallete ? 
            - Fonts / Bold ?
            - Tooltip ?
            - locale ?
            
        FieldName Label:
            - Manually set the label text, including rich text features.
            - Text replaceable by Pixmap / icon
                - scaledContents Yes/No for stretch the pixmap
            - manually determined size of the control or size policies.
            - manually set the text/pixmap aligment (left-right-top-bottom-center-middle)
            - capability of word wrapping
            - manually change textInteractionFlags (text selectable, editable, open external links..)
                * what means to edit a FieldName in a form? makes sense?
        
        Search Button:
            - May be other class or button style instead? QPushButton, QToolButton...
            - Is the only button action possible? maybe there more than one button? different actions?
            - May the icon change, text instead
            - May set the textflow settings of text+icon
            - Checkable, makes sense?
            - Popup-menu, more options (buttons) can appear when pressing and holding the button
            - configurable shortcuts
        
        All Text Field Edits:
            - Readonly yes/no
            - Frame yes/no
            - aligment
        
        FieldType String: (Assume string is for one-line string QLineEdit)
            - Other PostgreSQL datatypes for this could be:
                * text, for infinite one-line text
                * char, for fixed-width short text
                * int/double/number , with inputmask 0000...  and conversion to number on save.
            - patterns / formats?
                - InputMask, 999999A
                - Validators (we should precreate validators or... )
            - echoMode for passwords and so.
            - auto md5/sha1 (hash) on save? cipher on save?
            - placeHolderText (like "Write here your fielddata") --> collapse field label with placeholder text
            - what about multilingual texts? they may span multiple fields in database.
            ** main problems:
                * with inputmask, the control seems to do it wrong, maybe confuses the user
                
        FieldType OptionString: (QComboBox)
            - Editable: A QLineEdit with dropdown of options. Remembers previous entered items.
                - InsertPolicy: AtBottom, AtCurrent, Alphabetically.
            - May allow icons along with options
            
        FieldType OptionString: (QListWidget)
            
        FieldType Uint: (QSpinBox) (also, QDial, QSlider)
            - wrapping ( 99.99 -> 0.0)
            - buttonSymbols -> arrows, plusminus, none
            - specialValueText (Maybe for mapping None? )
            - accelerated yes/no
            - correctionMode -> previousvalue, nearestvalue
            - keyboardtraking yes/no
            ::::::::::::
            - suffix, prefix
            - minimum, maximum
            - singleStep
            :::::
            ** main problems:
                * awful control to fill data with keyboard.
        
        FieldType Double: (QDoubleSpinBox)
            - wrapping ( 99.99 -> 0.0)
            - buttonSymbols -> arrows, plusminus, none
            - specialValueText (Maybe for mapping None? )
            - accelerated yes/no
            - correctionMode -> previousvalue, nearestvalue
            - keyboardtraking yes/no
            ::::::::::::
            - suffix, prefix
            - minimum, maximum
            - singleStep
            - decimals 
            :::::
            ** main problems:
                * awful control to fill data with keyboard.
        
        Control Layout:
            - Horizontal / Vertical
            - Straight / Reversed Order
            
        modes:
            -> Auto (Automatically selects the proper mode for the fieldType)
            -> LineEdit
    """
    #modeList = ["Auto","LineEdit","Multiline","Checkbox","Radio]
    
    def __init__(self, parent=None):
        super(FLFieldDB, self).__init__(parent)
        self._layout = QtGui.QHBoxLayout()
        self._labelSuffix = ": "
        self._label = QtGui.QLabel("FieldName" + self._labelSuffix)
        self._button = QtGui.QToolButton() # TODO: change to tool button.
        self._button.setText("::")
        self._editors = {
            'line' : QtGui.QLineEdit("FieldContent"),
            'checkbox' : QtGui.QCheckBox("FieldContent"),
            'combobox' : QtGui.QComboBox(),
            'spinbox' : QtGui.QSpinBox(),
        }
        self._editor = self._editors['line']
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._button)
        for editor in self._editors.values():
            editor.setVisible(False)
            editor.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
            self._layout.addWidget(editor)
        self._label.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        self._button.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        self._editor.setVisible(True)
        self._layout.setSpacing(0)
        self._margin = 3
        self._layout.setContentsMargins(self._margin,self._margin,self._margin,self._margin)
        self.setLayout(self._layout)
        
        self._fieldName = ""
	self._tableName = ""
	self._fieldRelation = ""
	self._foreignField = ""
	self._actionName = ""
        self.connect(self._button, QtCore.SIGNAL("released()"),
                        self.searchClicked)
        self._mode = 0
        self._fieldType = 0
    
    def getFieldName(self):
        return self._fieldName
    
    @QtCore.pyqtSlot(str)
    def setFieldName(self,value):
        self._fieldName = value
    
    def resetFieldName(self):
        self._fieldName = ""

    def getTableName(self):
        return self._tableName
    
    @QtCore.pyqtSlot(str)
    def setTableName(self,value):
        self._tableName = value
    
    def resetTableName(self):
        self._tableName = ""

    def getFieldRelation(self):
        return self._fieldRelation
    
    @QtCore.pyqtSlot(str)
    def setFieldRelation(self,value):
        self._fieldRelation = value
    
    def resetFieldRelation(self):
        self._fieldRelation = ""

    def getForeignField(self):
        return self._foreignField
    
    @QtCore.pyqtSlot(str)
    def setForeignField(self,value):
        self._foreignField = value
    
    def resetForeignField(self):
        self._foreignField = ""

    def getActionName(self):
        return self._actionName
    
    @QtCore.pyqtSlot(str)
    def setActionName(self,value):
        self._actionName = value
    
    def resetActionName(self):
        self._actionName = ""
    
    def setMargin(self,value): 
        self._margin = value
        self._layout.setContentsMargins(self._margin,self._margin,self._margin,self._margin)
    
    def getMargin(self): return self._margin

    @QtCore.pyqtSlot(str)
    def setLabelSuffix(self,value): self._labelSuffix = value; self.setLabelText(self.getLabelText())
    def getLabelSuffix(self): return self._labelSuffix
    
    @QtCore.pyqtSlot(str)
    def setLabelText(self,value): return self._label.setText(value+self._labelSuffix)
    def getLabelText(self): 
        if self._labelSuffix:
            x = len(self._labelSuffix)
            return self._label.text()[:-x] 
        else:
            return self._label.text()

    @QtCore.pyqtSlot(int)
    def setLabelMinWidth(self,value): 
        self._label.setMinimumWidth(value)
        
    def getLabelMinWidth(self): return self._label.minimumWidth()

    @QtCore.pyqtSlot(str)
    def setButtonText(self,value): return self._button.setText(value)
    def getButtonText(self): return self._button.text()
    
    def getEditorText(self): return self._editor.text()
    
    @QtCore.pyqtSlot(str)
    def setEditorText(self,value): return self._editor.setText(value)
    
    @QtCore.pyqtSlot()
    def resetEditorText(self): return self._editor.setText("")
    
    @QtCore.pyqtSlot(bool)
    def setLabelVisible(self,value): self._label.setVisible(value)
    def isLabelVisible(self): return self._label.isVisible()
    
    @QtCore.pyqtSlot(bool)
    def setEditorVisible(self,value): self._editor.setVisible(value)
    def isEditorVisible(self): return self._editor.isVisible()
    
    @QtCore.pyqtSlot(bool)
    def setButtonVisible(self,value): self._button.setVisible(value)
    def isButtonVisible(self): return self._button.isVisible()
    
    margin = QtCore.pyqtProperty(int, getMargin, setMargin, None)
    
    fieldName = QtCore.pyqtProperty(str, getFieldName, setFieldName, resetFieldName)
    tableName = QtCore.pyqtProperty(str, getTableName, setTableName, resetTableName)
    fieldRelation = QtCore.pyqtProperty(str, getFieldRelation, setFieldRelation, resetFieldRelation)
    foreignField = QtCore.pyqtProperty(str, getForeignField, setForeignField, resetForeignField)
    actionName = QtCore.pyqtProperty(str, getActionName, setActionName, resetActionName)

    labelSuffix = QtCore.pyqtProperty(str, getLabelSuffix, setLabelSuffix, None)
    labelMinWidth = QtCore.pyqtProperty(int, getLabelMinWidth, setLabelMinWidth, None)
    
    editorText = QtCore.pyqtProperty(str, getEditorText, setEditorText, resetEditorText)
    labelText = QtCore.pyqtProperty(str, getLabelText, setLabelText, None)
    buttonText = QtCore.pyqtProperty(str, getButtonText, setButtonText, None)
    
    labelVisible = QtCore.pyqtProperty(bool, isLabelVisible, setLabelVisible, None)
    editorVisible = QtCore.pyqtProperty(bool, isEditorVisible, setEditorVisible, None)
    buttonVisible = QtCore.pyqtProperty(bool, isButtonVisible, setButtonVisible, None)
    
    def getFieldType(self): return self._fieldType
    def setFieldType(self,value): 
        if value < 0 or value >= len(self.enumFieldType): return False
        self._fieldType = value
        self.updateFieldType()
        
    def updateFieldType(self):
        typeName = self.enumFieldType[self._fieldType]
        neweditor = self._editors['line']
        if typeName == 'bool':  neweditor = self._editors['checkbox']
        if typeName == 'optionlist':  neweditor = self._editors['combobox']
        if typeName == 'uint':  neweditor = self._editors['spinbox']
        
        if neweditor != self._editor:
            print "typeName:", typeName, "newEditor:", type(neweditor)
            self._editor.setVisible(False)
            self._editor = neweditor
            self._editor.setVisible(True)
    
    def getFieldTypeName(self): return self.enumFieldType[self._fieldType]
    def setFieldTypeName(self,value): 
        try:
            self._fieldType = self.enumFieldType.index(value)
            self.updateFieldType()
        except ValueError:
            return False
    
    fieldType = QtCore.pyqtProperty(int, getFieldType, setFieldType, None)
    fieldTypeName = QtCore.pyqtProperty(str, getFieldTypeName, setFieldTypeName, None)






class FLClock(QtGui.QWidget):
    # Emitted when the clock's time changes.
    timeChanged = QtCore.pyqtSignal(QtCore.QTime)

    # Emitted when the clock's time zone changes.
    timeZoneChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):

        super(FLClock, self).__init__(parent)

        self.timeZoneOffset = 0

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.timeout.connect(self.updateTime)
        timer.start(60)

        self.setWindowTitle(QtCore.QObject.tr(self, "Analog Clock"))
        self.resize(200, 200)

        self.hourHand = QtGui.QPolygon([
            QtCore.QPoint(7, 8),
            QtCore.QPoint(-7, 8),
            QtCore.QPoint(0, -40)
        ])
        self.minuteHand = QtGui.QPolygon([
            QtCore.QPoint(7, 8),
            QtCore.QPoint(-7, 8),
            QtCore.QPoint(0, -70)
        ])
        self.secondHand = QtGui.QPolygon([
            QtCore.QPoint(3, 2),
            QtCore.QPoint(0, 6),
            QtCore.QPoint(-3, 2),
            QtCore.QPoint(0, -100)
        ])

        self.hourColor = QtGui.QColor(0, 127, 0)
        self.minuteColor = QtGui.QColor(0, 127, 127, 191)
        self.secondColor = QtGui.QColor(255, 100, 21, 190)
        self.hourPen = QtGui.QPen(QtGui.QBrush(QtCore.Qt.Dense5Pattern),3)

    def paintEvent(self, event):

        side = min(self.width(), self.height())
        time = QtCore.QTime.currentTime()
        time = time.addSecs(self.timeZoneOffset * 3600)

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.hourColor))

        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(self.hourHand)
        painter.restore()

        painter.setPen(self.hourColor)
        painter.setPen(self.hourPen)

        for i in range(0, 12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.minuteColor))

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(self.minuteHand)
        painter.restore()

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.secondColor))

        painter.save()
        painter.rotate(6.0 * (time.second() + (time.msec() / 1000.0) ** 3.0 ))
        painter.drawConvexPolygon(self.secondHand)
        painter.restore()
        
        painter.setPen(QtGui.QPen(self.minuteColor))

        for j in range(0, 60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)

        painter.end()

    def minimumSizeHint(self):

        return QtCore.QSize(50, 50)

    def sizeHint(self):

        return QtCore.QSize(100, 100)

    def updateTime(self):

        self.timeChanged.emit(QtCore.QTime.currentTime())

    # The timeZone property is implemented using the getTimeZone() getter
    # method, the setTimeZone() setter method, and the resetTimeZone() method.

    # The getter just returns the internal time zone value.
    def getTimeZone(self):

        return self.timeZoneOffset

    # The setTimeZone() method is also defined to be a slot. The @pyqtSlot
    # decorator is used to tell PyQt which argument type the method expects,
    # and is especially useful when you want to define slots with the same
    # name that accept different argument types.

    @QtCore.pyqtSlot(int)
    def setTimeZone(self, value):

        self.timeZoneOffset = value
        self.timeZoneChanged.emit(value)
        self.update()

    # Qt's property system supports properties that can be reset to their
    # original values. This method enables the timeZone property to be reset.
    def resetTimeZone(self):

        self.timeZoneOffset = 0
        self.timeZoneChanged.emit(0)
        self.update()

    # Qt-style properties are defined differently to Python's properties.
    # To declare a property, we call pyqtProperty() to specify the type and,
    # in this case, getter, setter and resetter methods.
    timeZone = QtCore.pyqtProperty(int, getTimeZone, setTimeZone, resetTimeZone)

class LlItemView(QtGui.QFrame):
    searchClicked = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(LlItemView, self).__init__(parent)
        self._layout = QtGui.QHBoxLayout()
        self._labelSuffix = ": "
        self._label = QtGui.QLabel("FieldName" + self._labelSuffix)
        font = self._label.font()
        font.setBold(True)
        self._label.setFont(font)

        self._button = QtGui.QToolButton()
        self._button.setText("::")
        self._editor = QtGui.QLineEdit("FieldContent")
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._button)
        self._editor.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Minimum)
        self._layout.addWidget(self._editor)
        self._label.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self._button.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        self._layout.setSpacing(0)
        self._margin = 3
        self._layout.setContentsMargins(self._margin,self._margin,self._margin,self._margin)
        self.setLayout(self._layout)
        
        self._fieldName = ""
        self._tableName = ""
        self._fieldRelation = ""
        self._foreignField = ""
        self._actionName = ""
        self.connect(self._button, QtCore.SIGNAL("released()"),
                        self.searchClicked)
        self._mode = 0
        self._fieldType = 0
        self.setMaximumHeight(48)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Minimum)
    
    #def sizeHint(self):
    #   return QtCore.QSize(80,20)
    def setSizePolicy(self, *args):
        ret = QtGui.QFrame.setSizePolicy(self,*args)
        self._editor.setSizePolicy(self.sizePolicy())
        return ret        
    
    def replaceEditorWidget(self, widget):
        try: self._editor.close()
        except Exception, e: print e
        self._editor = widget
        self._editor.setSizePolicy(self.sizePolicy())
        self._layout.addWidget(self._editor)
    
    def getFieldName(self):
        return self._fieldName
    
    @QtCore.pyqtSlot(str)
    def setFieldName(self,value):
        self._fieldName = value
    
    def resetFieldName(self):
        self._fieldName = ""

    def getTableName(self):
        return self._tableName
    
    @QtCore.pyqtSlot(str)
    def setTableName(self,value):
        self._tableName = value
    
    def resetTableName(self):
        self._tableName = ""

    def getFieldRelation(self):
        return self._fieldRelation
    
    @QtCore.pyqtSlot(str)
    def setFieldRelation(self,value):
        self._fieldRelation = value
    
    def resetFieldRelation(self):
        self._fieldRelation = ""

    def getForeignField(self):
        return self._foreignField
    
    @QtCore.pyqtSlot(str)
    def setForeignField(self,value):
        self._foreignField = value
    
    def resetForeignField(self):
        self._foreignField = ""

    def getActionName(self):
        return self._actionName
    
    @QtCore.pyqtSlot(str)
    def setActionName(self,value):
        self._actionName = value
    
    def resetActionName(self):
        self._actionName = ""
    
    def setMargin(self,value): 
        self._margin = value
        self._layout.setContentsMargins(self._margin,self._margin,self._margin,self._margin)
    
    def getMargin(self): return self._margin

    @QtCore.pyqtSlot(str)
    def setLabelSuffix(self,value): self._labelSuffix = value; self.setLabelText(self.getLabelText())
    def getLabelSuffix(self): return self._labelSuffix
    
    @QtCore.pyqtSlot(str)
    def setLabelText(self,value): return self._label.setText(value+self._labelSuffix)
    def getLabelText(self): 
        if self._labelSuffix:
            x = len(self._labelSuffix)
            return self._label.text()[:-x] 
        else:
            return self._label.text()

    @QtCore.pyqtSlot(int)
    def setLabelMinWidth(self,value): 
        self._label.setMinimumWidth(value)
        
    def getLabelMinWidth(self): return self._label.minimumWidth()

    @QtCore.pyqtSlot(str)
    def setButtonText(self,value): return self._button.setText(value)
    def getButtonText(self): return self._button.text()
    
    def getEditorText(self): return self._editor.text()
    
    @QtCore.pyqtSlot(str)
    def setEditorText(self,value): return self._editor.setText(value)
    
    @QtCore.pyqtSlot()
    def resetEditorText(self): return self._editor.setText("")
    
    @QtCore.pyqtSlot(bool)
    def setLabelVisible(self,value): self._label.setVisible(value)
    def isLabelVisible(self): return self._label.isVisible()
    
    @QtCore.pyqtSlot(bool)
    def setEditorVisible(self,value): self._editor.setVisible(value)
    def isEditorVisible(self): return self._editor.isVisible()
    
    @QtCore.pyqtSlot(bool)
    def setButtonVisible(self,value): self._button.setVisible(value)
    def isButtonVisible(self): return self._button.isVisible()
    
    margin = QtCore.pyqtProperty(int, getMargin, setMargin, None)
    
    fieldName = QtCore.pyqtProperty(str, getFieldName, setFieldName, resetFieldName)
    tableName = QtCore.pyqtProperty(str, getTableName, setTableName, resetTableName)
    fieldRelation = QtCore.pyqtProperty(str, getFieldRelation, setFieldRelation, resetFieldRelation)
    foreignField = QtCore.pyqtProperty(str, getForeignField, setForeignField, resetForeignField)
    actionName = QtCore.pyqtProperty(str, getActionName, setActionName, resetActionName)

    labelSuffix = QtCore.pyqtProperty(str, getLabelSuffix, setLabelSuffix, None)
    labelMinWidth = QtCore.pyqtProperty(int, getLabelMinWidth, setLabelMinWidth, None)
    
    editorText = QtCore.pyqtProperty(str, getEditorText, setEditorText, resetEditorText)
    labelText = QtCore.pyqtProperty(str, getLabelText, setLabelText, None)
    buttonText = QtCore.pyqtProperty(str, getButtonText, setButtonText, None)
    
    labelVisible = QtCore.pyqtProperty(bool, isLabelVisible, setLabelVisible, None)
    editorVisible = QtCore.pyqtProperty(bool, isEditorVisible, setEditorVisible, None)
    buttonVisible = QtCore.pyqtProperty(bool, isButtonVisible, setButtonVisible, None)



class FLTableDB(QtGui.QFrame):
    searchClicked = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(FLTableDB, self).__init__(parent)
        self._layout = QtGui.QHBoxLayout()
        self._editors = {
            'table' : QtGui.QTableWidget(),
        }
        self._editor = self._editors['table']
        for editor in self._editors.values():
            editor.setVisible(False)
            editor.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
            self._layout.addWidget(editor)
        self._editor.setVisible(True)
        self._layout.setSpacing(0)
        self._margin = 3
        self._layout.setContentsMargins(self._margin,self._margin,self._margin,self._margin)
        self.setLayout(self._layout)
        
        self._actionName = ""
	self._tableName = ""
	self._fieldRelation = ""
	self._foreignField = ""
    
    def getActionName(self):
        return self._actionName
    
    @QtCore.pyqtSlot(str)
    def setActionName(self,value):
        self._actionName = value
    
    def resetActionName(self):
        self._actionName = ""
    
    def getTableName(self):
        return self._tableName
    
    @QtCore.pyqtSlot(str)
    def setTableName(self,value):
        self._tableName = value
    
    def resetTableName(self):
        self._tableName = ""

    def getFieldRelation(self):
        return self._fieldRelation
    
    @QtCore.pyqtSlot(str)
    def setFieldRelation(self,value):
        self._fieldRelation = value
    
    def resetFieldRelation(self):
        self._fieldRelation = ""

    def getForeignField(self):
        return self._foreignField
    
    @QtCore.pyqtSlot(str)
    def setForeignField(self,value):
        self._foreignField = value
    
    def resetForeignField(self):
        self._foreignField = ""
    
    actionName = QtCore.pyqtProperty(str, getActionName, setActionName, resetActionName)
    tableName = QtCore.pyqtProperty(str, getTableName, setTableName, resetTableName)
    fieldRelation = QtCore.pyqtProperty(str, getFieldRelation, setFieldRelation, resetFieldRelation)
    foreignField = QtCore.pyqtProperty(str, getForeignField, setForeignField, resetForeignField)


class LlTableDB(QtGui.QTableView):
    searchClicked = QtCore.pyqtSignal()
   
    def __init__(self, parent=None):
        super(LlTableDB, self).__init__(parent)
        
        self._actionName = ""
	self._tableName = ""
	self._fieldRelation = ""
	self._foreignField = ""
    
    def getActionName(self):
        return self._actionName
    
    @QtCore.pyqtSlot(str)
    def setActionName(self,value):
        self._actionName = value
    
    def resetActionName(self):
        self._actionName = ""
    
    def getTableName(self):
        return self._tableName
    
    @QtCore.pyqtSlot(str)
    def setTableName(self,value):
        self._tableName = value
    
    def resetTableName(self):
        self._tableName = ""

    def getFieldRelation(self):
        return self._fieldRelation
    
    @QtCore.pyqtSlot(str)
    def setFieldRelation(self,value):
        self._fieldRelation = value
    
    def resetFieldRelation(self):
        self._fieldRelation = ""

    def getForeignField(self):
        return self._foreignField
    
    @QtCore.pyqtSlot(str)
    def setForeignField(self,value):
        self._foreignField = value
    
    def resetForeignField(self):
        self._foreignField = ""
    
    actionName = QtCore.pyqtProperty(str, getActionName, setActionName, resetActionName)
    tableName = QtCore.pyqtProperty(str, getTableName, setTableName, resetTableName)
    fieldRelation = QtCore.pyqtProperty(str, getFieldRelation, setFieldRelation, resetFieldRelation)
    foreignField = QtCore.pyqtProperty(str, getForeignField, setForeignField, resetForeignField)


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    field1 = FLFieldDB()
    field1.show()

    table1 = FLTableDB()
    table1.show()

    llampexTable = LlTableDB()
    llampexTable.show()
    
    sys.exit(app.exec_())

