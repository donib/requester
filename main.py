import wx
import wx.xrc
import wx.stc
import wx.lib.agw.aui.auibook
import sys
import os
import time

from request_panel import RequestPanel

bundle_dir = getattr(
    sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


class MainFrame(wx.Frame):

    def __init__(self):
        super(MainFrame, self).__init__(
            None, title='Requester', size=wx.Size(800, 500))
        icon_path = os.path.abspath(os.path.join(bundle_dir, 'icon.png'))
        self.SetIcon(wx.Icon(icon_path))

        self.notebook = wx.lib.agw.aui.auibook.AuiNotebook(
            self, style=wx.EXPAND | wx.ALL)

        self.notebook.Bind(
            wx.lib.agw.aui.auibook.EVT_AUINOTEBOOK_PAGE_CHANGED, self.handleTabChange)
        self.notebook.Bind(
            wx.lib.agw.aui.auibook.EVT_AUINOTEBOOK_PAGE_CLOSE, self.handleTabClosing)
        self.AddTabPanel = wx.Panel(self.notebook)

        # ugly hack
        self.notebook.AddPage(self.AddTabPanel, "+")

        self.notebook.DoSizing()

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


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
