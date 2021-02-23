from Plugins.Plugin import PluginDescriptor
from Components.HdmiCec import HdmiCec
from Components.ActionMap import ActionMap
from Components.config import config, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigText, ConfigSelection
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Screens.Screen import Screen
from enigma import eActionMap
from sys import maxint
from samsungtv.remote import SamsungTV
from time import strftime
from datetime import datetime

import sys


# Config settings for the plugin
config.plugins.SamsungRemote = ConfigSubsection()
config.plugins.SamsungRemote.tv_address = ConfigText(default="", fixed_size=False)
config.plugins.SamsungRemote.log_enabled = ConfigYesNo(default=False)
config.plugins.SamsungRemote.log_file = ConfigText(default="/tmp/SamsungRemote.log", fixed_size=False)

# Supported key codes that we want to handle
SUPPORTED_KEYS = [113, 114, 115]
KEY_CODES_DICT = {
    113:'Mute',
    114:'Volume Down',
    115:'Volume Up'
}
KEY_EVENTS_DICT = {
    0:'Button Pressed',
    1:'Button Released'
}
HANDLED_DICT = {
    0:'No',
    1:'Yes'
}


def debug(locationStr, messageStr):
    if config.plugins.SamsungRemote.log_enabled.value:
        with open(config.plugins.SamsungRemote.log_file.value, 'a') as d:
            d.write(datetime.now().strftime('%x-%H:%M:%S.%f') + ' - ' + locationStr + ' - ' + messageStr + '\n')


class SamsungRemote():

    def __init__(self):
        self._tv = None
        self._connected = False

        # Bind to the HDMI CEC plugin so that on key presses we get triggered
        debug('SamsungRemote.__init__', 'Binding to HDMI CEC plugin')
        eActionMap.getInstance().unbindAction('', HdmiCec.instance.keyEvent)
        eActionMap.getInstance().bindAction('', -maxint - 1, self.keyEvent)

    def keyEvent(self, keyCode, keyEvent):

        # We haven't set the plugin up
        if config.plugins.SamsungRemote.tv_address.value == "":
            return 0

        # We havent enabled volume forwarding so exit unhandled
        if not HdmiCec.instance.volumeForwardingEnabled:
            return 0

        # If the keycode isn't in our list of handled codes, then exit unhandled
        if not keyCode in SUPPORTED_KEYS:
            return 0

        # Try to connect to the TV
        try:
            if not self._connected:
                debug('SamsungRemote.keyEvent', 'Connecting to TV ' + config.plugins.SamsungRemote.tv_address.value)
                self._tv = SamsungTV(config.plugins.SamsungRemote.tv_address.value)
                self._connected = True
        except Exception, e:
            debug('SamsungRemote.keyEvent', 'Unable to connect to TV, Error:' + str(e))
            self._connected = False
            return 0

        # Define the result code, 1=handled, 0=not handled
        handledInt = 0

        # Try to handle the keycode
        debug('SamsungRemote.keyEvent', 'KeyCode=' + str(KEY_CODES_DICT.get(keyCode)) + ', KeyEvent=' + str(KEY_EVENTS_DICT.get(keyEvent)))
        try:
            if keyCode == 115:
                # vol+
                handledInt = 1
                if keyEvent == 1:
                    self._tv.volume_up()
            elif keyCode == 114:
                # vol-
                handledInt = 1
                if keyEvent == 1:
                    self._tv.volume_down()
            elif keyCode == 113:
                # mute
                handledInt = 1
                if keyEvent == 1:
                    self._tv.mute()
        except Exception, e:
            handledInt = 0
            debug('SamsungRemote.keyEvent', 'Error:' + str(e))
            self._connected = False

        debug('SamsungRemote.keyEvent', 'Handled=' + str(HANDLED_DICT.get(handledInt)))
        return handledInt


def main(session, **kwargs):
    session.open(SamsungRemoteConfigFunction)
    return


def Plugins(**kwargs):
    SamsungRemote.instance = SamsungRemote()
    return PluginDescriptor(
        name="Samsung Remote Emulator",
        description="Sends volume keys to TV over the network",
        where=PluginDescriptor.WHERE_PLUGINMENU,
        fnc=main)


class SamsungRemoteConfigFunction(ConfigListScreen, Screen):
    skin = """
        <screen position="80,170" size="560,270" title="Samsung Remote Emulator">
            <ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" transparent="1" alphatest="on" />
            <ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" transparent="1" alphatest="on" />
            <ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" transparent="1" alphatest="on" />
            <ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" transparent="1" alphatest="on" />
            <widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;20" valign="center" halign="center" backgroundColor="#1f771f" transparent="1" />
            <widget name="config" position="0,45" size="560,220" scrollbarMode="showOnDemand" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self["key_green"] = Label(_("Save"))
        self.cfglist = []
        self.cfglist.append(getConfigListEntry(_("TV IP Address:"), config.plugins.SamsungRemote.tv_address))
        self.cfglist.append(getConfigListEntry(_("Logging Enabled:"), config.plugins.SamsungRemote.log_enabled))
        self.cfglist.append(getConfigListEntry(_("Log File:"), config.plugins.SamsungRemote.log_file))
        ConfigListScreen.__init__(self, self.cfglist, session)
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {"green": self.save, "cancel": self.exit}, -1)

    def save(self):
        for x in self["config"].list:
            x[1].save()
        self.close()

    def exit(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close()
