import wx
import wx.stc as stc

class JSONTextView(stc.StyledTextCtrl):

    def __init__(self, parent):
        stc.StyledTextCtrl.__init__(self, parent)

        font = wx.Font(10, wx.FONTFAMILY_SWISS,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL)
        self.face = font.GetFaceName()
        self.size = font.GetPointSize()

        self.SetMarginCount(2)
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(1, 0)
        self.SetMarginWidth(1, 25)
        self.SetMargins(10, 10)

        self.SetKeyWords(0, "true false null")
        self.SetLexer(stc.STC_LEX_JSON)

        # Styles
        self.SetTabIndents(4)
        self.indicators = [] #list to store current indicator ranges in tuples
        self.DefineErrorInidcators()
        self.SetTextStyle()

        # Modified Mask
        self.SetModEventMask(stc.STC_MOD_INSERTTEXT|stc.STC_MOD_DELETETEXT|stc.STC_PERFORMED_UNDO|
        stc.STC_PERFORMED_REDO|stc.STC_MULTILINEUNDOREDO|stc.STC_LASTSTEPINUNDOREDO)

        self.Bind(wx.EVT_FIND, self.OnFindNext)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFindNext)
        

    def GetFaces(self):
        return dict(font=self.face, size=self.size)

    def SetTextStyle(self):
        faces = self.GetFaces()
        default = "face:%(font)s,size:%(size)d" % faces
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, default)

        fonts = "face:%(font)s,size:%(size)d" % faces
        tmpl = "fore:%s," + fonts
        default = "fore:#000000," + fonts

        self.StyleSetSpec(stc.STC_JSON_DEFAULT, default)
        self.StyleSetSpec(stc.STC_JSON_PROPERTYNAME, tmpl % "#bc5426")
        self.StyleSetSpec(stc.STC_JSON_STRING, tmpl % "#3a7dc1")
        self.StyleSetSpec(stc.STC_JSON_NUMBER, tmpl % "#6f9b31")
        self.StyleSetSpec(stc.STC_JSON_KEYWORD, tmpl % "#9a62be")
        self.StyleSetSpec(stc.STC_JSON_OPERATOR, tmpl % "#202020")
        self.StyleSetSpec(stc.STC_JSON_URI, tmpl % "#d24189")
 

    def BindTextModifiedHandler(self, callback):
        self.Bind(stc.EVT_STC_MODIFIED, callback)

        
    def DefineErrorInidcators(self):
        """ Defines the indicator's style """
        self.IndicatorSetStyle(0, stc.STC_INDIC_POINT)
        self.IndicatorSetForeground(0, wx.RED)
        self.indicators.append(0)

        self.IndicatorSetStyle(1, stc.STC_INDIC_FULLBOX)
        self.IndicatorSetForeground(1, wx.RED)
        self.indicators.append(1)
    

    def ClearAllIndicators(self):
        """ Clear all indicators """
        for indicator in self.indicators:
            self.SetIndicatorCurrent(indicator)
            self.IndicatorClearRange(0, self.GetTextLength())


    def HighlightIndicateError(self, line, column, pos):
        """ Turn on indicator highlights on the indicated area"""
        
        self.ClearAllIndicators()

        # Highlight till the end of the file
        line_end = self.GetLineEndPosition(line - 1) # convert to index style
        self.SetIndicatorCurrent(1)
        self.IndicatorFillRange(pos, line_end - pos)

        #Set point inidcator
        self.SetIndicatorCurrent(0)
        self.IndicatorFillRange(pos, line_end - pos)

    def OnFindNext(self, event):
        """ Find text find next event handler """
        flags = self.search_replace_data.GetFlags()
        going_down = False
        if flags & wx.FR_DOWN:
            going_down = True

        if going_down:
            self.SetCurrentPos(self.GetAnchor())
        else:
            back = self.GetAnchor()-1
            if back <= 0:
                back = self.GetTextLength()
            self.SetAnchor(back)
            self.SetCurrentPos(back)

        self.SearchAnchor()
        self.ClearSelections()
        
        if going_down:
            self.SearchNext(flags, self.search_replace_data.GetFindString())
            self.LineScrollDown()
        else:
            self.SearchPrev(flags, self.search_replace_data.GetFindString())
            self.LineScrollUp()

    
    def OnUndo(self, event):
        self.Undo()


    def OnRedo(self, event):
        self.Redo()

    def OnSearch(self, event):
        self.search_replace_data = wx.FindReplaceData()
        dlg = wx.FindReplaceDialog(self, self.search_replace_data, title="Search", style=0)
        dlg.Show()
