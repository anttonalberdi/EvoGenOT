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

####################################
# To be added later (to each well) #
####################################
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

# MODULES
temp_deck = modules.load('tempdeck', '9')
temp_plate = labware.load('opentrons-aluminum-block-2ml-eppendorf', '9', share=True)
temp_plate.set_temperature(4)
temp_deck.wait_for_temp()

# TIP RACKS
tipracks_300 = [labware.load('tiprack-200ul', slot, share=True) for slot in ['1','2','4','5','6	']]
tipracks_50 = [labware.load('tiprack-200ul', slot, share=True) for slot in ['1','2','4','5','6	']]

# PIPETTES
m300 = instruments.P300_Single(mount='left', tip_racks=tipracks_300)
s50 = instruments.P50_Multi(mount='right', tip_racks=tipracks_50)

# PROTOCOL

s50.transfer(100, temp_plate.wells('A1'), temp_plate.wells('B2'))

