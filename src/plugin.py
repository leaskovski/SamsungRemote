from Plugins.Plugin import PluginDescriptor
from Components.HdmiCec import HdmiCec
from enigma import eActionMap
from sys import maxint
from samsungtv.remote import SamsungTV
from time import gmtime, strftime
import sys


# IP Address of the TV
TV_ADDRESS = '192.168.0.100'
# Supported key codes that we want to handle
SUPPORTED_KEYS = [113,114,115]


def debug(locationStr, messageStr):
    with open('/tmp/SamsungRemote.log', 'a') as d:
        d.write(strftime('%x %X', gmtime()) + ' - ' + locationStr + ' - ' + messageStr + '\n')


class SamsungRemote():

    def __init__(self):
        self._tv = None
        self._connected = False

        # Bind to the HDMI CEC plugin so that on key presses we get triggered
        debug('SamsungRemote.__init__','Binding to HDMI CEC plugin')
        eActionMap.getInstance().unbindAction('', HdmiCec.instance.keyEvent)
        eActionMap.getInstance().bindAction('', -maxint - 1, self.keyEvent)


    def keyEvent(self, keyCode, keyEvent):

        # We havent enabled volume forwarding so exit unhandled
        if not HdmiCec.instance.volumeForwardingEnabled:
            return 0

        # If the keycode isn't in our list of handled codes, then exit unhandled
        if not keyCode in SUPPORTED_KEYS:
            return 0        

        # Try to connect to the TV
        try:
            if not self._connected:
                debug('SamsungRemote.keyEvent','Connecting to TV ' + TV_ADDRESS)
                self._tv = SamsungTV(TV_ADDRESS)
                self._connected = True
        except Exception, e:
            debug('SamsungRemote.keyEvent','Unable to connect to TV, Error:' + str(e))
            self._connected = False
            return 0

        # Define the result code, 1=handled, 0=not handled
        handledInt = 0

        # Try to handle the keycode
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
            debug('SamsungRemote.keyEvent','Error:' + str(e))
            self._connected = False
                
        debug('SamsungRemote.keyEvent','KeyCode=' + str(keyCode) + ', KeyEvent=' + str(keyEvent) + ', Handled=' + str(handledInt))
        return handledInt


def main(session, **kwargs):
    return


def Plugins(**kwargs):
    SamsungRemote.instance = SamsungRemote()
    return PluginDescriptor(
        name="Samsung Remote Emulator",
        description="Sends volume keys to TV over the network",
        where=PluginDescriptor.WHERE_PLUGINMENU,
        fnc=main)
