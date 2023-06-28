import wx
import wx.xrc
import wx.richtext
from threading import Thread
from requests import request
from requests.exceptions import ConnectionError


class RequestPanel (wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(800, 500), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos,
                          size=size, style=style, name=name)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        requestSizer = self.makeRequestSizer()
        mainSizer.Add(requestSizer, 0, wx.ALL | wx.EXPAND, 5)

        responseSizer = wx.BoxSizer(wx.VERTICAL)

        self.responseRtc = wx.richtext.RichTextCtrl(
            self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)
        self.responseRtc.SetEditable(False)
        responseSizer.Add(self.responseRtc, 1, wx.EXPAND | wx.ALL, 5)

        mainSizer.Add(responseSizer, 1, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

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

        self.urlCtrl.SetValue("localhost")

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
        runner = Thread(target=self.doRequest)
        runner.start()

    def doRequest(self):
        self.lockRequests()
        url = self.urlCtrl.GetValue()
        if "http" not in url:
            url = "http://" + url
        method = self.methodChoice.GetString(
            self.methodChoice.GetCurrentSelection())
        try:
            response = request(method=method, url=url)
        except ConnectionError as e:
            print(e)
            print(dir(e))
            wx.MessageDialog(
                self, "Unable to connect, please check your url", caption="Alert").ShowModal()
        else:
            self.responseRtc.SetEditable(True)
            self.responseRtc.Clear()
            self.responseRtc.WriteText(response.text)
            self.responseRtc.SetEditable(False)
            print(response.status_code)
            print('content start')
            print(response.content)
            print('content end')
            print(response.encoding)
            print(response.headers)
        self.unlockRequests()

    def __del__(self):
        pass
