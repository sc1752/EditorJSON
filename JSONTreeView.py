import wx
import wx.dataview as DV
import re
import copy
import util

class TreeItemDataType():
    """ Pseudo data type enum """
    Null = 0
    String = 1
    Number = 2
    Object = 3
    Array = 4
    Boolean = 5

    def GetTypeIndex(data):
        """ Functions to rerturns Data type Emnum """
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

class TreeListItemNotSelectedException(Exception):
    """ Exception raised when missing user selection """
    pass

class IllegalParentException(Exception):
    """ Exception raised append child action is attempted on a non object or list types """
    pass
                
class EditJSONTreeItemDiaglogueWindow(wx.Dialog):
    """
    Helper TreeListItem editor Dialogue window provide user input for JSON key, value 
    type and value. 
    """
    def __init__(self, parent, showKey=True, enableType=True, values=None, title="Edit Json Object"):
        wx.Dialog.__init__(self, parent, title=title)
        self.v_box = wx.BoxSizer(wx.VERTICAL)

        self.ValueTypedLabel = wx.StaticText(self, label="Value Type")
        self.ValueTypeSelect = wx.Choice(self, choices=['None', 'String', 'Number', 'Object', 'Array', 'Boolean'])
        self.ValueTypeSelect.SetSelection(TreeItemDataType.String)
        if values and values[1]:
            self.ValueTypeSelect.SetSelection(values[1])   

        self.ValueTypeSelect.Bind(wx.EVT_CHOICE, self.OnValueTypeChanged)
        if not enableType:
            self.ValueTypeSelect.Disable()

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
            if not re.match(r'^true|false|True|False|t|f|T|F$', self.ValueInputField.GetValue()):
                isValid = False
        
        if not isValid:
            self.ValueInputField.SetBackgroundColour(colour=wx.RED)
        else:
            self.ValueInputField.SetBackgroundColour(colour=wx.WHITE)

        return isValid
    
    def GetDialogueValues(self):
        """
        return user input values in the form or a key value pair (key, value)
        """
        selection = self.ValueTypeSelect.GetSelection()
        
        key = self.KeyInputField.GetValue()

        value = self.ValueInputField.GetValue()
        if selection == TreeItemDataType.Array:
            value = []
        elif selection == TreeItemDataType.Object:
            value = {}
        elif selection == TreeItemDataType.Null:
            value = None
        elif selection == TreeItemDataType.Boolean:
            value = value.lower() in ['true' , 't']
        elif selection == TreeItemDataType.Boolean:
            value = util.to_number(value)

        return (key, value)


class JSONTreeView(DV.TreeListCtrl):

    def __init__(self, parent):
        """ JSONTreeView constructor """
        DV.TreeListCtrl.__init__(self, parent, style=DV.TL_NO_HEADER|DV.TL_SINGLE)
        self.GetDataView().SetWindowStyle(DV.DV_VERT_RULES|DV.DV_HORIZ_RULES)
        self.Bind(DV.EVT_TREELIST_SELECTION_CHANGED, self.OnSelected)
        self.Bind(DV.EVT_TREELIST_ITEM_ACTIVATED, self.OnActivated)
        self.Bind(DV.EVT_TREELIST_ITEM_CONTEXT_MENU, self.OnActivated)
        self.AppendColumn("Key")
        self.AppendColumn("Value")
        self.activated = None

    def UpdateTreeViewFromJSONData(self, JSON_Object={}):
        """
        Update the entire tree view with decoded JSON data
        """
        self.DeleteAllItems()
        tree_parent = self.GetRootItem()
        self.BuildTreeViewFromJSONDataRecursively(JSON_Object, tree_parent)
        self.ExpandFirstLevelNodes()

    def BuildTreeViewFromJSONDataRecursively(self, JSON_Object, tree_parent):
        """
        A recursive function that traverse JSON dictionary data and build 
        TreeListView items recursively. 
        """
        if tree_parent:
            JSONparent = JSON_Object
            if type(JSON_Object) == dict:
                if tree_parent != self.GetRootItem():
                    key = self.GetItemText(tree_parent)
                    self.SetRow(tree_parent, key, JSON_Object)
                for key in JSON_Object:
                    tree_item = self.AppendItem(tree_parent, key)
                    
                    value = JSONparent[key]
                    self.BuildTreeViewFromJSONDataRecursively(value, tree_item)
            elif type(JSON_Object) == list:
                key = self.GetItemText(tree_parent)
                self.SetRow(tree_parent,  key, JSON_Object)
                for array_item in JSON_Object:
                    array_tree_item = self.AppendItem(tree_parent, "")
                    self.BuildTreeViewFromJSONDataRecursively(array_item, array_tree_item)
                self.UpdateArrayItemChildrenIndex(tree_parent)
            else: #End of chain
                key = self.GetItemText(tree_parent)
                self.SetRow(tree_parent, key, JSON_Object)


    def GenerateJSONData(self):
        """
        Generate JSON data from the values in 
        """
        JSON_root = {}
        tree_root = self.GetRootItem()
        self.GenerateJSONDataReCursively(tree_root, JSON_root)
        return JSON_root

    def GenerateJSONDataReCursively(self, tree_item_parent, JSON_root):
        """
        Traversing data stored in TreeListCtrl
        """
        parent = self.GetItemData(tree_item_parent)
        current = self.GetFirstChild(tree_item_parent)

        while current:
            current_key = self.GetItemText(current)
            current_value = copy.deepcopy(self.GetItemData(current))

            if TreeItemDataType.GetTypeIndex(current_value) == TreeItemDataType.Object:
                # depth first 
                if TreeItemDataType.GetTypeIndex(JSON_root) == TreeItemDataType.Array:
                    JSON_root.append(self.GenerateJSONDataReCursively(current, current_value))
                else:
                    JSON_root[current_key] = {}
                    JSON_root[current_key] = self.GenerateJSONDataReCursively(current, JSON_root[current_key])
            elif TreeItemDataType.GetTypeIndex(current_value) == TreeItemDataType.Array:
                # breadth first
                if TreeItemDataType.GetTypeIndex(JSON_root) == TreeItemDataType.Array:
                    JSON_root.append(self.GenerateJSONDataReCursively(current, current_value))
                else:
                    JSON_root[current_key] = []
                    current_array_item = self.GetFirstChild(current)
                    while current_array_item:
                        array_value = copy.deepcopy(self.GetItemData(current_array_item))
                        JSON_root[current_key].append(self.GenerateJSONDataReCursively(current_array_item, array_value))
                        current_array_item = self.GetNextSibling(current_array_item)
            else:
                if TreeItemDataType.GetTypeIndex(JSON_root) == TreeItemDataType.Array:
                    JSON_root.append(current_value)
                else:
                    JSON_root[current_key] = current_value

            current = self.GetNextSibling(current)

        return JSON_root

    def OnSelected(self, event):
        self.activated = event.GetItem()

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
        try:
            if ID == 1:
                self.OnEditItem(event)
            elif ID == 2:
                self.OnDeleteItem(event)
            elif ID == 3:
                self.OnAppendChild(event)
            elif ID == 4:
                self.OnInsert(event)
        except TreeListItemNotSelectedException:
            dlg = wx.MessageDialog(self, "Please select an item (row) to process.")
            dlg.ShowModal()
        except IllegalParentException:
            dlg = wx.MessageDialog(self, "Cannot append children on non Object or Array Types")
            dlg.ShowModal()

    def OnEditItem(self, event):

        if not self.activated or self.activated == self.GetRootItem():
            raise TreeListItemNotSelectedException

        current_values = self.GetValuesFromRow(self.activated)

        show_key = True
        enable_type_sel = True
        name_to_show = self.GetItemText(self.activated)

        parent = self.GetItemParent(self.activated)
        parent_type = self.GetParentDataType(self.activated)
        if parent_type == TreeItemDataType.Array:
            show_key = False

        if self.ItemIsParent(self.activated):
            enable_type_sel = False

        dlg = EditJSONTreeItemDiaglogueWindow(self, showKey=show_key, values=current_values, enableType=enable_type_sel, title="Edit %s" % name_to_show)
        if dlg.ShowModal() == wx.ID_OK:
            (key, value) = dlg.GetDialogueValues()
            self.SetRow(self.activated, key, value)
            if not show_key:
                self.UpdateArrayItemChildrenIndex(parent)

    def UpdateArrayItemChildrenIndex(self, item):
        index = 0
        if item and TreeItemDataType.GetTypeIndex(self.GetItemData(item)) == TreeItemDataType.Array:
            current = self.GetFirstChild(item)
            while current:
                self.SetItemText(current, text=str(index))
                current = self.GetNextSibling(current)
                index += 1

    def ItemIsParent(self, item):
        """ Returns true if speicifed tree item is a parent """
        has_child = False
        if item:
            child = self.GetFirstChild(item)
            if child:
                has_child = True

        return has_child

    def GetValuesFromRow(self, item):
        """
        Extract values from row returns 3-tupple pair (key, value type, value)
        """
        values = None
        if item:
            key = self.GetItemText(item)
            value = self.GetItemData(item)
            value_type = TreeItemDataType.GetTypeIndex(value)

            if not value_type or type(value_type) is not int:
                value_type = TreeItemDataType.String
            values = (key, value_type, value)
        return values

    def GetParentDataType(self, item):
        
        parent = self.GetItemParent(self.activated)
        parent_data_type = None
        if parent:
            parent_data_type = TreeItemDataType.GetTypeIndex(self.GetItemData(parent))
        
        return parent_data_type

    def SetRow(self, item, key, value, override_key=None):
        """
        Set item text as well as item data to specific TreeListCtrlItem
        """
        if item:
            if key == None:
                key = ""

            if override_key:
                self.SetItemText(item, str(override_key))
            else:
                self.SetItemText(item, str(key))

            value_text = str(value)
            if TreeItemDataType.GetTypeIndex(value) == TreeItemDataType.Array:
                value = []
                value_text = r'[]'
            elif TreeItemDataType.GetTypeIndex(value) == TreeItemDataType.Object:
                value = {}
                value_text = r'{}'
            self.SetItemText(item, 1, value_text)
            self.SetItemData(item, value)


    def OnDeleteItem(self, event):

        if not self.activated or self.activated == self.GetRootItem():
            raise TreeListItemNotSelectedException

        parent = self.GetItemParent(self.activated)
        self.DeleteItem(self.activated)
        self.UpdateArrayItemChildrenIndex(parent)
        
    
    def GetSelectedItemKey(self):
        """ Return the printable name of the selected item, returns "Root Item" if nothing is selected."""
        if self.activated:
            if self.activated == self.GetRootItem():
                return "Root Item"
            else:
                return self.GetItemText(self.activated)

    def OnAppendChild(self, event):

        if not self.activated:
            self.activated = self.GetRootItem()

        if self.activated:
            data_type = TreeItemDataType.GetTypeIndex(self.GetItemData(self.activated))

            if (data_type and (data_type == TreeItemDataType.Object or data_type == TreeItemDataType.Array)) or self.activated == self.GetRootItem():

                show_key = not data_type == TreeItemDataType.Array

                name_to_show = self.GetSelectedItemKey()
                dlg = EditJSONTreeItemDiaglogueWindow(self, show_key, title="Insert new child item for %s" % name_to_show)
                if dlg.ShowModal() == wx.ID_OK:
                    (key, value) = dlg.GetDialogueValues()

                    new_item = self.AppendItem(self.activated, "")
                    self.SetRow(new_item, key, value)
                    if not show_key:
                        self.UpdateArrayItemChildrenIndex(self.activated)

                    self.Expand(self.activated)
                    self.Select(new_item)
            else:
                raise IllegalParentException



    def OnInsert(self, event):

        if self.activated and self.activated != self.GetRootItem():
            parent_data_type = self.GetParentDataType(self.activated)
            show_key = not(parent_data_type and parent_data_type == TreeItemDataType.Array)
            
            item_name = self.GetSelectedItemKey()
            dlg = EditJSONTreeItemDiaglogueWindow(self, show_key, title="Insert sibling under %s" % item_name)
            if dlg.ShowModal() == wx.ID_OK:
                (key, value) = dlg.GetDialogueValues()

                parent = self.GetRootItem()
                if self.activated:
                    parent = self.GetItemParent(self.activated)
                    new_item = self.InsertItem(parent, self.activated, "")

                    self.SetRow(new_item, key, value)
                    if not show_key:
                        self.UpdateArrayItemChildrenIndex(parent)
                    self.Select(new_item)
        else:
            # If no items is selected, append to the root item
            try:
                self.OnAppendChild(self.GetRootItem())
            except IllegalParentException as error:
                raise error


    def ExpandFirstLevelNodes(self):
        """Function to expand children of the root item for presentation"""
        root_item = self.GetRootItem()
        child = self.GetFirstChild(root_item)
        while child:
            self.Expand(child)
            child = self.GetNextSibling(child)


    def ExpandRecursively(self, item):
        """ Expand the entire tree list recursively """
        if item:
            child = self.GetFirstChild(item)
            while child:
                self.Expand(item)
                self.ExpandRecursively(child)
                child = self.GetNextSibling(child)


    def CollapseRecursively(self, item):
        """ Collapse the entire tree list recursively """
        if item:
            child = self.GetFirstChild(item)
            while child:
                self.Collapse(item)
                self.CollapseRecursively(child)
                child = self.GetNextSibling(child)


    def OnExpandAll(self, event):
        """Function to expand children of the root item for presentation"""
        root_item = self.GetRootItem()
        self.ExpandRecursively(root_item)

    def OnCollapseAll(self, event):
        """Function to expand children of the root item for presentation"""
        root_item = self.GetRootItem()
        self.CollapseRecursively(root_item)
