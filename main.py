import wx
import wx.xrc
import wx.stc
import sys
import os

from request_panel import RequestPanel

bundle_dir = getattr(
    sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


class MainFrame(wx.Frame):

    def __init__(self):
        super(MainFrame, self).__init__(
            None, title='Requester', size=wx.Size(800, 500))
        icon_path = os.path.abspath(os.path.join(bundle_dir, 'icon.png'))
        self.SetIcon(wx.Icon(icon_path))
        self.pnl = RequestPanel(self)


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
