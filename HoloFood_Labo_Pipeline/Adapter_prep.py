#Adapter prep using Tempdeck
from opentrons import labware, instruments, modules, robot
from opentrons.legacy_api.modules import tempdeck

temp_deck_1 = tempdeck.TempDeck()
temp_deck_1._port = '/dev/ttyACM0'
temp_deck_1 = modules.load('tempdeck', '10')



#pipette
tiprack_200 = labware.load('labsolute-tiprack-200µl', '5')

#pipette
s50 = instruments.P50_Single(mount='left', tip_racks=[tiprack_200])


#PROTOCOL
temp_deck_1.set_temperature(95)
temp_deck_1.wait_for_temp()
s50.delay(minutes=20)
temp_deck_1.deactivate()
