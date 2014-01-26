import wx
from experimental import Song, ObserverInterface, SubjectInterface
import os

class FileLoader(wx.Panel):
	def __init__(self, *args, **kwargs):
		super(FileLoader, self).__init__(*args, **kwargs)

		self.sub_interface = SubjectInterface()

		self.load_button = wx.Button(self, wx.ID_ANY, "Load Files?")
		self.load_button.Bind(wx.EVT_BUTTON, self.OnLoad)

		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.load_button, 1, wx.EXPAND)
		self.SetSizer(self.sizer)

	def OnLoad(self, event):
		dialog = wx.FileDialog(self, message="Select a file to play.",
			defaultDir = os.getcwd(),
			defaultFile = "",
			style = wx.OPEN | wx.CHANGE_DIR | wx.MULTIPLE)
		if dialog.ShowModal() == wx.ID_OK:
			filepath = dialog.GetPaths()
			songlist = []
			for path in filepath:
				songlist.append(Song(path))
			self.sub_interface.NotifyObservers(songlist)
			
