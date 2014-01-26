import wx
import wx.media as media
import os
import eyed3

# I'll need to work on this one a little bit...
# I can't really figure out how to work it the way I want to...

class DirectoryBrowser(wx.Panel):
	def __init__(self, *args, **kwargs):
		super(DirectoryBrowser, self).__init__(*args, **kwargs)
		self.dir_browser = wx.GenericDirCtrl(self, wx.ID_ANY, style=wx.DIRCTRL_DIR_ONLY|wx.DIRCTRL_MULTIPLE)

		self.dir_browser.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnSelect)

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.dir_browser, 1, wx.EXPAND | wx.ALL, border=3)
		self.SetSizer(self.sizer)

	def OnSelect(self, event):
		print self.dir_browser.GetPath()



