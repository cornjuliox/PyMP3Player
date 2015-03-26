# new main.py
import wx
from pubsub import pub

# I know that wildcard imports are a bad thing but it can't
# be avoided at this point.
from views import *
from musicplayer import *
from models import Song

# 475 8015 GIRLIE

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
       
        # menu creation code has been moved to the mainwindow class
        # because its just better that way. 
        self.CreateMenu()

        self.master_panel = wx.Panel(self)
        self.music_player = MusicPlayer(self.master_panel)

        self.master_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.main_component_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_component_sizer.Add(self.music_player, 1, wx.EXPAND)

        self.master_sizer.Add(self.main_component_sizer, 1, wx.EXPAND)

        self.master_panel.SetSizer(self.master_sizer)
        self.master_sizer.Fit(self)

    def CreateMenu(self):
        self.menubar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        self.f_item = self.fileMenu.Append(wx.ID_OPEN, 'Load Sound File', 'Loads a sound file from disk.')
        self.q_item = self.fileMenu.Append(wx.ID_EXIT, 'Quit', 'Closes the application.')

        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.menubar.Append(self.fileMenu, '&File')

        self.SetMenuBar(self.menubar)

    def OnMenu(self, event):
        evt_id = event.GetId()
        actions_table = {
            wx.ID_OPEN : self.OnLoad,
            wx.ID_EXIT : self.OnQuit,
        }
        action = actions_table.get(evt_id, None)
        if action:
            action(event)
        else:
            event.Skip()

    def OnQuit(self, event):
        self.Close()

    def OnLoad(self, event):
        dialog = wx.FileDialog(self, message="Select a file to play.",
            defaultDir = os.getcwd(),
            defaultFile = "",
            style = wx.OPEN | wx.CHANGE_DIR)
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            self.music_player.LoadFile(filepath)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainWindow(None, -1, title="Music is Fun!", size=(800,600))
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()