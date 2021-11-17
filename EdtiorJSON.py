import JSONTreeView as TreeView
import JSONTextView as TextView
import wx


class TabTextView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.control_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.btn_undo = wx.Button(self, label="Undo", size=(35,35))
        self.btn_redo = wx.Button(self, label="Redo", size=(35,35))
        self.btn_pretty_format = wx.Button(self, label="Pretty", size=(35,35))
        self.btn_compact_format = wx.Button(self, label="Compact", size=(35,35))
        self.btn_pretty_validate = wx.Button(self, label="Validate", size=(35,35))

        self.control_panel_sizer.Add(self.btn_undo)
        self.control_panel_sizer.Add(self.btn_redo)
        self.control_panel_sizer.Add(self.btn_pretty_format)
        self.control_panel_sizer.Add(self.btn_compact_format)
        self.control_panel_sizer.Add(self.btn_pretty_validate)

        self.editor = TextView.JSONTextView(self)

        self.main_sizer.Add(self.control_panel_sizer, 0, wx.ALL, 2)
        self.main_sizer.Add(self.editor, 1, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM, 2)
        self.SetSizer(self.main_sizer)

        
class TabTreeView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.control_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.btn_expand_all = wx.Button(self, label="Expand", size=(35,35))
        self.btn_collapse_all = wx.Button(self, label="Collapse", size=(35,35))

        self.control_panel_sizer.Add(self.btn_expand_all)
        self.control_panel_sizer.Add(self.btn_collapse_all)

        self.tree = TreeView.JSONTreeView(self)

        self.main_sizer.Add(self.control_panel_sizer, 0, wx.ALL, 2)
        self.main_sizer.Add(self.tree, 1, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM, 2)

        self.SetSizer(self.main_sizer)


class EditorJSON(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        
        self.SetSize(1280, 800)
        self.SetUpMenuBar()

        # Main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Tree, Text Editor Area
        main_panel = wx.Panel(self)
        tabs_panel = wx.Notebook(main_panel, size=(600,800), style=wx.NB_NOPAGETHEME)

        self.tree_tab = TabTreeView(tabs_panel)
        self.tree = self.tree_tab.tree
        self.editor_tab = TabTextView(tabs_panel)
        self.editor = self.editor_tab.editor

        tabs_panel.AddPage(self.editor_tab, "Editor View")
        tabs_panel.AddPage(self.tree_tab, "Tree View")
        tabs_panel.SetPadding(wx.Size(10, 10))

        main_sizer.Add(tabs_panel, 1, wx.EXPAND)

        main_panel.SetSizer(main_sizer)
        main_panel.Fit()


    def SetUpMenuBar(self):
        self.menu = wx.MenuBar()
        file_menu = wx.Menu()
        file_item = wx.MenuItem(file_menu, wx.ID_NEW, text="New", helpString="Create new JSON file")
        file_menu.AppendItem(file_item)
        file_item = wx.MenuItem(file_menu, wx.ID_OPEN, text="Open", helpString="Open existing JSON file")
        file_menu.AppendItem(file_item)
        file_item = wx.MenuItem(file_menu, wx.ID_SAVE, text = "Save", helpString="Save current JSON file")
        file_menu.AppendItem(file_item)
        file_item = wx.MenuItem(file_menu, wx.ID_SAVEAS, text = "Save As", helpString="Save as current JSON file")
        file_menu.AppendItem(file_item)
        file_item = wx.MenuItem(file_menu, wx.ID_EXIT, text = "Exit", helpString="Exit tool")
        file_menu.AppendItem(file_item)

        #If time allowed adding edit feature

        help_menu = wx.Menu()
        help_item = wx.MenuItem(help_menu, wx.ID_HELP, text = "Help", helpString="About this application")
        help_menu.AppendItem(help_item)
        help_item = wx.MenuItem(help_menu, wx.ID_ABOUT, text = "About", helpString="About this application")
        help_menu.AppendItem(help_item)

        self.menu.Append(file_menu, "File")
        self.menu.Append(help_menu, "Help")
        self.SetMenuBar(self.menu)
        self.Bind(wx.EVT_MENU, self.MenuItemHandler)

    def MenuItemHandler(self, event):
        id = event.GetId()
        #TODO

class MyApp(wx.App):
    def OnInit(self):
        self.frame = EditorJSON(None, "Editor JSON")
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
