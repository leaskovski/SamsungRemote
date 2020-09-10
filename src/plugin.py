from Plugins.Plugin import PluginDescriptor
from Components.HdmiCec import HdmiCec
from enigma import eActionMap
from sys import maxint
from samsungtv.remote import SamsungTV

def debug(str):
    with open('/tmp/SamsungRemote.log', 'a') as d:
        d.write(str + '\n')


class SamsungRemote():

    def __init__(self):
        debug('SamsungRemote.__init__')
        eActionMap.getInstance().unbindAction('', HdmiCec.instance.keyEvent)
        eActionMap.getInstance().bindAction('', -maxint - 1, self.keyEvent)

    def keyEvent(self, keyCode, keyEvent):
        if not HdmiCec.instance.volumeForwardingEnabled:
            return 0
        debug('SamsungRemote.keyEvent ' + str(keyCode) + ' ' + str(keyEvent))

        tv = SamsungTV('192.168.0.100')

        if keyCode == 115:
            # vol+
            tv.volume_up
        elif keyCode == 114:
            # vol-
            tv.volume_down
        elif keyCode == 113:
            # mute
            tv.mute
        else:
            # key not handled
            return 0

        if keyEvent == 1:
            # key release handled
            return 1
        elif keyEvent != 0 and keyEvent != 2:
            # other type of event not handled
            return 0

        # key press
        debug('SamsungRemote.keyEvent complete')
        tv.close

        return 1


def main(session, **kwargs):
    return


def Plugins(**kwargs):
    SamsungRemote.instance = SamsungRemote()
    return PluginDescriptor(
        name="Network volume forwarder",
        description="Sends volume keys to TV over the network",
        where=PluginDescriptor.WHERE_PLUGINMENU,
        fnc=main)
