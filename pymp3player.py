# new main.py
import wx
from musicplayer import MusicPlayer
from directorybrowser import DirectoryBrowser
from playlist import PlaylistListCtrl
from fileloader import FileLoader
from experimental import Feed

class MainWindow(wx.Frame):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.master_panel = wx.Panel(self)
		self.music_player = MusicPlayer(self.master_panel)
		self.file_loader = FileLoader(self.master_panel)
		self.playlist = PlaylistListCtrl(self.master_panel)

		# this -might- defeat the purpose of the observer pattern
		# right? Maybe?
		self.file_loader.sub_interface.RegisterObserver(self.playlist)
		self.playlist.sub_interface.RegisterObserver(self.music_player)

		self.master_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.main_component_sizer = wx.BoxSizer(wx.VERTICAL)
		self.main_component_sizer.Add(self.file_loader, 1, wx.EXPAND)
		self.main_component_sizer.Add(self.music_player, 1, wx.EXPAND)
		self.main_component_sizer.Add(self.playlist, 4, wx.EXPAND)

		self.master_sizer.Add(self.main_component_sizer, 1, wx.EXPAND)

		self.master_panel.SetSizer(self.master_sizer)


class MyApp(wx.App):
	def OnInit(self):
		self.frame = MainWindow(None, -1, title="Music is Fun!", size=(800,600))
		self.frame.Show()
		return True


if __name__ == "__main__":
	app = MyApp(0)
	app.MainLoop()