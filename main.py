from request_panel import RequestPanel
import wx
import wx.xrc
import wx.stc
import wx.lib.agw.aui.auibook
import sys
import os
import time
import json

from platformdirs import user_config_dir

appName = "requester"
appAuthor = "donib"

bundle_dir = getattr(
    sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


class MainFrame(wx.Frame):

    def __init__(self):
        super(MainFrame, self).__init__(
            None, title='Requester', size=wx.Size(800, 500))
        icon_path = os.path.abspath(os.path.join(bundle_dir, 'icon.png'))
        self.confDir = user_config_dir(appname=appName, appauthor=appAuthor)
        self.SetIcon(wx.Icon(icon_path))

        self.notebook = wx.lib.agw.aui.auibook.AuiNotebook(
            self, style=wx.EXPAND | wx.ALL)

        self.loadSession()
        self.notebook.Bind(
            wx.lib.agw.aui.auibook.EVT_AUINOTEBOOK_PAGE_CHANGED, self.handleTabChange)
        self.notebook.Bind(
            wx.lib.agw.aui.auibook.EVT_AUINOTEBOOK_PAGE_CLOSE, self.handleTabClosing)
        self.AddTabPanel = wx.Panel(self.notebook)

        # ugly hack
        self.notebook.AddPage(self.AddTabPanel, "+", select=False)

        self.notebook.DoSizing()

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def handleTabChange(self, e):
        current = self.notebook.GetCurrentPage()
        if self.AddTabPanel == current:
            idx = self.notebook.GetPageIndex(current)
            newPage = RequestPanel(self.notebook)
            self.notebook.InsertPage(
                idx, newPage, "Request")
            newPage.updateTitle()
            self.lastAdded = time.time()
            wx.CallAfter(self.notebook.SetSelection, idx)
        e.Skip()

    def handleTabClosing(self, e: wx.lib.agw.aui.auibook.AuiNotebookEvent):
        current = self.notebook.GetCurrentPage()
        if current == self.AddTabPanel:
            return e.Veto()

        self.notebook.AdvanceSelection(False, False)
        e.Skip()

    def loadSession(self):
        filePath = os.path.join(self.confDir, "session.json")
        try:
            with open(filePath, "r") as fp:
                session = json.load(fp)
                for s in session:
                    newTab = RequestPanel(
                        self.notebook, session=s)
                    self.notebook.AddPage(newTab, "New Tab")
                    newTab.updateTitle()
                return True
        except FileNotFoundError:
            return None

    def saveSession(self):
        session = []
        for idx in range(self.notebook.GetPageCount()):
            page = self.notebook.GetPage(idx)
            if isinstance(page, RequestPanel):
                session.append({
                    "url": page.urlCtrl.GetValue(),
                    "method": page.methodChoice.GetCurrentSelection(),
                    "response": page.tabResponse.dataRTX.GetValue(),
                    "body": page.tabRequestData.dataSTX.GetValue(),
                    "header": page.getHeaderTable()
                })
        os.makedirs(self.confDir, exist_ok=True)
        filePath = os.path.join(self.confDir, "session.json")
        with open(filePath, "w") as fp:
            json.dump(session, fp)

    def onClose(self, e):
        self.saveSession()
        e.Skip()


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
