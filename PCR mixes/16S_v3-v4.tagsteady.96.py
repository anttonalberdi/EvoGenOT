####################################
# PCR MIX PROTOCOL FOR OPENTRONS 2 #
####################################

#By: Antton Alberdi
#Version: 1.0
#Date: 2019/02/05

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
