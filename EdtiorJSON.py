import JSONTreeView as TreeView
import JSONTextView as TextView
from JSONDataModel import JSONDataModel
from json.decoder import JSONDecodeError
from pathlib import Path
import os
import wx
import time


class TabTextView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.control_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        bitmap = wx.Bitmap(os.path.join("icon", "btn_undo.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_undo = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_undo.ToolTip = "Undo"
    
        bitmap = wx.Bitmap(os.path.join("icon", "btn_redo.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_redo = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_redo.ToolTip = "Redo"

        bitmap = wx.Bitmap(os.path.join("icon", "btn_formatted.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_pretty_format = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_pretty_format.ToolTip = "Pretty Formating"

        bitmap = wx.Bitmap(os.path.join("icon", "btn_compact.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_compact_format = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_compact_format.ToolTip = "Compact Formating"

        bitmap = wx.Bitmap(os.path.join("icon", "btn_validate.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_validate = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_validate.ToolTip = "Validate"

        self.control_panel_sizer.Add(self.btn_undo)
        self.control_panel_sizer.Add(self.btn_redo)
        self.control_panel_sizer.Add(self.btn_pretty_format)
        self.control_panel_sizer.Add(self.btn_compact_format)
        self.control_panel_sizer.Add(self.btn_validate)

        self.editor = TextView.JSONTextView(self)

        self.main_sizer.Add(self.control_panel_sizer, 0, wx.ALL, 2)
        self.main_sizer.Add(self.editor, 1, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM, 2)
        self.SetSizer(self.main_sizer)

        # Bind button functions
        self.btn_undo.Bind(wx.EVT_BUTTON, self.editor.OnUndo)
        self.btn_redo.Bind(wx.EVT_BUTTON, self.editor.OnUndo)



class TabTreeView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.control_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        bitmap = wx.Bitmap(os.path.join("icon", "btn_expand.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_expand_all = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_expand_all.ToolTip = "Expand"

        bitmap = wx.Bitmap(os.path.join("icon", "btn_collaspe.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_collapse_all = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_collapse_all.ToolTip = "Collapse"

        bitmap = wx.Bitmap(os.path.join("icon", "btn_edit.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_edit = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_edit.ToolTip = "Collapse"

        bitmap = wx.Bitmap(os.path.join("icon", "btn_delete.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_delete = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_delete.ToolTip = "Collapse"

        bitmap = wx.Bitmap(os.path.join("icon", "btn_insert.png"), type=wx.BITMAP_TYPE_PNG)
        self.btn_insert = wx.BitmapButton(self, bitmap=bitmap, size=(30,30))
        self.btn_insert.ToolTip = "Insert new entry"

        bitmap = wx.Bitmap(os.path.join("icon", "btn_addchild.png"), type=wx.BITMAP_TYPE_PNG)
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
        self.btn_edit.Bind(wx.EVT_BUTTON, self.tree.OnEditItem)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.tree.OnDeleteItem)
        self.btn_insert.Bind(wx.EVT_BUTTON, self.tree.OnInsert)
        self.btn_append.Bind(wx.EVT_BUTTON, self.tree.OnAppendChild)

class EditorJSON(wx.Frame):
    def __init__(self, parent, title, data : JSONDataModel):
        wx.Frame.__init__(self, parent, title=title)

        self.JSONData = data

        self.SetSize(600, 800)
        self.SetUpMenuBar()

        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Tree, Text Editor Area
        main_panel = wx.Panel(self)
        self.tabs_panel = wx.Notebook(main_panel, size=(600,800), style=wx.NB_NOPAGETHEME)

        self.tree_tab = TabTreeView(self.tabs_panel)
        self.tree = self.tree_tab.tree
        self.editor_tab = TabTextView(self.tabs_panel)
        self.editor = self.editor_tab.editor

        # Assemble pages
        self.tabs_panel.AddPage(self.editor_tab, "Editor View")
        self.tabs_panel.AddPage(self.tree_tab, "Tree View")
        self.tabs_panel.SetPadding(wx.Size(10, 10))
        self.tabs_panel.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.ToggleEditingMode)
        self.tree_edit_mode = False

        # Setup Icons in tabs
        image_list = wx.ImageList(25, 25)
        icon_editor = image_list.Add(wx.Bitmap(os.path.join("icon", "btn_json.png"), wx.BITMAP_TYPE_PNG))
        icon_treev = image_list.Add(wx.Bitmap(os.path.join("icon", "btn_treeview.png"), wx.BITMAP_TYPE_PNG))
        self.tabs_panel.AssignImageList(image_list)
        self.tabs_panel.SetPageImage(0, icon_editor)
        self.tabs_panel.SetPageImage(1, icon_treev)


        main_sizer.Add(self.tabs_panel, 1, wx.EXPAND)

        main_panel.SetSizer(main_sizer)
        main_panel.Fit()
        
        self.last_directory = None
        self.current_document_path = None
        self.last_modified_time = time.time()
        self.last_saved_time = time.time()

        # Bind text editor buttons
        self.editor_tab.btn_pretty_format.Bind(wx.EVT_BUTTON, self.OnPrettify)
        self.editor_tab.btn_compact_format.Bind(wx.EVT_BUTTON, self.OnCompactify)
        self.editor_tab.btn_validate.Bind(wx.EVT_BUTTON, self.OnValidateText)

        self.OnInit()

    def IsDocumentSaved(self):
        return self.last_modified_time >= self.last_saved_time

    def SetUpMenuBar(self):
        self.menu = wx.MenuBar()
        file_menu = wx.Menu()
        file_item = wx.MenuItem(file_menu, wx.ID_NEW, text="New", helpString="Create new JSON file")
        file_menu.Append(file_item)
        file_item = wx.MenuItem(file_menu, wx.ID_OPEN, text="Open", helpString="Open existing JSON file")
        file_menu.Append(file_item)
        file_item = wx.MenuItem(file_menu, wx.ID_SAVE, text = "Save", helpString="Save current JSON file")
        file_menu.Append(file_item)
        file_item = wx.MenuItem(file_menu, wx.ID_SAVEAS, text = "Save As", helpString="Save as current JSON file")
        file_menu.Append(file_item)
        file_item = wx.MenuItem(file_menu, wx.ID_EXIT, text = "Exit", helpString="Exit tool")
        file_menu.Append(file_item)

        #If time allowed adding edit feature

        help_menu = wx.Menu()
        help_item = wx.MenuItem(help_menu, wx.ID_HELP, text = "Help", helpString="About this application")
        help_menu.Append(help_item)
        help_item = wx.MenuItem(help_menu, wx.ID_ABOUT, text = "About", helpString="About this application")
        help_menu.Append(help_item)

        self.menu.Append(file_menu, "File")
        self.menu.Append(help_menu, "Help")
        self.SetMenuBar(self.menu)
        self.Bind(wx.EVT_MENU, self.MenuItemHandler)

    def OnInit(self):
        self.OnNewFile()

    def ToggleEditingMode(self, event):
        self.tree_edit_mode = not self.tree_edit_mode
        try:
            if self.tree_edit_mode:
                print('to tree')
                self.JSONData.Text = self.editor.Text
                self.JSONData.SyncTextToData()
                self.tree.UpdateTreeViewFromJSONData(self.JSONData.JSONdata)
            else:
                print('to editor')
                self.JSONData.JSONdata = self.tree.GenerateJSONData()
                self.JSONData.SyncDataToText()
                self.editor.SetText(self.JSONData.Text)
        except Exception as e:
            #TODO handle decoder exception
            event.Veto()
            wx.MessageDialog(self, str(e), "Error")


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
        
    def OnNewFile(self):
        if not self.IsDocumentSaved():
            self.OnPromptToSave()
        self.tree.DeleteAllItems()
        self.editor.ClearAll()
        self.JSONData.NewFile()
        self.editor.SetText(self.JSONData.Text)
        self.tree.UpdateTreeViewFromJSONData(self.JSONData.JSONdata)
        self.current_document_path = None
        self.last_saved_time = time.time()
    
    def GetDefaultDirectory(self):
        """Get recent directory or use home directory"""
        if self.last_directory and os.path.isdir(self.last_directory):
            return self.last_directory
        else:
            return str(Path.home())

    def OnOpenFile(self):
        
        with wx.FileDialog(self, "Select JSON file to load", defaultDir=self.GetDefaultDirectory(), 
        wildcard='*.json', style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() != wx.ID_CANCEL:
                path = dlg.GetPath()
                try:
                    with open(path, 'r') as file:
                        self.JSONData.SetJSONText(file.read())
                        self.editor.SetText(self.JSONData.Text)
                        self.current_document_path = path
                        self.last_saved_time = time.time()
                except Exception:
                    wx.MessageDialog(self, "Unable to open %s ." % path, "Error")

                self.last_directory = os.path.dirname(path)

        if self.tree_edit_mode:
            try:
                self.JSONData.SyncTextToData()
                self.tree.UpdateTreeViewFromJSONData(self.JSONData.JSONdata)
            except Exception:
                wx.MessageDialog(self, "Unable to parse loaded JSON file.", "Error")
                wx.GenericMessageDialog(self, "Unable to parse loaded JSON file.")
        

    def OnPromptToSave(self, save_as=False):
        """Prompt a save file diaglogue to user."""
        if not save_as and self.current_document_path and os.path.isfile(self.current_document_path):
            try:
                self.SaveFile(self.current_document_path)
            except Exception:
                wx.GenericMessageDialog(self, "Unable to save %s ." % self.current_document_path)
            return

        with wx.FileDialog(self, "Select Save Location", defaultDir=self.GetDefaultDirectory(), 
        wildcard='*.json', style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() != wx.ID_CANCEL:
                path = dlg.GetPath()
                try:
                    self.SaveFile(path)
                    self.current_document_path = path
                except Exception:
                    wx.GenericMessageDialog(self, "Unable to save %s ." % path)

                self.last_directory = os.path.dirname(path)

    def SaveFile(self, path):
        try:
            with open(path, 'w') as file:
                if self.tree_edit_mode:
                    self.JSONData.SyncDataToText()
                else:
                    self.JSONData.SetJSONText(self.editor.GetText())

                file.write(self.JSONData.Text)
                self.last_saved_time = time.time()
        except Exception as error:
            raise error

    def OnPrettify(self, event):

        try:
            self.JSONData.Text = self.editor.GetText()
            self.JSONData.PrettifyText()
            self.editor.Text = self.JSONData.Text
        except ValueError as error:
            print(error)
            #TODO

    def OnCompactify(self, event):

        try:
            self.JSONData.Text = self.editor.GetText()
            self.JSONData.CompactifyText()
            self.editor.Text = self.JSONData.Text
        except ValueError as error:
            print(error)
            #TODO

    def OnValidateText(self, event):
        try:
            self.JSONData.Text = self.editor.GetText()
            self.JSONData.ValidateJSONText()
            self.editor.Text = self.JSONData.Text
        except ValueError as error:
            print(error)
            #TODO

    
class MyApp(wx.App):
    def OnInit(self):
        self.data = JSONDataModel()
        self.frame = EditorJSON(None, "Editor JSON", self.data)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
