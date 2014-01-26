import wx
import wx.dataview as dv
from ObjectListView import ObjectListView, ColumnDefn
from experimental import ObserverInterface, SubjectInterface


class PlaylistListCtrl(wx.Panel):
	def __init__(self, *args, **kwargs):
		super(PlaylistListCtrl, self).__init__(*args, **kwargs)

		self.sub_interface = SubjectInterface()

		#self.playlist = dv.DataViewListCtrl(self, style=dv.DV_ROW_LINES)
		self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		self.parsed_list = []

		self.dataOlv.SetColumns([
			ColumnDefn("Title", "left", 200, "title"),
			ColumnDefn("Artist", "left", 200, "artist"),
			ColumnDefn("Album", "left", 200, "album"),
			ColumnDefn("Length", "left", 200, "length"),
			])

		self.dataOlv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActivation)

		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.dataOlv, 1, wx.EXPAND | wx.ALL, border=5)
		self.SetSizer(self.sizer)

	def UpdateStateControl(self, data):
		# build a list of songs and their attribs
		# [['artist', 'title', 'album']]
		self.parsed_list = data
		self.refreshList()

	def refreshList(self):
		# note; lists of data must match
		# the order in wich the columns appear.
		# .data should be a list, remember?
		self.dataOlv.SetObjects(self.parsed_list)

	def OnActivation(self, event):
		myObject = self.dataOlv.GetSelectedObject()
		self.sub_interface.NotifyObservers(myObject)
		