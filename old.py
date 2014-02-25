import wx
import wx.media as media
import os
import eyed3
import wx.dataview as dv
#######################################
# NOTE:
# This file is retained for legacy purposes.
# By that I mean I'm using it as a guide
# to develop the rest of the app.
# Since the MediaCtrl class is rather poorly
# documented, and this file contains
# pretty much everything I know about it
# (learned through experimentation)
#######################################


class MainWindow(wx.Frame):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.panel = wx.Panel(self, wx.ID_ANY)

	def utility_info_dialog(self, text="Not Implemented Yet!", title="Error!"):
		""" Small utility function, designed to be used internally whenever a generic MessageDialog
		is needed.

		Takes two arguments, text and title, and passses them into wx.MessageDialog to create
		a simple error/info dialog. """
		modal = wx.MessageDialog(self, text, title, style=wx.OK | wx.INFORMATION)
		modal.ShowModal()
		modal.Destroy()


class MusicPlayer(MainWindow):
	def __init__(self, *args, **kwargs):
		super(MusicPlayer, self).__init__(*args, **kwargs)
		# should I move this into a separate class? 
		# I have barely any idea what I'm doing re: design.
		self.seek_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.onTimer)
		self.seek_timer.Start(100)

		self.seek_slider = wx.Slider(self.panel, -1, 0, 1, 2)

		try:
			self.media_ctrl = media.MediaCtrl(self.panel, wx.ID_ANY, 
				szBackend=media.MEDIABACKEND_DIRECTSHOW)
		except NotImplementedError:
			text_blob = "MediaCtrl does not appear to be implemented on this system."
			self.utility_info_dialog(text=text_blob)
			self.Destroy()
			raise
		# I don't really need to see the mediactrl.
		self.media_ctrl.Hide()

	def onTimer(self, event):
		offset = self.media_ctrl.Tell()
		self.seek_slider.SetValue(offset)
		print "offset %s" % offset

	def onSeek(self, event):
		offset = self.seek_slider.GetValue()
		self.mediaSeek(offset)

	def onPlay(self, event):
		if self.media_ctrl.GetState() == media.MEDIASTATE_PLAYING:
			self.media_ctrl.Pause()
		else:
			self.seek_slider.SetRange(0,self.media_ctrl.Length())
			self.media_ctrl.Play()

	def onStop(self, event):
		self.media_ctrl.Stop()

	def mediaSeek(self, offset):
		self.media_ctrl.Seek(offset)

	def mediaLoad(self, filepath):
		self.media_ctrl.Load(filepath)
		# TODO: Write in checks for the artist/album data
		# make sure it doesn't crash.
		self._getSetMetaData(filepath)
		self.play_button.SetLabel("Play")
		print "file loaded: %s" % filepath

	def _getSetMetaData(self, filepath):
		if audio_data.tag.artist != None:
			artist = audio_data.tag.artist
		else:
			artist = "None"
		if audio_data.tag.title != None:
			title = audio_data.tag.title
		else:
			title = "None"
		if audio_data.tag.album != None:
			album = audio_data.tag.album
		else:
			album = "None"
		minutes = audio_data.info.time_secs / 60
		seconds = audio_data.info.time_secs % 60
		if seconds < 10: 
			length = "%d:%02d" % (minutes, seconds)
		else:
			length = "%d:%d" % (minutes, seconds)
		# should blah blah blah blah.
		self.setLabels(title, artist, album, length)


class ButtonManager(MusicPlayer):
	def __init__(self, *args, **kwargs):
		super(ButtonManager, self).__init__(*args, **kwargs)
		self.load_button = wx.Button(self.panel, wx.ID_ANY, "Load")
		self.play_button = wx.Button(self.panel, wx.ID_ANY, "Play")
		self.stop_button = wx.Button(self.panel, wx.ID_ANY, "Stop")

		self.load_button.Bind(wx.EVT_BUTTON, self.loadFile)
		self.play_button.Bind(wx.EVT_BUTTON, self.callPlay)
		self.play_button.Disable() # don't enable it until a file has been loaded and its ready to play.
		self.stop_button.Bind(wx.EVT_BUTTON, self.callStop)
		self.seek_slider.Bind(wx.EVT_COMMAND_SCROLL, self.onSeek)
		#self.list_button.Bind(wx.EVT_BUTTON, self.)

	def loadFile(self, event):
		dialog = wx.FileDialog(self, message="Select a file to play.",
			defaultDir = os.getcwd(),
			defaultFile = "",
			style = wx.OPEN | wx.CHANGE_DIR)
		if dialog.ShowModal() == wx.ID_OK:
			filepath = dialog.GetPath()
			self.mediaLoad(filepath)
			self.play_button.Enable()

	def callPlay(self, event):
		if self.play_button.GetLabel().lower() == "play":
			self.play_button.SetLabel("Pause")
		elif self.play_button.GetLabel().lower() == "pause":
			self.play_button.SetLabel("Play")
		self.onPlay(event)
		
	def callStop(self, event):
		self.play_button.SetLabel("Play")
		self.onStop(event)


class SongInfoLayer(ButtonManager):
	def __init__(self, *args, **kwargs):
		super(SongInfoLayer, self).__init__(*args, **kwargs)
		self.now_playing_label = wx.StaticText(self.panel, wx.ID_ANY, "(nothing loaded)")
		self.artist_label = wx.StaticText(self.panel, wx.ID_ANY, "(nothing loaded)")
		self.album_label = wx.StaticText(self.panel, wx.ID_ANY, "(nothing loaded)")
		self.song_length = wx.StaticText(self.panel, wx.ID_ANY, "(nothing loaded)")

		self.playlist = dv.DataViewListCtrl(self.panel, style=dv.DV_ROW_LINES)
		self.playlist.AppendTextColumn("Artist", width=200)
		self.playlist.AppendTextColumn("Title", width=200)
		self.playlist.AppendTextColumn("Genre", width=200)

	def setLabels(self, song_title, artist, album, length):
		self.now_playing_label.SetLabel("Title: " + song_title)
		self.artist_label.SetLabel("Artist: " + artist)
		self.album_label.SetLabel("Album: " + album)
		self.song_length.SetLabel("Length: " + length)


class DirControlViewer(SongInfoLayer):
	def __init__(self, *args, **kwargs):
		super(DirControlViewer, self).__init__(*args, **kwargs)
		self.dir2 = wx.GenericDirCtrl(self.panel, -1, style=wx.DIRCTRL_DIR_ONLY|wx.DIRCTRL_MULTIPLE)
		#self.dir2.SetDefaultPath(os.getcwd())


class LayoutManager(DirControlViewer):
	def __init__(self, *args, **kwargs):
		super(LayoutManager, self).__init__(*args, **kwargs)

		self.master_container = wx.BoxSizer(wx.HORIZONTAL)
		self.master_sizer = wx.BoxSizer(wx.VERTICAL)
		self.dirctrl_sizer = wx.BoxSizer(wx.VERTICAL)
		self.dirctrl_sizer.Add(self.dir2, 1, wx.EXPAND)

		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.load_button, 1, wx.EXPAND | wx.ALL)
		self.sizer.Add(self.play_button, 1, wx.EXPAND | wx.ALL)
		self.sizer.Add(self.stop_button, 1, wx.EXPAND | wx.ALL)

		self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer2.Add(self.seek_slider, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, border = 10)

		self.sizer3 = wx.BoxSizer(wx.VERTICAL)
		self.sizer3.Add(self.now_playing_label, 0, wx.EXPAND | wx.LEFT, border = 10)
		self.sizer3.Add(self.artist_label, 0, wx.EXPAND | wx.LEFT, border = 10)
		self.sizer3.Add(self.album_label, 0, wx.EXPAND | wx.LEFT, border = 10)
		self.sizer3.Add(self.song_length, 0, wx.EXPAND | wx.LEFT, border = 10)

		self.sizer4 = wx.BoxSizer(wx.VERTICAL)
		self.sizer4.Add(self.playlist, 0, wx.EXPAND | wx.ALL) 

		self.master_sizer.Add(self.sizer, 0, wx.EXPAND)
		self.master_sizer.Add(self.sizer2, 0, wx.EXPAND)
		self.master_sizer.Add(self.sizer3, 0, wx.EXPAND)
		self.master_sizer.Add(self.sizer4, 0, wx.EXPAND)

		self.master_container.Add(self.dirctrl_sizer, 1, wx.EXPAND | wx.ALL)
		self.master_container.Add(self.master_sizer, 1, wx.EXPAND)

		self.panel.SetSizer(self.master_container)


class MyApp(wx.App):
	def OnInit(self):
		self.frame = LayoutManager(None, -1, title="Music is Fun!", size=(800,600))
		self.frame.Show()
		return True

if __name__ == "__main__":
	app = MyApp(0)
	app.MainLoop()


