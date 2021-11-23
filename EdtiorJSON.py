import JSONTreeView as TreeView
import JSONTextView as TextView
from JSONDataModel import JSONDataModel
from json.decoder import JSONDecodeError
from pathlib import Path
import os
import wx
import sys


# PyInstaller workaround
def resource_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    return os.path.join(os.path.abspath("."))

app_dir_root = resource_path()

class TabTextView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.control_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_undo.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_undo = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_undo.ToolTip = "Undo"
    
        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_redo.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_redo = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_redo.ToolTip = "Redo"

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_formatted.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_pretty_format = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_pretty_format.ToolTip = "Pretty Formating"

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_compact.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_compact_format = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_compact_format.ToolTip = "Compact Formating"

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_search.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_search = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_search.ToolTip = "Search"

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_validate.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_validate = wx.BitmapToggleButton(self, label=bitmap, size=(30,30))
        self.btn_validate.ToolTip = "Toggle on/off live JSON format checking"

        self.control_panel_sizer.Add(self.btn_undo)
        self.control_panel_sizer.Add(self.btn_redo)
        self.control_panel_sizer.Add(self.btn_pretty_format)
        self.control_panel_sizer.Add(self.btn_compact_format)
        self.control_panel_sizer.Add(self.btn_search)
        self.control_panel_sizer.Add(self.btn_validate)

        self.editor = TextView.JSONTextView(self)

        self.main_sizer.Add(self.control_panel_sizer, 0, wx.ALL, 2)
        self.main_sizer.Add(self.editor, 1, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM, 2)
        self.SetSizer(self.main_sizer)

        # Bind button functions
        self.btn_undo.Bind(wx.EVT_BUTTON, self.editor.OnUndo)
        self.btn_redo.Bind(wx.EVT_BUTTON, self.editor.OnRedo)



class TabTreeView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.control_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_expand.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_expand_all = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_expand_all.ToolTip = "Expand All"

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_collaspe.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_collapse_all = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_collapse_all.ToolTip = "Collapse All"

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_edit.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_edit = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_edit.ToolTip = "Edit Item"

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_delete.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_delete = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_delete.ToolTip = "Delete Item"

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_insert.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_insert = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_insert.ToolTip = "Insert new entry"

        bitmap = wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_addchild.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_append = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_append.ToolTip = "Add child"

        self.control_panel_sizer.Add(self.btn_expand_all)
        self.control_panel_sizer.Add(self.btn_collapse_all)
        self.control_panel_sizer.Add(self.btn_edit)
        self.control_panel_sizer.Add(self.btn_insert)
        self.control_panel_sizer.Add(self.btn_append)
        self.control_panel_sizer.Add(self.btn_delete)

        self.tree = TreeView.JSONTreeView(self)

        self.main_sizer.Add(self.control_panel_sizer, 0, wx.ALL, 2)
        self.main_sizer.Add(self.tree, 1, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM, 2)

        self.SetSizer(self.main_sizer)

        # Bind functions to button
        self.btn_expand_all.Bind(wx.EVT_BUTTON, self.tree.OnExpandAll)
        self.btn_collapse_all.Bind(wx.EVT_BUTTON, self.tree.OnCollapseAll)
        self.btn_edit.Bind(wx.EVT_BUTTON, self.OnEditTreeItem)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.OnDeleteTreeItem)
        self.btn_insert.Bind(wx.EVT_BUTTON, self.tree.OnInsert)
        self.btn_append.Bind(wx.EVT_BUTTON, self.OnAppendChild)

    def OnEditTreeItem(self, event):
        """ Edit item handler """
        try:
            self.tree.OnEditItem(event)
        except TreeView.TreeListItemNotSelectedException:
            dlg = wx.MessageDialog(self, "Please select an item (row) to edit.")
            dlg.ShowModal()

    def OnDeleteTreeItem(self, event):
        """ Delete item handler """
        try:
            self.tree.OnDeleteItem(event)
        except TreeView.TreeListItemNotSelectedException:
            dlg = wx.MessageDialog(self, "Please select an item (row) to delete.")
            dlg.ShowModal()

    def OnAppendChild(self, event):
        try:
            self.tree.OnAppendChild(event)
        except TreeView.IllegalParentException:
            dlg = wx.MessageDialog(self, "Cannot append children on non Object or Array Types")
            dlg.ShowModal()


class EditorJSON(wx.Frame):
    def __init__(self, parent, title, data : JSONDataModel):
        wx.Frame.__init__(self, parent, title=title)

        self.JSONData = data

        self.SetSize(800, 600)
        self.SetUpMenuBar()

        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Tree, Text Editor Area
        main_panel = wx.Panel(self)
        self.tabs_panel = wx.Notebook(main_panel, size=(800,600), style=wx.NB_NOPAGETHEME)

        self.tree_tab = TabTreeView(self.tabs_panel)
        self.tree = self.tree_tab.tree
        self.editor_tab = TabTextView(self.tabs_panel)
        self.editor = self.editor_tab.editor
        self.editor.BindTextModifiedHandler(self.OnJSONTextModified)

        # Assemble pages
        self.tabs_panel.AddPage(self.editor_tab, "Editor View")
        self.tabs_panel.AddPage(self.tree_tab, "Tree View")
        self.tabs_panel.SetPadding(wx.Size(10, 10))
        self.tabs_panel.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.ToggleEditingMode)
        self.tabs_panel.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.UpdateToggleEditingStatus)
        self.tree_edit_mode = False

        # Setup Icons in tabs
        image_list = wx.ImageList(25, 25)
        icon_editor = image_list.Add(wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_json.png"), wx.BITMAP_TYPE_PNG))
        icon_treev = image_list.Add(wx.Bitmap(os.path.join(app_dir_root, "icon", "btn_treeview.png"), wx.BITMAP_TYPE_PNG))
        self.tabs_panel.AssignImageList(image_list)
        self.tabs_panel.SetPageImage(0, icon_editor)
        self.tabs_panel.SetPageImage(1, icon_treev)

        self.status_bar = self.CreateStatusBar()

        main_sizer.Add(self.tabs_panel, 1, wx.EXPAND)

        main_panel.SetSizer(main_sizer)
        main_panel.Fit()
        
        self.last_directory = None
        self.current_document_path = None
        self.is_document_modified = False
        self.live_json_validation_on = False

        # Bind text editor buttons
        self.editor_tab.btn_pretty_format.Bind(wx.EVT_BUTTON, self.OnPrettify)
        self.editor_tab.btn_compact_format.Bind(wx.EVT_BUTTON, self.OnCompactify)
        self.editor_tab.btn_validate.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleValidateContinously)
        self.editor_tab.btn_search.Bind(wx.EVT_BUTTON, self.editor.OnSearch)

        self.OnInit()


    def SetUpMenuBar(self):
        self.menu = wx.MenuBar()
        file_menu = wx.Menu()
        file_item = wx.MenuItem(file_menu, wx.ID_NEW, text="New", helpString="Create new JSON file")
        accelerator_entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('N'), wx.ID_NEW)
        file_item.SetAccel(accelerator_entry)
        file_menu.AppendSeparator()
        file_menu.Append(file_item)
        
        file_item = wx.MenuItem(file_menu, wx.ID_OPEN, text="Open", helpString="Open existing JSON file")
        accelerator_entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('O'), wx.ID_OPEN)
        file_item.SetAccel(accelerator_entry)
        file_menu.Append(file_item)
        file_menu.AppendSeparator()

        file_item = wx.MenuItem(file_menu, wx.ID_SAVE, text = "Save", helpString="Save current JSON file")
        accelerator_entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE)
        file_item.SetAccel(accelerator_entry)
        file_menu.Append(file_item)

        file_item = wx.MenuItem(file_menu, wx.ID_SAVEAS, text = "Save As", helpString="Save as current JSON file")
        accelerator_entry = wx.AcceleratorEntry(wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('S'), wx.ID_SAVEAS)
        file_item.SetAccel(accelerator_entry)
        file_menu.Append(file_item)
        file_menu.AppendSeparator()

        file_item = wx.MenuItem(file_menu, wx.ID_EXIT, text = "Exit", helpString="Exit tool")
        file_menu.Append(file_item)

        self.edit_menu = wx.Menu()
        edit_item = wx.MenuItem(file_menu, wx.ID_CUT, text="Cut", helpString="Cut")
        accelerator_entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('X'), wx.ID_CUT)
        edit_item.SetAccel(accelerator_entry)
        self.edit_menu.Append(edit_item)
        
        self.edit_menu.AppendSeparator()
        edit_item = wx.MenuItem(file_menu, wx.ID_COPY, text="Copy", helpString="Copy")
        accelerator_entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('C'), wx.ID_COPY)
        edit_item.SetAccel(accelerator_entry)
        self.edit_menu.Append(edit_item)

        edit_item = wx.MenuItem(file_menu, wx.ID_PASTE, text = "Paste", helpString="Paste")
        accelerator_entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('V'), wx.ID_PASTE)
        edit_item.SetAccel(accelerator_entry)
        self.edit_menu.Append(edit_item)

        self.edit_menu.AppendSeparator()
        edit_item = wx.MenuItem(file_menu, wx.ID_FIND, text = "Search", helpString="Search")
        accelerator_entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('F'), wx.ID_FIND)
        edit_item.SetAccel(accelerator_entry)
        self.edit_menu.Append(edit_item)
        

        help_menu = wx.Menu()
        help_item = wx.MenuItem(help_menu, wx.ID_HELP, text = "Help", helpString="About this application")
        help_menu.Append(help_item)
        help_menu.AppendSeparator()
        help_item = wx.MenuItem(help_menu, wx.ID_ABOUT, text = "About", helpString="About this application")
        help_menu.Append(help_item)

        self.menu.Append(file_menu, "File")
        self.menu.Append(self.edit_menu, "Edit")
        self.menu.Append(help_menu, "Help")
        self.SetMenuBar(self.menu)

        self.Bind(wx.EVT_MENU, self.MenuItemHandler)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnInit(self):
        self.OnNewFile()

    def ToggleEditingMode(self, event):
        """ Toggle handler to be switch between Text and Tree mode"""
        try:
            if not self.tree_edit_mode:
                self.JSONData.Text = self.editor.Text
                self.JSONData.SyncTextToData()
                self.tree.UpdateTreeViewFromJSONData(self.JSONData.JSONdata)
            else:
                treeData = self.tree.GenerateJSONData()
                if self.JSONData.JSONdata != treeData:
                    self.JSONData.JSONdata = self.tree.GenerateJSONData()
                    self.JSONData.SyncDataToText()
                    if self.editor.GetText() != self.JSONData.Text:
                        self.editor.SetText(self.JSONData.Text)
        except JSONDecodeError as e:
            event.Veto()
            self.JSONDecoderExceptionHandler(e, "Please fix JSON error before switching edit mode.\n")
        except Exception:
            event.Veto()
            dlg = wx.MessageDialog(self, "Please fix JSON error before switching edit mode", "JSON format error")
            dlg.ShowModal()


    def UpdateToggleEditingStatus(self, event):
        """ 
        Handler of EVT_NOTEBOOK_PAGE_CHANGED to ensure update 
        state only when EVT_NOTEBOOK_PAGE_CHANGGING was not vetoed.
        """
        self.tree_edit_mode = not self.tree_edit_mode
        if self.tree_edit_mode:
            self.ToggleEditMenu(False)
        else:
            self.ToggleEditMenu(True)


    def ToggleEditMenu(self, enable : bool):
        """Utility for enabling or greying out edit menu"""
        if self.edit_menu:
            self.edit_menu.Enable(wx.ID_CUT, enable)
            self.edit_menu.Enable(wx.ID_COPY, enable)
            self.edit_menu.Enable(wx.ID_PASTE, enable)
            self.edit_menu.Enable(wx.ID_FIND, enable)
        

    def JSONDecoderExceptionHandler(self, error: JSONDecodeError, msg : str, quiet = False):
        """
        Function will be called to respond to Text editor formating errors. 
        Sending line number and column number information to the editor highlight.
        """
        msg += str(error)
        self.editor.HighlightIndicateError(error.lineno, error.colno, error.pos)
        self.status_bar.PushStatusText(msg)
        if not quiet:
            dlg = wx.MessageDialog(self, msg, "JSON format error")
            dlg.ShowModal()

    def MenuItemHandler(self, event):
        id = event.GetId()
        if id == wx.ID_NEW:
            self.OnNewFile()
        elif id == wx.ID_OPEN:
            self.OnOpenFile()
        elif id == wx.ID_SAVE:
            self.OnPromptToSave()
        elif id == wx.ID_SAVEAS:
            self.OnPromptToSave(save_as=True)
        elif id == wx.ID_EXIT:
            self.Close()
        elif id == wx.ID_HELP:
            self.OnHelp()
        elif id == wx.ID_ABOUT:
            self.OnAbout()
        elif id == wx.ID_CUT:
            self.editor.Cut()
        elif id == wx.ID_COPY:
            self.editor.Copy()
        elif id == wx.ID_PASTE:
            self.editor.Paste()
        elif id == wx.ID_FIND:
            self.editor.OnSearch(None)
        
    def OnNewFile(self):
        if self.is_document_modified:
            dlg = wx.MessageDialog(self, "Do you want to save current document? ", style=wx.YES_NO)
            if dlg.ShowModal() == wx.ID_OK:
                self.OnPromptToSave(save_as=True)
            
        self.tree.DeleteAllItems()
        self.editor.ClearAll()
        try:
            self.JSONData.NewFile()
        except JSONDecodeError:
            dlg =wx.MessageDialog(self, "Unable to parse loaded JSON file.", "Error")
            dlg.ShowModal()

        self.editor.SetText(self.JSONData.Text)
        self.tree.UpdateTreeViewFromJSONData(self.JSONData.JSONdata)
        self.current_document_path = None
        self.is_document_modified = False

        self.UpdateWindowTitle()
    
    def GetDefaultDirectory(self):
        """Get recent directory or use home directory"""
        if self.last_directory and os.path.isdir(self.last_directory):
            return self.last_directory
        else:
            return str(Path.home())

    def OnOpenFile(self):
        """ Handle new open file"""
        if self.is_document_modified:
            dlg = wx.MessageDialog(self, "Do you want to save current document? ", style=wx.YES_NO)
            if dlg.ShowModal() == wx.ID_OK:
                self.OnPromptToSave()

        file_opened = False
        with wx.FileDialog(self, "Select JSON file to load", defaultDir=self.GetDefaultDirectory(), 
        wildcard='*.json', style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() != wx.ID_CANCEL:
                path = dlg.GetPath()
                try:
                    with open(path, 'r') as file:
                        self.JSONData.SetJSONText(file.read())
                        self.editor.SetText(self.JSONData.Text)
                        self.current_document_path = path
                        file_opened = True
                except Exception:
                    dlg = wx.MessageDialog(self, "Unable to open %s ." % path, "Error")
                    dlg.ShowModal()

                self.last_directory = os.path.dirname(path)

        if self.tree_edit_mode:
            try:
                self.JSONData.SyncTextToData()
                self.tree.UpdateTreeViewFromJSONData(self.JSONData.JSONdata)
            except JSONDecodeError:
                dlg =wx.MessageDialog(self, "Unable to parse loaded JSON file.", "Error")
                dlg.ShowModal()
        
        if file_opened:
            self.is_document_modified = False
            self.UpdateWindowTitle()
        

    def OnPromptToSave(self, save_as=False):
        """Prompt a save file diaglogue to user."""
        if not save_as and self.current_document_path and os.path.isfile(self.current_document_path):
            try:
                self.SaveFile(self.current_document_path)
            except Exception:
                dlg = wx.MessageDialog(self, "Unable to save %s ." % self.current_document_path)
                dlg.ShowModal()
            return

        with wx.FileDialog(self, "Select Save Location", defaultDir=self.GetDefaultDirectory(), 
        wildcard='*.json', style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() != wx.ID_CANCEL:
                path = dlg.GetPath()
                try:
                    self.SaveFile(path)
                
                except Exception:
                    dlg = wx.MessageDialog(self, "Unable to save file at %s ." % path)
                    dlg.ShowModal()

                self.last_directory = os.path.dirname(path)

    def SaveFile(self, path):
        try:
            with open(path, 'w') as file:
                if self.tree_edit_mode:
                    self.JSONData.SyncDataToText()
                else:
                    self.JSONData.SetJSONText(self.editor.GetText())

                file.write(self.JSONData.Text)
                self.is_document_modified = False
                self.current_document_path = path
                self.UpdateWindowTitle()

        except Exception as error:
            raise error

    def OnPrettify(self, event):

        try:
            self.JSONData.Text = self.editor.GetText()
            self.JSONData.PrettifyText()
            self.editor.Text = self.JSONData.Text
        except JSONDecodeError as error:
            self.JSONDecoderExceptionHandler(error, "Unable to format JSON due to format error.\n")

    def OnCompactify(self, event):

        try:
            self.JSONData.Text = self.editor.GetText()
            self.JSONData.CompactifyText()
            self.editor.Text = self.JSONData.Text
        except JSONDecodeError as error:
            self.JSONDecoderExceptionHandler(error, "Unable to compact JSON due to format error\n")

    def OnValidateText(self, event, quiet=False):
        try:
            self.JSONData.Text = self.editor.GetText()
            self.JSONData.ValidateJSONText()
            self.editor.ClearAllIndicators()

            if not quiet:
                dlg = wx.MessageDialog(self, "JSON is valid!")
                dlg.ShowModal() 
            self.status_bar.SetStatusText("")
        except JSONDecodeError as error:
            self.JSONDecoderExceptionHandler(error, "Validation Failed: \n", quiet)
        

    def OnToggleValidateContinously(self, event):
        """ Hanldes event when turning JSON format checker on or off """
        self.live_json_validation_on = event.IsChecked()
        if self.live_json_validation_on:
            self.OnValidateText(None, quiet=True)
            self.status_bar.SetStatusText("JSON checker ON")
        else:
            self.status_bar.SetStatusText("")
            self.editor.ClearAllIndicators()


    def OnJSONTextModified(self, event):
        """ Handling editor text modifed event """
        if not self.is_document_modified:
            self.is_document_modified = True
            self.UpdateWindowTitle()

        if self.live_json_validation_on:
            self.OnValidateText(None, quiet=True)


    def UpdateWindowTitle(self):
        title = "Editor JSON"
        if self.current_document_path:
            title = title + " - " + os.path.basename(self.current_document_path)
        else:
            title =  title + " - " + "Untitled JSON"
        if self.is_document_modified:
            title += "*"
        
        self.SetTitle(title)

    def OnClose(self, event):
        """ Handle application cloes event. This prompt user to save current document or not. """
        if self.is_document_modified:
            dlg = wx.MessageDialog(self, "Do you want to save current document? ", style=wx.YES|wx.NO|wx.CANCEL)
            id = dlg.ShowModal()
            if id == wx.ID_YES:
                self.OnPromptToSave(save_as=True)
            elif id == wx.ID_CANCEL:
                event.Veto()
                return
            
        self.Destroy() 
    
    def OnHelp(self):
        wx.LaunchDefaultBrowser("https://github.com/sc1752/EditorJSON/wiki")
    
    def OnAbout(self):
        dlg = wx.MessageDialog(self, "Author: c. shu", "About")
        dlg.ShowModal()

class MyApp(wx.App):
    def OnInit(self):
        self.data = JSONDataModel()
        self.frame = EditorJSON(None, "Editor JSON", self.data)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
