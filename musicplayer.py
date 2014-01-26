import wx
import wx.media as media
import os
import eyed3
from experimental import ObserverInterface

# note: I might have to package the buttons
# with this thing rather than having it separate
# like i do now.

class MusicPlayer(wx.Panel):
	def __init__(self, *args, **kwargs):
		super(MusicPlayer, self).__init__(*args, **kwargs)

		# it remains to be seen if my new design choices
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

	def UpdateStateControl(self, data):
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
			backend = media.MEDIABACKEND_DIRECTSHOW
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

	def OnPlay(self, event):
		self.seek_slider.SetRange(0,self.media_ctrl.Length())
		self.media_ctrl.Play()

	def OnPause(self, event):
		self.media_ctrl.Pause()

	def OnStop(self, event):
		self.media_ctrl.Stop()



