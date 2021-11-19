import wx
import wx.stc as stc

class JSONTextView(stc.StyledTextCtrl):

    def __init__(self, parent):
        stc.StyledTextCtrl.__init__(self, parent)

        self.SetMarginCount(2)
        
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(1, 0)
        self.SetMarginWidth(1, 25)
        self.SetMargins(10, 10)

        self.SetKeyWords(0, "true false null")
        self.SetLexer(stc.STC_LEX_JSON)

        self.SetTabIndents(4)
        self.WrapCount(1)

    def OnUndo(self, evt):
        self.Undo()


    def OnRedo(self, evt):
        self.Redo()
