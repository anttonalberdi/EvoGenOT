##### PURIFY #####
#
#
# THINGS TO DO BEFORE PROCEDURE
# 1.  Make fresh 80% Ethanol
# 2.  Equlibrate SPRI beads at room temperature
#
# PROCEDURE
#	
#   1. Add 1.5x SPRI beads to x volume of DNA	
#   2. Incubate for 1 minutes
#   3. Engage magnet and incubate for 5 minutes
#   4. Remove supernatant
#   5. Wash twice with 80% ethanol
#   6. Elute DNA

######## IMPORT LIBRARIES ########
#from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'Purify_96_sample',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/02/09',
    'description': '1.5x SPRI beads purification of DNA',
}
#### IMPORT LIBRARIES ####
from opentrons import labware, instruments, modules, robot

elution_plate = labware.load('96-flat', '3')
trough = labware.load('trough-12row', '9')
mag_deck = modules.load('magdeck', '7')
mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)

tipracks_300 = [labware.load('tiprack-200ul', slot, share=True)
                for slot in ['1','2','4','5','6	']]

# pipette setup

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks_300)

SPRI_beads = trough.wells('A1')
ethanol = trough.wells('A2')
elution_buffer = trough.wells('A3')
liquid_trash = trough.wells('A12')
liquid_trash = trough.wells('A11')
liquid_trash = trough.wells('A10')

sample_vol = 50
bead_vol = sample_vol * 1.5
remove_vol = sample_vol + bead_vol
ethanol_vol = 3.5 * sample_vol
elution_vol = 40

# Purification

robot.comment("All hands hoay! Purification begins.")

mag_deck.disengage()

m300.transfer(bead_vol, SPRI_beads, mag_plate.cols , mix_before=(2,100),mix_after=(4,50), blow_out =True, new_tip='always', trash=False)
m300.delay(minutes=1)
#Incubate at room temperature for 5 min.

mag_deck.engage()
m300.delay(minutes=5)

m300.reset()
m300.transfer(remove_vol, mag_plate.cols(), liquid_trash, new_tip='always', blow_out =True)
mag_deck.disengage()

m300.transfer(ethanol_vol, ethanol, mag_plate.cols, mix_after=(3,150), air_gap=20, blow_out =True, new_tip='always')

mag_deck.engage()
m300.delay(minutes=1)
m300.transfer(200, mag_plate.cols(), liquid_trash, air_gap=20, new_tip='always')

m300.delay(minutes=4)
mag_deck.disengage()

m300.transfer(elution_vol, elution_buffer, mag_plate.cols(), new_tip='once')

m300.delay(minutes=15)

mag_deck.engage()
m300.delay(minutes=2)

m300.transfer(elution_vol, mag_plate.cols(), elution_plate.cols(), new_tip='always')

