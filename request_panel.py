import wx
import wx.xrc
import wx.richtext
import wx.grid
import json
from wx import stc
from threading import Thread
from requests import request
from requests.exceptions import ConnectionError


class TabPanelRTX(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.dataRTX = wx.richtext.RichTextCtrl(
            self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)
        mainSizer.Add(self.dataRTX, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(mainSizer)


class TabPanelSTX(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.dataSTX = wx.stc.StyledTextCtrl(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.dataSTX.StyleClearAll()
        self.dataSTX.SetUseTabs(False)
        self.dataSTX.SetTabWidth(4)
        self.dataSTX.SetIndent(4)
        self.dataSTX.SetTabIndents(True)
        self.dataSTX.SetBackSpaceUnIndents(True)
        self.dataSTX.SetViewEOL(False)
        self.dataSTX.SetViewWhiteSpace(False)
        self.dataSTX.SetMarginWidth(2, 0)
        self.dataSTX.SetIndentationGuides(True)
        self.dataSTX.SetReadOnly(False)
        self.dataSTX.SetMarginType(1, wx.stc.STC_MARGIN_SYMBOL)
        self.dataSTX.SetMarginMask(1, wx.stc.STC_MASK_FOLDERS)
        self.dataSTX.SetMarginWidth(1, 16)
        self.dataSTX.SetMarginSensitive(1, True)
        self.dataSTX.SetProperty("fold", "1")
        self.dataSTX.SetFoldFlags(
            wx.stc.STC_FOLDFLAG_LINEBEFORE_CONTRACTED | wx.stc.STC_FOLDFLAG_LINEAFTER_CONTRACTED)
        self.dataSTX.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER)
        self.dataSTX.SetMarginWidth(0, self.dataSTX.TextWidth(
            wx.stc.STC_STYLE_LINENUMBER, "_99999"))
        self.dataSTX.MarkerDefine(
            wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS)
        self.dataSTX.MarkerSetBackground(wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
        self.dataSTX.MarkerSetForeground(wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
        self.dataSTX.MarkerDefine(
            wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS)
        self.dataSTX.MarkerSetBackground(
            wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK)
        self.dataSTX.MarkerSetForeground(
            wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE)
        self.dataSTX.MarkerDefine(
            wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY)
        self.dataSTX.MarkerDefine(
            wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS)
        self.dataSTX.MarkerSetBackground(
            wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK)
        self.dataSTX.MarkerSetForeground(
            wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE)
        self.dataSTX.MarkerDefine(
            wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS)
        self.dataSTX.MarkerSetBackground(
            wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
        self.dataSTX.MarkerSetForeground(
            wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
        self.dataSTX.MarkerDefine(
            wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY)
        self.dataSTX.MarkerDefine(
            wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY)
        self.dataSTX.SetSelBackground(
            True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.dataSTX.SetSelForeground(
            True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        self.dataSTX.SetLexer(stc.STC_LEX_JSON)
        self.dataSTX.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,
                                  "fore:RED,back:MEDIUM TURQUOISE,bold")
        self.dataSTX.StyleSetSpec(
            stc.STC_STYLE_BRACEBAD, "fore:RED,back:THISTLE,bold")
        self.dataSTX.StyleSetSpec(stc.STC_JSON_BLOCKCOMMENT,
                                  "fore:#008000,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_COMPACTIRI, "fore:#0000FF,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_DEFAULT, "fore:#000000,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_ERROR, "fore:#FFFF80,back:#FF0000")
        self.dataSTX.StyleSetSpec(stc.STC_JSON_ESCAPESEQUENCE,
                                  "fore:#0000FF,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_KEYWORD, "fore:#18AF8A,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(stc.STC_JSON_PROPERTYNAME,
                                  "fore:#8000FF,back:#FFFFFF,bold")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_LDKEYWORD, "fore:#FF0000,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(stc.STC_JSON_LINECOMMENT,
                                  "fore:#008000,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_URI, "fore:#0000FF,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_STRINGEOL, "fore=#808080,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_NUMBER, "fore:#FF8000,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_STRING, "fore:#800000,back:#FFFFFF")
        self.dataSTX.StyleSetSpec(
            stc.STC_JSON_OPERATOR, "fore:#000000,back:#FFFFFF")
        self.dataSTX.SetKeyWords(0, 'null false true')
        self.dataSTX.SetKeyWords(
            1, '@id @context @type @value @language @container @list @set @reverse @index @base @vocab @graph')

        mainSizer.Add(self.dataSTX, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(mainSizer)


class RequestPanel (wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(800, 500), style=wx.TAB_TRAVERSAL, name=wx.EmptyString, session=None):
        wx.Panel.__init__(self, parent, id=id, pos=pos,
                          size=size, style=style, name=name)

        self.lastResponse = None
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        requestSizer = self.makeRequestSizer()
        mainSizer.Add(requestSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.headerGrid = wx.grid.Grid(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        if session:
            rows = len(session['header'])
            self.headerGrid.CreateGrid(rows, 3)
            for row in range(rows):
                self.headerGrid.SetCellRenderer(
                    row, 0, wx.grid.GridCellBoolRenderer())
                self.headerGrid.SetCellEditor(
                    row, 0, wx.grid.GridCellBoolEditor())
                enabled, key, value = session['header'][row]
                self.headerGrid.SetCellValue(row, 0, enabled)
                self.headerGrid.SetCellValue(row, 1, key)
                self.headerGrid.SetCellValue(row, 2, value)

            self.urlCtrl.SetValue(session['url'])
            self.methodChoice.SetSelection(session['method'])
        else:
            rows = 3
            self.headerGrid.CreateGrid(3, 3)
            for i in range(rows):
                self.headerGrid.SetCellRenderer(
                    i, 0, wx.grid.GridCellBoolRenderer())
                self.headerGrid.SetCellEditor(
                    i, 0, wx.grid.GridCellBoolEditor())

            self.headerGrid.SetCellValue(0, 0, '1')
            self.headerGrid.SetCellValue(0, 1, 'Content-Type')
            self.headerGrid.SetCellValue(0, 2, 'application/json')
            self.headerGrid.SetCellValue(1, 1, 'Accept')
            self.headerGrid.SetCellValue(1, 2, 'application/json')

        self.headerGrid.EnableEditing(True)
        self.headerGrid.EnableGridLines(True)
        self.headerGrid.SetMargins(0, 0)

        # Rows
        self.headerGrid.AutoSizeRows()

        # Label Appearance
        self.headerGrid.HideColLabels()
        self.headerGrid.HideRowLabels()

        # Cell Defaults
        self.headerGrid.Bind(
            wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.onGridClicked)
        self.headerGrid.Bind(
            wx.grid.EVT_GRID_CELL_CHANGED, self.onGridEdit)
        self.headerSizer.Add(self.headerGrid, 1, wx.ALL, 5)
        mainSizer.Add(self.headerSizer, 0, wx.ALL | wx.EXPAND, 5)

        self.notebook = wx.Notebook(self)

        self.tabResponse = TabPanelRTX(self.notebook)
        self.tabResponse.dataRTX.SetEditable(False)

        self.tabRequestData = TabPanelSTX(self.notebook)

        if session:
            self.tabRequestData.dataSTX.SetValue(session['body'])
            self.tabResponse.dataRTX.SetValue(session['response'])

        self.notebook.AddPage(self.tabRequestData, "Body")
        self.notebook.AddPage(self.tabResponse, "Response")

        mainSizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(mainSizer)
        self.Bind(wx.EVT_SIZE, self.onResize)
        self.updateHeaderColumnsSize()

        self.urlCtrl.SetFocus()

        self.methodChoice.Bind(wx.EVT_CHOICE, self.updateTitle)
        self.urlCtrl.Bind(wx.EVT_TEXT, self.updateTitle)

    def makeRequestSizer(self):
        requestSizer = wx.BoxSizer(wx.HORIZONTAL)

        methodChoiceChoices = [
            u"GET", u"POST", u"PUT", u"DELETE", u"PATCH"]
        self.methodChoice = wx.Choice(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, methodChoiceChoices, 0)
        self.methodChoice.SetSelection(0)
        requestSizer.Add(self.methodChoice, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        self.urlCtrl = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        requestSizer.Add(
            self.urlCtrl, 1, wx.ALL, 5)

        self.requestButton = wx.Button(
            self, wx.ID_ANY, u"Go", wx.DefaultPosition, wx.DefaultSize, 0)
        self.requestButton.Bind(wx.EVT_BUTTON, self.onDoRequest)
        requestSizer.Add(self.requestButton, 0, wx.ALL, 5)

        self.urlCtrl.SetValue("localhost:8080")

        return requestSizer

    def lockRequests(self):
        self.methodChoice.Disable()
        self.urlCtrl.Disable()
        self.requestButton.Disable()

    def unlockRequests(self):
        self.methodChoice.Enable()
        self.urlCtrl.Enable()
        self.requestButton.Enable()

    def onDoRequest(self, evt):
        self.lockRequests()
        Thread(target=self.doRequest).start()

    def onGridClicked(self, e):
        e.GetEventObject().SetGridCursor(e.GetRow(), e.GetCol())
        e.Skip()

    def onGridEdit(self, e):
        rows = self.headerGrid.GetNumberRows()
        key = self.headerGrid.GetCellValue(
            rows - 1, 1)
        if str.strip(key):
            self.headerGrid.AppendRows()
            self.headerGrid.SetCellRenderer(
                rows, 0, wx.grid.GridCellBoolRenderer())
            self.headerGrid.SetCellEditor(
                rows, 0, wx.grid.GridCellBoolEditor())
            self.updateHeaderColumnsSize()

    def doRequest(self):
        url = self.urlCtrl.GetValue()
        header = self.getHeader()
        body = self.tabRequestData.dataSTX.GetValue()
        if "http" not in url:
            url = "http://" + url
        method = self.methodChoice.GetString(
            self.methodChoice.GetCurrentSelection())
        try:
            self.lastResponse = request(method=method, url=url,
                                        data=body, headers=header,
                                        allow_redirects=False)
        except ConnectionError as e:
            wx.MessageDialog(
                self, "Unable to connect, please check your url", caption="Alert").ShowModal()
        wx.CallAfter(self.updateResponse)

    def updateResponse(self):
        self.unlockRequests()
        if not self.lastResponse:
            return
        self.tabResponse.dataRTX.SetEditable(True)
        self.tabResponse.dataRTX.Clear()
        self.tabResponse.dataRTX.WriteText('=' * 80)
        self.tabResponse.dataRTX.WriteText('\n')
        if self.lastResponse.status_code < 300:
            self.tabResponse.dataRTX.BeginTextColour(wx.Colour((10, 230, 10)))
        elif self.lastResponse.status_code < 400:
            self.tabResponse.dataRTX.BeginTextColour(wx.Colour((125, 125, 10)))
        else:
            self.tabResponse.dataRTX.BeginTextColour(wx.Colour((230, 10, 100)))
        self.tabResponse.dataRTX.WriteText(
            f'Status: {self.lastResponse.status_code}\n')
        self.tabResponse.dataRTX.EndAllStyles()
        self.tabResponse.dataRTX.WriteText(
            f'Content-Type: {self.lastResponse.headers["Content-Type"]}\n')
        self.tabResponse.dataRTX.WriteText('=' * 80)
        self.tabResponse.dataRTX.WriteText('\n')
        if "/json" in self.lastResponse.headers["Content-Type"]:
            response = json.dumps(self.lastResponse.json(),
                                  indent=4, ensure_ascii=False)
        else:
            response = self.lastResponse.text
        self.tabResponse.dataRTX.WriteText(response)
        self.tabResponse.dataRTX.SetEditable(False)
        self.notebook.SetSelection(1)
        self.Layout()

    def updateHeaderColumnsSize(self):
        x, _ = self.headerGrid.GetSize()
        if x <= 0:
            return
        self.headerGrid.SetColSize(0, 30)
        self.headerGrid.SetColSize(1, int(x / 2) - 30)
        self.headerGrid.SetColSize(2, int(x / 2) - 30)
        for i in range(self.headerGrid.GetNumberRows()):
            self.headerGrid.SetCellAlignment(
                i, 0, horiz=wx.ALIGN_CENTER, vert=wx.ALIGN_CENTER)
        self.Layout()

    def updateTitle(self, e=None):
        method = self.methodChoice.GetString(
            self.methodChoice.GetCurrentSelection())
        url = self.urlCtrl.GetValue()
        title = f"{method}: {url}"
        idx = self.Parent.GetPageIndex(self)
        self.Parent.SetPageText(page_idx=idx, text=title)

    def onResize(self, e):
        self.updateHeaderColumnsSize()
        e.Skip()

    def getHeaderTable(self):
        header = []
        for row in range(self.headerGrid.GetNumberRows()):
            header.append((self.headerGrid.GetCellValue(row, 0), self.headerGrid.GetCellValue(
                row, 1), self.headerGrid.GetCellValue(row, 2)))
        return header

    def getHeader(self):
        header = {}
        for row in range(self.headerGrid.GetNumberRows()):
            if self.headerGrid.GetCellValue(row, 0) == '1':
                header[self.headerGrid.GetCellValue(
                    row, 1)] = self.headerGrid.GetCellValue(row, 2)

        header = {k: header[k] for k in header if k}
        return header

    def __del__(self):
        pass
