#Adapter prep using Tempdeck
from opentrons import labware, instruments, modules, robot
from opentrons.legacy_api.modules import tempdeck

temp_deck_1 = tempdeck.TempDeck()
temp_deck_1._port = '/dev/ttyACM0'
temp_deck1 = modules.load('tempdeck', '4')

#PROTOCOL
temp_deck_1.set_temperature(95)
temp_deck_1.wait_for_temp()

temp_deck_1.deactivate()
