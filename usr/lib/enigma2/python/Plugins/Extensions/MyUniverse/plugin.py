#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#######################################################################
#
#    MyUniverse
#    for openMips on Gigablue devices
#    Coded by Sinthex Designagentur (c) 2017
#    www.sinthex.de
#
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.
#
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#
#
#######################################################################

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from twisted.web.client import downloadPage
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
import urllib, re
import gettext
from enigma import ePicLoad
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS

#############################################################

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("MyUniverse", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/MyUniverse/locale/"))

def _(txt):
	t = gettext.dgettext("MyUniverse", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block

#############################################################

config.plugins.MyUniverse = ConfigSubsection()
#config.skin = ConfigSubsection()
#General
config.plugins.MyUniverse.SkinColor = ConfigSelection(default="#007392bd", choices = [
				("#007392bd", _("Blue")),
				("#0061b8da", _("Lightblue")),
				("#00a658d3", _("Violett")),
				("#00d67c67", _("Red")),
				("#00d7618b", _("Pink")),
				("#00b5d364", _("Green")),
				("#00bbbbbb", _("Grey"))
				])
config.plugins.MyUniverse.SkinTransparency = ConfigSelection(default="#bbaaaaaa", choices = [
				("#00aaaaaa", _("Level 1 - Not transparent")),
				("#22aaaaaa", _("Level 2")),
				("#44aaaaaa", _("Level 3")),
				("#66aaaaaa", _("Level 4")),
				("#88aaaaaa", _("Level 5")),
				("#aaaaaaaa", _("Level 6")),
				("#bbaaaaaa", _("Level 7 - Default")),
				("#ccaaaaaa", _("Level 8")),
				("#ffaaaaaa", _("Level 9 - More transparent"))
				])

def main(session, **kwargs):
	session.open(MyUniverse,"/usr/lib/enigma2/python/Plugins/Extensions/MyUniverse/images/#007392bd.jpg")

def Plugins(**kwargs):
	return PluginDescriptor(name="MyUniverse", description=_("Configuration tool for GBUniverseHD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)



#######################################################################


class MyUniverse(ConfigListScreen, Screen):
	skin = """
<screen name="MyUniverse-Setup" position="0,0" size="1920,1080" flags="wfNoBorder" backgroundColor="transparent">
	<widget source="global.CurrentTime" render="Label" position="1660,52" size="200,78" font="Universe-Heavy; 50" backgroundColor="background" transparent="1" zPosition="1" halign="right" noWrap="1" valign="bottom">
	<convert type="ClockToText">Default</convert>
	</widget>
	<widget source="global.CurrentTime" render="Label" position="1384,55" size="291,68" font="Universe-Thin; 35" backgroundColor="background" transparent="1" zPosition="1" halign="right" noWrap="1" valign="bottom">
	<convert type="ClockToText">Format:%a. %e. %b</convert>
	</widget>
	<ePixmap name="menu-top" position="0,0" size="1920,460" pixmap="GBUniverseHD/construct/shadow/top.png" alphatest="blend" zPosition="-10" />
	<eLabel text="MyUniverse" position="65,52" size="1300,78" font="Universe-Heavy; 50" foregroundColor="skin-foreground" backgroundColor="background" transparent="1" noWrap="1" valign="bottom" zPosition="-1" />
	<eLabel text="Cancel" zPosition="1" backgroundColor="background" size="231,40" foregroundColor="skin-foreground" position="1612,278" font="Universe-Heavy; 20" transparent="1" halign="right" />
	<eLabel text="Save" zPosition="1" backgroundColor="background" size="231,40" foregroundColor="skin-foreground" position="1612,338" font="Universe-Heavy; 20" transparent="1" halign="right" />
	<eLabel text="Reboot" zPosition="1" backgroundColor="background" size="231,40" foregroundColor="skin-foreground" position="1612,393" font="Universe-Heavy; 20" transparent="1" halign="right" />
	<ePixmap pixmap="GBUniverseHD/construct/backgrounds/background-exit-button.png" size="10,55" position="1850,142" />
	<eLabel backgroundColor="red" size="10,55" position="1850,263" />
	<eLabel backgroundColor="green" size="10,55" position="1850,323" />
	<eLabel backgroundColor="yellow" size="10,55" position="1850,383" />
	<eLabel backgroundColor="blue" size="10,55" position="1850,444" />
	<eLabel backgroundColor="grey" size="231,40" foregroundColor="skin-foreground" position="1612,157" font="Universe-Heavy; 20" transparent="1" halign="right" text="Exit" />
	<ePixmap name="" position="0,0" size="1920,1080" pixmap="GBUniverseHD/construct/shadow/right.png" zPosition="-20" alphatest="blend" />
	<ePixmap position="1635,785" size="232,254" zPosition="-9" pixmap="GBUniverseHD/construct/backgrounds/background-symbol.png" transparent="0" alphatest="blend" />
	<ePixmap position="63,150" size="937,887" zPosition="-3" pixmap="GBUniverseHD/construct/backgrounds/background-window-title.png" alphatest="blend" />
	<ePixmap alphatest="blend" position="1000,150" size="46,887" zPosition="-5" pixmap="GBUniverseHD/construct/shadow/window-right.png" />
	<ePixmap alphatest="blend" position="63,1037" size="937,48" zPosition="-5" pixmap="GBUniverseHD/construct/shadow/window-bottom.png" />
	<ePixmap alphatest="blend" position="1000,1037" size="46,48" zPosition="-5" pixmap="GBUniverseHD/construct/shadow/window-br.png" />
	<eLabel position="63,150" size="937,887" zPosition="-100" backgroundColor="skin-transparency" />
	<ePixmap pixmap="GBUniverseHD/construct/symbols/skin.png" position="1635,785" size="232,254" alphatest="blend" />
	<widget name="config" position="73,170" scrollbarMode="showOnDemand" size="913,320" transparent="1" />
	<widget name="previewimage" position="73,510" size="913,514" zPosition="1" backgroundColor="background" />
</screen>
"""

	def __init__(self, session, args = None, picPath = None):
		self.skin_lines = []
		Screen.__init__(self, session)
		self.session = session
		self.backgroundsDir = "/usr/share/enigma2/GBUniverseHD/construct/backgrounds/"
		self.skinFileBackup = "/usr/share/enigma2/GBUniverseHD/skin.xml.backup"
		self.skinFile = "/usr/share/enigma2/GBUniverseHD/skin.xml"
		self.picPath = picPath
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["previewimage"] = Pixmap()
		list = []
		list.append(getConfigListEntry(_("Skin Color"), config.plugins.MyUniverse.SkinColor))
		list.append(getConfigListEntry(_("Skin Transparency"), config.plugins.MyUniverse.SkinTransparency))
		

		ConfigListScreen.__init__(self, list)
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft,"down": self.keyDown,"up": self.keyUp,"right": self.keyRight,"red": self.exit,"yellow": self.reboot, "blue": self.showInfo, "green": self.save,"cancel": self.exit}, -1)
		self.onLayoutFinish.append(self.UpdateComponents)

		
	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			#print "\n selectedOption: " + returnValue + "\n"
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MyUniverse/images/" + returnValue + ".jpg"
			return path
		except:
			return "/usr/lib/enigma2/python/Plugins/Extensions/MyUniverse/images/#007392bd.jpg"
		
	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)
	
	def ShowPicture(self):
		self.PicLoad.setPara([self["previewimage"].instance.size().width(),self["previewimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#44000000"])
		self.PicLoad.startDecode(self.GetPicturePath())
		#print "showing image"
		
	def DecodePicture(self, PicInfo = ""):
		#print "decoding picture"
		ptr = self.PicLoad.getData()
		self["previewimage"].instance.setPixmap(ptr)	

	def UpdateComponents(self):
		self.UpdatePicture()
				

	def keyLeft(self):	
		ConfigListScreen.keyLeft(self)	
		self.ShowPicture()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.ShowPicture()
	
	def keyDown(self):
		#print "key down"
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		#ConfigListScreen.keyDown(self)
		self.ShowPicture()
		
	def keyUp(self):
		#print "key up"
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		#ConfigListScreen.keyUp(self)
		self.ShowPicture()
	
	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))
		
	def showInfo(self):
		self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

	def save(self):
		for x in self["config"].list:
			if len(x) > 1:
        			x[1].save()
			else:
       				pass
       			
		###########READING DATA FILES
		try:
			###Main XML
			#self.appendSkinFile(self.daten + "main.xml")

			#xFile = open(self.sourceSkinFile, "w")
			#for xx in self.skin_lines:
			#	xFile.writelines(xx)
			#xFile.close()
			system('cp ' + self.backgroundsDir + 'alt/' + config.plugins.MyUniverse.SkinColor.value + '/background-infobar.png ' + self.backgroundsDir)
			system('cp ' + self.backgroundsDir + 'alt/' + config.plugins.MyUniverse.SkinColor.value + '/background-window-details.png ' + self.backgroundsDir)
			system('cp ' + self.backgroundsDir + 'alt/' + config.plugins.MyUniverse.SkinColor.value + '/background-window-title.png ' + self.backgroundsDir)
			system('cp ' + self.backgroundsDir + 'alt/' + config.plugins.MyUniverse.SkinColor.value + '/background-window.png ' + self.backgroundsDir)
			system('cp ' + self.backgroundsDir + 'alt/' + config.plugins.MyUniverse.SkinColor.value + '/background-symbol.png ' + self.backgroundsDir)
			
			
			system('cp ' + self.skinFile + ' ' + self.skinFileBackup)
			o = open(self.skinFile,"w")
			regex_col = re.compile(r".*<color name=\"skin-background-colored\".*$", re.IGNORECASE)
			regex_trans = re.compile(r".*<color name=\"skin-transparency\".*$", re.IGNORECASE)
			for line in open(self.skinFileBackup):
				line = regex_col.sub("     <color name=\"skin-background-colored\" value=\"%s\" />" % config.plugins.MyUniverse.SkinColor.value, line)	
				line = regex_trans.sub("     <color name=\"skin-transparency\" value=\"%s\" />" % config.plugins.MyUniverse.SkinTransparency.value, line)	
				o.write(line)
			o.close()
			#system('rm -rf ' + self.sourceSkinFile)

		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)
		#config.skin.primary_skin.value = "GBUniverseHD/skin.xml"
		configfile.save()
		

	def restartGUI(self, answer):
		if answer is True:  
			configfile.save()
			self.session.open(TryQuitMainloop, 3)
		else:
			for x in self["config"].list:
				if len(x) > 1:
					x[1].cancel()
			self.close()

	def exit(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))
