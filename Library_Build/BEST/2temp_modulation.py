from opentrons import labware, instruments, modules, robot
from opentrons.legacy_api.modules import tempdeck


'''
    ssh into robot and
    then run ls /dev/tty*
    you are looking for two values with the format /dev/ttyACM*
    you will use those values in line 22 and 23.
    If you need to know which tempdeck is hooked up to which port.
    You will unplug one, then run ls /dev/tty*. There should only be one /dev/ttyACM*.
    This will correlate to the tempdeck that is plugged in. Then you plug the other temp deck in and run ls /dev/tty* again.
    There should now be two /dev/ttyACM*s, the one that was not there in the previous command will correlate to the
    tempdeck you just plugged in.

'''


temp_deck_1 = tempdeck.TempDeck()
temp_deck_2 = tempdeck.TempDeck()

temp_deck_1._port = '/dev/ttyACM3'
temp_deck_2._port = '/dev/ttyACM2'


if not robot.is_simulating():
	temp_deck_1.connect()
	temp_deck_2.connect()

temp_deck1 = modules.load('tempdeck', '4')
temp_deck2 = modules.load('tempdeck', '7')


temp_deck_1.set_temperature(10)
temp_deck_2.set_temperature(10)

temp_deck_1.wait_for_temp()
temp_deck_2.wait_for_temp()
