############################
### Library Purification ###
############################

## Author Jonas Greve Lauritsen
## Automatic preparation of covaris plates based on csv input

############################

## User Input 
Col_Number = 12 # Number of columns with samples.



#############################

#### Package loading ####
from opentrons import protocol_api

#### Meta Data ####
metadata = {
    'protocolName': 'Purification of Library Build',
    'apiLevel': '2.12',
    'author': 'Jonas Lauritsen <jonas.lauritsen@sund.ku.dk>',
    'description': 'Automated purification of library builds'}

#### Protocol Script ####
def run(protocol: protocol_api.ProtocolContext):
    #### LABWARE SETUP ####
    ## Placement of smart and dumb labware.
    Magnet_module = protocol.load_module('magnetic_module',9)

    Library_plate = Magnet_module.load_labware('biorad_96_wellplate_200ul_pcr')
    Purified_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',11)

    ## Purification materials.
    Beads = protocol.load_labware('nest_12_reservoir_15ml',6)['A1']
    Ethanol = protocol.load_labware('nest_12_reservoir_15ml',6)['A2']
    EBT = protocol.load_labware('nest_12_reservoir_15ml',6)['A3']

    ## Tip racks (2x 10 µL, 2x 200 µl)
    tiprack_200 = protocol.load_labware('opentrons_96_filtertiprack_200ul',(1,2,3,4,5,7,8,10)) #Maybe it has to divided into several seperat potential.
    #tiprack_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul',11)
    #tiprack_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul',11)
    

    #### PIPETTE SETUP ####
    ## Loading pipettes
    m200 = protocol.load_instrument('p300_multi_gen2', mount='right', tip_racks=(tiprack_200))

    
    #### Lab Work Protocol ####
    ## Addition of Magnetic beadsLoop for mixing samples and moving to  cherrypicking samples
    for i in range(Col_Number):
        ## Variable definitions for the functions - increases readability of the script.
        Column = i*8 #Gives the index of the first well in the column
        m200.transfer(volume = 75, source = Beads, dest = Library_plate[Column], new_tip = 'always', mix_before = (3,75), mix_after = (8,90), blow_out = True, blowout_location = Library_plate[Column])
    
    ## 5 minutes incubation at room temperature
    protocol.delay(minutes=5) 

    ## Engaging magnetic module
    Magnet_module.engage()

    ## Removing supernatant
    for i in range(Col_Number):
        ## Variable definitions for the functions - increases readability of the script.
        Column = i*8 #Gives the index of the first well in the column
        m200.transfer(volume = 150, source = Library_plate[Column], dest = 'trash', new_tip = 'always')

    ## Ethanol washing
    for k in range(2): # Repeating the wash
        for i in range(Col_Number):
            Column = i*8 #Gives the index of the first well in the column
            m200.transfer(volume = 200, source = Ethanol, dest = Library_plate[Column], new_tip = 'always')
            m200.transfer(volume = 220, source = Library_plate[Column], dest = 'trash', new_tip = 'always')

    ## Drying beads (5 mins) 
    protocol.delay(minutes = 5)

    ## Disengaging magnet
    Magnet_module.disengage()

    ## Adding EBT buffer
    for i in range(Col_Number):
        Column = i*8 #Gives the index of the first well in the column
        m200.transfer(volume = 40, source = EBT, dest = Library_plate[Column], new_tip = 'always',mix_after = (3,35), blow_out=True, blowout_location = Library_plate[Column])

    ## Incubation of library plate.
    protocol.pause('Seal library plate and spin down the plate shortly. Incubate the library plate for 5 min at 55 C. Press RESUME, when library plate has been replaced in the magnet module.')
    
    ## Engaging Magnet
    Magnet_module.engage()

    ## Transferring purified library to a new plate (purified plate).
    for i in range(Col_Number):
        Column = i*8 #Gives the index of the first well in the column
        m200.transfer(volume = 40, source = Library_plate[Column], dest = Purified_plate[Column], new_tip = 'always')

    ## Deactivating magnet module
    Magnet_module.deactivate()

    protocol.comment("STATUS: Protocol Completed.")
