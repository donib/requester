import wx
import wx.xrc
import wx.richtext
import wx.grid
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


class RequestPanel (wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(800, 500), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
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
        self.headerGrid.CreateGrid(1, 2)
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

        self.tabRequestData = TabPanelRTX(self.notebook)

        self.notebook.AddPage(self.tabRequestData, "Body")
        self.notebook.AddPage(self.tabResponse, "Response")

        mainSizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(mainSizer)
        self.Bind(wx.EVT_SIZE, self.onResize)
        self.Layout()

        self.updateHeaderColumnsSize()

        self.urlCtrl.SetFocus()

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

        self.urlCtrl.SetValue("localhost:8020")

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
        key = self.headerGrid.GetCellValue(
            self.headerGrid.GetNumberRows() - 1, 0)
        if str.strip(key):
            self.headerGrid.AppendRows()
            self.Layout()

    def doRequest(self):
        url = self.urlCtrl.GetValue()
        header = self.getHeader()
        body = self.tabRequestData.dataRTX.GetValue()
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
        self.tabResponse.dataRTX.WriteText(self.lastResponse.text)
        self.tabResponse.dataRTX.SetEditable(False)
        self.Layout()

    def updateHeaderColumnsSize(self):
        x, _ = self.headerGrid.GetSize()
        self.headerGrid.SetColSize(0, int(x / 2) - 20)
        self.headerGrid.SetColSize(1, int(x / 2) - 20)

    def onResize(self, e):
        self.updateHeaderColumnsSize()
        e.Skip()

    def getHeader(self):
        header = {}
        for row in range(self.headerGrid.GetNumberRows()):
            header[self.headerGrid.GetCellValue(
                row, 0)] = self.headerGrid.GetCellValue(row, 1)

        header = {k: header[k] for k in header if k}
        return header

    def __del__(self):
        pass
