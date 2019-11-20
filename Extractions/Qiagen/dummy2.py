####### IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

# metadata
metadata = {
    'protocolName': 'DNA Purification',
    'author': 'Name <lassenyholm@gmail.com>',
    'description': 'DNA purification of PowerSoil/Fecal extracts (C1 and bead beating)',
}

### LABWARE SETUP ###

mag_deck = modules.load('magdeck', '7')


mag_deck.engage(height=20)
