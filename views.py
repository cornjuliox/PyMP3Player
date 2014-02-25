import wx
import wx.media as media
import os
import eyed3
from models import Song
import wx.dataview as dv
from ObjectListView import ObjectListView, ColumnDefn
from pubsub import pub

import pdb


class FileLoader(wx.Panel):
	def __init__(self, *args, **kwargs):
		super(FileLoader, self).__init__(*args, **kwargs)

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
			songlist = []
			filepath = dialog.GetPaths()
			for path in filepath:
				song = Song(path)
				if not song:
					print "SONG DIDN'T WORK."
				songlist.append(Song(path))
			pub.sendMessage("files_loaded_topic", data=songlist)

class MusicPlayer(wx.Panel):
	def __init__(self, *args, **kwargs):
		super(MusicPlayer, self).__init__(*args, **kwargs)

		# it remains to be seen if my new design choices
		# have any negative effect on the application
		# in the end.
		self.setupTimer()
		self.media_ctrl = self.setupMediaPlayer()
		self.media_ctrl.Hide()

		self.master_sizer = wx.BoxSizer(wx.VERTICAL)
		self.slider_sizer = self.setupSlider() #this should return a sizer.
		self.button_sizer = self.setupButtons()
		self.music_info_sizer = self.setupMusicDataView()

		self.master_sizer.Add(self.button_sizer, 0, wx.EXPAND)
		self.master_sizer.Add(self.slider_sizer, 0, wx.EXPAND)
		self.master_sizer.Add(self.music_info_sizer, 0, wx.EXPAND | wx.ALL, border=7)

		self.SetSizer(self.master_sizer)

		self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnPlay)
		pub.subscribe(self.OnLoad, 'file_selected_topic')

	def UpdateDataView(self, data):
		try: 
			self.media_ctrl.Load(data.filepath)
		except:
			# Load() throws an execption but the doc page seems to be missing
			# I'll just wing it for now.
			print "Could not load file! Check path and try again."
			print "Filepath: %s" % data.filepath
		self.song_title.SetLabel(data.title)
		self.artist_name.SetLabel(data.artist)
		self.album_name.SetLabel(data.album)
		self.play_button.Enable()

	def setupMusicDataView(self):
		self.song_title = wx.StaticText(self, wx.ID_ANY, "(TITLE)")
		font1 = wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		self.song_title.SetFont(font1)

		self.artist_name = wx.StaticText(self, wx.ID_ANY, "(ARTIST)")
		font2 = wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.artist_name.SetFont(font2)

		self.album_name = wx.StaticText(self, wx.ID_ANY, "(ALBUM)")
		font3 = wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.album_name.SetFont(font3)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.song_title, 0, wx.EXPAND)
		sizer.Add(self.artist_name, 0, wx.EXPAND)
		sizer.Add(self.album_name, 0, wx.EXPAND)

		return sizer

	def setupTimer(self):
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer)
		self.timer.Start(100)

	def setupMediaPlayer(self):
		try:
			# Directshow is  not throwing the 'EVT_MEDIA_LOADED' event
			# when .load() is called. 
			# Switching this to WMP10 for now
			# http://trac.wxwidgets.org/ticket/13828
			backend = media.MEDIABACKEND_WMP10
			media_ctrl = media.MediaCtrl(self, wx.ID_ANY, szBackend=backend)
		except NotImplementedError:
			print "Error: MediaCtrl not implemented on this system! Windows only!"
			self.Destroy()
			raise
		return media_ctrl

	def setupSlider(self):
		# I wonder if I need to add self to this...
		self.seek_slider = wx.Slider(self, -1, 0, 1, 2)
		self.seek_slider.Bind(wx.EVT_SCROLL, self.OnSeek)
		
		sliderSizer = wx.BoxSizer(wx.HORIZONTAL)
		sliderSizer.Add(self.seek_slider, 1, wx.EXPAND | wx.ALL, border=2)
		return sliderSizer

	def setupButtons(self):
		self.play_button = wx.Button(self, wx.ID_ANY, "Play")
		self.pause_button = wx.Button(self, wx.ID_ANY, "Pause")
		self.stop_button = wx.Button(self, wx.ID_ANY, "Stop")

		self.play_button.Bind(wx.EVT_BUTTON, self.OnPlay)
		self.pause_button.Bind(wx.EVT_BUTTON, self.OnPause)
		self.stop_button.Bind(wx.EVT_BUTTON, self.OnStop)

		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer.Add(self.play_button, 1, wx.EXPAND)
		buttonSizer.Add(self.pause_button, 1, wx.EXPAND)
		buttonSizer.Add(self.stop_button, 1, wx.EXPAND)

		self.play_button.Disable()
		return buttonSizer

	def OnTimer(self, event):
		offset = self.media_ctrl.Tell()
		self.seek_slider.SetValue(offset)

	def OnSeek(self, event):
		offset = self.seek_slider.GetValue()
		self.media_ctrl.Seek(offset)

	# you might be wondering why there are two functions,
	# both wrapping media_ctrl.Play().
	# this is because I'm trying to get the player to automatically
	# start playing when a file is loaded, but EVT_MEDIA_LOADED
	# for some reason does not want to work properly.
	def OnPlay(self, event):
		self.seek_slider.SetRange(0,self.media_ctrl.Length())
		self.media_ctrl.Play()

	def FirePlay(self):
		self.media_ctrl.Play()

	def OnPause(self, event):
		self.media_ctrl.Pause()

	def OnStop(self, event):
		self.media_ctrl.Stop()

	def OnLoad(self, song):
		self.media_ctrl.Load(song.filepath)
		self.UpdateDataView(song)

class PlaylistListCtrl(wx.Panel):
	def __init__(self, *args, **kwargs):
		super(PlaylistListCtrl, self).__init__(*args, **kwargs)

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
		pub.subscribe(self.UpdateStateControl, "files_loaded_topic")

		self.delete_button = wx.Button(self, wx.ID_ANY, "Remove from Playlist")
		self.delete_button.Bind(wx.EVT_BUTTON, self.OnDelete)


		self.wrapper = wx.BoxSizer(wx.VERTICAL)
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.dataOlv, 1, wx.EXPAND | wx.ALL, border=5)
		self.wrapper.Add(self.sizer, 1, wx.EXPAND)
		self.wrapper.Add(self.delete_button, 0, wx.EXPAND)

		self.SetSizer(self.wrapper)

	def UpdateStateControl(self, data):
		# build a list of songs and their attribs
		# [['artist', 'title', 'album']]
		self.parsed_list = data
		self.refreshList()

	def refreshList(self):
		# note; lists of data must match
		# the order in wich the columns appear.
		# .data should be a list, remember?
		self.dataOlv.AddObjects(self.parsed_list)

	def OnActivation(self, event):
		myObject = self.dataOlv.GetSelectedObject()
		pub.sendMessage("file_selected_topic", song=myObject)

	def OnDelete(self, event):
		objects = self.dataOlv.GetSelectedObjects()
		self.dataOlv.RemoveObjects(objects)