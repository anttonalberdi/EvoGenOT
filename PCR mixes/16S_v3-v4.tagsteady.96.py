####################################
# PCR MIX PROTOCOL FOR OPENTRONS 2 #
####################################

#############
# Mastermix #
#############
#             1x        96x
# ddH20       13.50     1296
# 10x buffer  2.5       240
# MgCl2       2.5       240
# BSA         1.5       144
# dNTP        0.5       48
# TaqGold     0.5       48

#####################
# To be added later #
#####################
# Primer-F    1
# Primer-R    1
# DNA         2
####################

from opentrons import labware, instruments, modules, robot

# METADATA
metadata = {
    'protocolName': '16S_v3-v4.tagsteady.96',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'date': '2019/02/05',
    'description': 'PCR mix for 16S rRNA (v3-v4) metabarcoding of bacteria',
    'primers': 'Forward: 341F (CCTAYGGGRBGCASCAG), Reverse: R806 (GGACTACNNGGGTATCTAAT)',
}


# LABWARE
elution_plate = labware.load('96-flat', '3')

# PIPETTES
m300 = instruments.P300_Multi(mount='left', tip_racks=tipracks_300)






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
