import wx
import wx.dataview as DV
import re
import json

class TreeItemDataType():
    Null = 0
    String = 1
    Number = 2
    Object = 3
    Array = 4
    Boolean = 5

    def GetTypeIndex(data):
        if type(data) == str:
            return TreeItemDataType.String
        elif type(data) == int or type(data) == float:
            return TreeItemDataType.Number
        elif type(data) == dict:
            return TreeItemDataType.Object
        elif type(data) == list:
            return TreeItemDataType.Array
        elif type(data) == bool:
            return TreeItemDataType.Boolean
        else:
            return TreeItemDataType.Null

                
class EditJSONTreeItemDiaglogueWindow(wx.Dialog):
    def __init__(self, parent, showKey=True, values=None):
        wx.Dialog.__init__(self, parent, title="Edit Json Object")
        self.v_box = wx.BoxSizer(wx.VERTICAL)

        self.ValueTypedLabel = wx.StaticText(self, label="Value Type")
        self.ValueTypeSelect = wx.Choice(self, choices=['None', 'String', 'Number', 'Object', 'Array', 'Boolean'])
        self.ValueTypeSelect.SetSelection(TreeItemDataType.String)
        if values and values[1]:
            self.ValueTypeSelect.SetSelection(values[1])   

        self.ValueTypeSelect.Bind(wx.EVT_CHOICE, self.OnValueTypeChanged)

        self.ValueInputFieldLabel = wx.StaticText(self, label="Value")
        self.ValueInputField = wx.TextCtrl(self)
        if values and values[2]:
            if self.ValueTypeSelect.GetSelection() == TreeItemDataType.String or self.ValueTypeSelect.GetSelection() == TreeItemDataType.Number:
                self.ValueInputField.SetValue(str(values[2]))

        self.ValueInputField.Bind(wx.EVT_TEXT, self.ValidateValue)

    
        self.KeyInputField = wx.TextCtrl(self)
        self.KeyInputField.Hide()
        if showKey:
            self.KeyInputFieldLabel = wx.StaticText(self, label="Field Name")
            self.KeyInputField.Show()
            self.v_box.Add(self.KeyInputFieldLabel,0, wx.EXPAND|wx.ALL, 3)
            self.v_box.Add(self.KeyInputField, 0, wx.EXPAND|wx.ALL, 3)
            if values and values[0]:
                self.KeyInputField.SetValue(values[0])
        
        self.buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.OkBtn = wx.Button(self, label='OK')
        self.OkBtn.Bind(wx.EVT_BUTTON, self.OnOK)
        self.CancelBtn = wx.Button(self, label='Cancel')
        self.CancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.buttons_sizer.Add(self.CancelBtn)
        self.buttons_sizer.Add(self.OkBtn)
        
        self.v_box.Add(self.ValueTypedLabel,0, wx.EXPAND|wx.ALL, 3)
        self.v_box.Add(self.ValueTypeSelect, 0, wx.EXPAND|wx.ALL, 3)

        self.v_box.Add(self.ValueInputFieldLabel,0, wx.EXPAND|wx.ALL, 3)
        self.v_box.Add(self.ValueInputField, 0, wx.EXPAND|wx.ALL, 3)
        self.v_box.Add(self.buttons_sizer, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizerAndFit(self.v_box)
        return

    def OnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)
    
    def OnOK(self, event):
        if self.ValidateValue(event):
            self.EndModal(wx.ID_OK)
        else:
            dlg = wx.MessageDialog(self, 'Value input not valid', 'Invalid Value')
            dlg.ShowModal()

    def OnValueTypeChanged(self, event):
        selection = self.ValueTypeSelect.GetSelection()
        if selection == TreeItemDataType.Object or selection == TreeItemDataType.Array or selection == TreeItemDataType.Null:
            self.ValueInputField.Disable()
        else:
            self.ValueInputField.Enable()
            self.ValidateValue(event)


    def ValidateValue(self, event):
        isValid = True
        selection = self.ValueTypeSelect.GetSelection()
        if selection == TreeItemDataType.Number:
            if not re.match(r'^-?\d+\.?\d*$', self.ValueInputField.GetValue()):
                isValid = False
        elif selection == TreeItemDataType.Boolean:
            if not re.match(r'^true|false|True|False$', self.ValueInputField.GetValue()):
                isValid = False
        
        if not isValid:
            self.ValueInputField.SetBackgroundColour(colour=wx.RED)
        else:
            self.ValueInputField.SetBackgroundColour(colour=wx.WHITE)

        return isValid
    
    def GetDialogueValues(self):
        """
        return user input values in the form or a 3-tuple (key, value type, value)
        """
        selection = self.ValueTypeSelect.GetSelection()
        
        key = self.KeyInputField.GetValue()

        value = self.ValueInputField.GetValue()
        if selection == TreeItemDataType.Array:
            value = r"[]"
        elif selection == TreeItemDataType.Object:
            value = r"{}"
        elif selection == TreeItemDataType.Null:
            value = "null"
        return(key, selection, value)


class JSONTreeView(DV.TreeListCtrl):

    def __init__(self, parent):
        """"""
        DV.TreeListCtrl.__init__(self, parent, style=DV.TL_NO_HEADER|DV.TL_SINGLE)
        self.GetDataView().SetWindowStyle(DV.DV_VERT_RULES|DV.DV_HORIZ_RULES)
        self.Bind(DV.EVT_TREELIST_ITEM_ACTIVATED, self.OnActivated)
        self.Bind(DV.EVT_TREELIST_ITEM_CONTEXT_MENU, self.OnActivated)
        self.AppendColumn("Key")
        self.AppendColumn("Value")

    def UpdateTreeViewFromJSONData(self, JSON_Object={}):
        """
        Update the entire tree view with decoded JSON data
        """
        self.DeleteAllItems()
        tree_parent = self.GetRootItem()
        self.BuildTreeViewFromJSONDataRecursively(JSON_Object, tree_parent)

    def BuildTreeViewFromJSONDataRecursively(self, JSON_Object, tree_parent):
        if tree_parent and JSON_Object:
            JSONparent = JSON_Object
            if type(JSON_Object) == dict:
                if tree_parent != self.GetRootItem():
                    key = self.GetItemText(tree_parent)
                    self.SetRowText(tree_parent, (key, TreeItemDataType.Object, r'{}'))
                for key in JSON_Object:
                    tree_item = self.AppendItem(tree_parent, key)
                    
                    value = JSONparent[key]
                    self.BuildTreeViewFromJSONDataRecursively(value, tree_item)
            elif type(JSON_Object) == list:
                key = self.GetItemText(tree_parent)
                self.SetRowText(tree_parent, (key, TreeItemDataType.Array, '[]'))
                for array_item in JSON_Object:
                    array_tree_item = self.AppendItem(tree_parent, "")
                    self.BuildTreeViewFromJSONDataRecursively(array_item, array_tree_item)
                self.UpdateArrayItemChildrenIndex(tree_parent)
            else: #End of chain
                key = self.GetItemText(tree_parent)
                item_type = TreeItemDataType.GetTypeIndex(JSON_Object)
                self.SetRowText(tree_parent, (key, item_type, str(JSON_Object)))



    def GenerateJSONData(self, JSON_Object):
        """
        Generate JSON data from the form
        """
        #TODO
        return

    def OnActivated(self, event: DV.TreeListEvent):
        self.activated = event.GetItem()
        
        popupmenu = wx.Menu()
        if self.activated != self.GetRootItem():
            popupmenu.Append(1, 'Edit Item', helpString='Edit the selected item')
            popupmenu.Append(2, 'Delete Item', helpString='Delete the selected item')
            popupmenu.Append(4, 'Insert Sibling Under', helpString='Insert another item after the selected')
        popupmenu.Append(3, 'Append Child Item', helpString='Append a child item under the selected')
        popupmenu.Bind(wx.EVT_MENU, self.ContextMenuItemHandler)

        self.PopupMenu(popupmenu)

    def ContextMenuItemHandler(self, event):
        ID = event.GetId()
        if ID == 1:
            self.OnEditItem()
        elif ID == 2:
            self.OnDeleteItem()
        elif ID == 3:
            self.OnAppendChild()
        elif ID == 4:
            self.OnInsert()

    def OnEditItem(self):

        current_values = self.GetValuesFromRow(self.activated)

        show_key = True

        parent = self.GetItemParent(self.activated)
        parent_type = self.GetParentDataType(self.activated)
        if parent_type and parent_type == TreeItemDataType.Array:
            show_key = False
            
        dlg = EditJSONTreeItemDiaglogueWindow(frame, showKey=show_key, values=current_values)
        if dlg.ShowModal() == wx.ID_OK:
            new_values = dlg.GetDialogueValues()
            self.SetRowText(self.activated, new_values)
            if not show_key:
                self.UpdateArrayItemChildrenIndex(parent)

    def UpdateArrayItemChildrenIndex(self, item):
        index = 0
        if item and self.GetItemData(item) == TreeItemDataType.Array:
            current = self.GetFirstChild(item)
            while current:
                self.SetItemText(current, text=str(index))
                current = self.GetNextSibling(current)
                index += 1



    def GetValuesFromRow(self, item):

        values = None
        if item:
            key = self.GetItemText(item)
            value_type = self.GetItemData(item)
            value = self.GetItemText(item, 1)
            if not value_type or type(value_type) is not int:
                value_type = TreeItemDataType.String
            values = (key, value_type, value)
        return values

    def GetParentDataType(self, item):
        
        parent = self.GetItemParent(self.activated)
        parent_data_type = None
        if parent:
            parent_data_type = self.GetItemData(parent)
        
        return parent_data_type

    def SetRowText(self, item, values, override_key=None):
        """
        Populate values gathered from edit item dialogue
        """
        if item and values and len(values) == 3:
            key = values[0]
            type = values[1]
            value = values[2]
            if key == None:
                key = ""

            if override_key:
                self.SetItemText(item, str(override_key))
            else:
                self.SetItemText(item, str(key))
            self.SetItemText(item, 1, value)
            self.SetItemData(item, type)

    def OnDeleteItem(self):

        if self.activated and self.activated != self.GetRootItem():
            parent = self.GetItemParent(self.activated)
            self.DeleteItem(self.activated)
            self.UpdateArrayItemChildrenIndex(parent)
    
    def OnAppendChild(self):

        if self.activated:
            data_type = self.GetItemData(self.activated)

            if (data_type and (data_type == TreeItemDataType.Object or data_type == TreeItemDataType.Array)) or self.GetRootItem() == self.activated:

                show_key = not data_type == TreeItemDataType.Array


                dlg = EditJSONTreeItemDiaglogueWindow(frame, show_key)
                if dlg.ShowModal() == wx.ID_OK:
                    new_values = dlg.GetDialogueValues()
                    
                    new_item = self.AppendItem(self.activated, "")
                    self.SetRowText(new_item, new_values)
                    if not show_key:
                        self.UpdateArrayItemChildrenIndex(self.activated)

                    self.Expand(self.activated)
                    self.Select(new_item)
            else:
                dlg = wx.MessageDialog(self, 'Cannot append children on non Object or Array Types', 'Cannot append children')
                dlg.ShowModal()


    def OnInsert(self):
        if self.activated and self.activated != self.GetRootItem():
            parent_data_type = self.GetParentDataType(self.activated)
            show_key = not(parent_data_type and parent_data_type == TreeItemDataType.Array)
            
            dlg = EditJSONTreeItemDiaglogueWindow(frame, show_key)
            if dlg.ShowModal() == wx.ID_OK:
                new_values = dlg.GetDialogueValues()

                parent = self.GetRootItem()
                if self.activated:
                    parent = self.GetItemParent(self.activated)
                    new_item = self.InsertItem(parent, self.activated, "")

                    self.SetRowText(new_item, new_values)
                    if not show_key:
                        self.UpdateArrayItemChildrenIndex(parent)
                    self.Select(new_item)

                

# class MyFrame(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent, -1, "Test")
#         panel = wx.Panel(self)


#         self.tree = JSONTreeView(panel)

#         sizer = wx.BoxSizer(wx.VERTICAL)
 
#         sizer.Add(self.tree, 1, wx.EXPAND)
#         panel.SetSizer(sizer)

#         file = open('sample.json')
#         data = json.load(file)
#         print(data)
#         self.tree.UpdateTreeViewFromJSONData(data)






# if __name__ == '__main__':
#     app = wx.App(False)
#     frame = MyFrame(None)
#     frame.Show()

#     app.MainLoop()

