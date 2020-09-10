# Samsung Remote

Samsung Remote is a plugin for Enigma2 based devices, that will allow Samsung TVs to handle particular requests (such as volume) that otherwise wouldn't be supported using HDMI-CEC.  It works by forwarding the request to the TV via the network.

This code was originally developed by [Plasticassius](https://sourceforge.net/u/gutemine/profile), and made available on the OpenPLI forums [here](https://forums.openpli.org/topic/65041-do-tvs-handle-hdmi-cec-forward-volume-keys/).  I wasn't able to get that original code to work, but have extended it to use the Samsung TV API remote python code that is available from [PIP](https://pypi.org/project/samsungtv/#description).

## Installation

Download the IPK to a folder on your Enigma2 box, and then go the "System > Software Management > Install Local Extension".  Find the IPK downloaded to the box, and install.  Once installed, change the HDMI-CEC plugin option "Forward volume keys" to "On".  Finally reboot the GUI for the box.

## Authors and acknowledgement

Plasticassius - <https://forums.openpli.org/user/186709-plasticassius/>

## License
This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.