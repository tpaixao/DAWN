from PyQt5.QtWidgets import QTreeWidget,QTreeWidgetItem


### a reimplementation of QTreeWidgetItem to be able to handle checked signals!
###https://stackoverflow.com/questions/13662020/how-to-implement-itemchecked-and-itemunchecked-signals-for-qtreewidget-in-pyqt4 

class TreeWidgetItem(QTreeWidgetItem):
    def setData(self, column, role, value):
        state = self.checkState(column)
        QTreeWidgetItem.setData(self, column, role, value)
        if (role == Qt.CheckStateRole and state != self.checkState(column)):
            treewidget = self.treeWidget()
            if treewidget is not None:
                treewidget.itemChecked.emit(self, column)

class TreeWidget(QTreeWidget):
    itemChecked = pyqtSignal(object, int)

    def __init__(self, rows, columns):
        QTreeWidget.__init__(self)
        self.itemChecked.connect(self.handleItemChecked)

    def handleItemChecked(self,item,column):
        n_children = item.childCount()
        currState = item.checkState(0)
        for n_child in range(n_children):
            child = item.child(n_child)
            if currState == Qt.Checked:
                child.setCheckState(0, Qt.Checked)
            else: 
                child.setCheckState(0,Qt.Unchecked)
