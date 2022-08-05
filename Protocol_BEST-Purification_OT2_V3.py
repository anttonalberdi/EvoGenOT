#################################
### BEST Library Purification ###
#################################

## Author Jonas Greve Lauritsen
## Automatic preparation of covaris plates based on csv input

############################

## User Input
Col_Number = 6 # Number of columns with samples

#############################

#### Package loading ####
from opentrons import protocol_api

#### Meta Data ####
metadata = {
    'protocolName': 'Purification of Library Build',
    'apiLevel': '2.12',
    'author': 'Jonas Lauritsen <jonas.lauritsen@sund.ku.dk>',
    'description': 'Automated purification of a BEST library build. The user inputs the number of columns for purification.'}

#### Protocol Script ####
def run(protocol: protocol_api.ProtocolContext):
    #### LABWARE SETUP ####
    ## Smart labware
    magnet_module = protocol.load_module('magnetic module',4)

    ## Work plates
    Library_plate = magnet_module.load_labware('biorad_96_wellplate_200ul_pcr')
    Purified_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',10)

    ## Purification materials
    Resevoir = protocol.load_labware('nest_12_reservoir_15ml',1) # We use a 22 ml version: it is taller, but otherwise share the same dimensions.
    Beads = Resevoir['A1']
    Ethanol1 = Resevoir['A2']
    Ethanol2 = Resevoir['A3']
    EBT = Resevoir['A5']
    Waste1 = Resevoir['A12'] # Beads supernatant waste
    Waste2 = Resevoir['A11'] # 1st ethanol wash waste
    Waste3 = Resevoir['A10'] # 2nd ethanol wash waste

    ## Tip racks (2x 10 µL, 2x 200 µl)
    tiprack_10_1 = protocol.load_labware('opentrons_96_filtertiprack_10ul',6)
    tiprack_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul',7)
    tiprack_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul',2)
    tiprack_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul',5)
    tiprack_200_4 = protocol.load_labware('opentrons_96_filtertiprack_200ul',3)
    tiprack_200_5 = protocol.load_labware('opentrons_96_filtertiprack_200ul',8)
    tiprack_200_6 = protocol.load_labware('opentrons_96_filtertiprack_200ul',9)

    #### PIPETTE SETUP ####
    ## Loading pipettes
    m200 = protocol.load_instrument('p300_multi_gen2', mount='left', tip_racks=([tiprack_200_1,tiprack_200_2,tiprack_200_3,tiprack_200_4,tiprack_200_5,tiprack_200_6]))
    m20 = protocol.load_instrument('p20_multi_gen2', mount='right', tip_racks=([tiprack_10_1]))

    #### Beads drying time (seconds) ####
    ## Different drying times - Sat from the last removal of the first column. Total drying time is estimated to 4 mins 55 seconds (23s per pipetting cycle)
    BeadsTime = (295, 272, 249, 226, 203, 180, 157, 134, 111, 88, 65, 42)
    BeadsTime = BeadsTime[(Col_Number-1)] # Selecting the relevant drying time



    ############################### Lab Work Protocol ###############################
    ## The instructions for the robot to execute.
    protocol.comment("STATUS: Purification of BEST Library Build Begun")
    protocol.set_rail_lights(True)
    magnet_module.disengage()


    ## Addition of Magnetic beads - slowed pipette included.
    protocol.comment("STATUS: Beads Transfer Begun")
    for i in range(Col_Number):
        Column = i*8 #Gives the index of the first well in the column
        m200.pick_up_tip()
        m200.move_to(location = Beads.top())
        m200.move_to(location = Beads.bottom(), speed = 40)
        m200.mix(repetitions = 5, volume = 75, location = Beads)
        m200.aspirate(volume = 75, location = Beads, rate = 0.5)
        protocol.delay(5)
        m200.move_to(location = Beads.top(), speed = 10)
        m200.dispense(volume = 75, location = Library_plate.wells()[Column])
        m200.mix(repetitions = 5, volume = 90, location = Library_plate.wells()[Column])
        m200.dispense(volume = 100, location = Library_plate.wells()[Column], rate = 0.8) # Controlled 'blowout'
        protocol.delay(5)
        m200.move_to(location = Library_plate.wells()[Column].top(), speed = 40)
        m200.return_tip()

    ## 5 minutes incubation at room temperature
    protocol.comment("STATUS: Beginning Beads Incubation")
    protocol.delay(minutes = 5)

    ## Engaging magnetic module. 5 mins wait for beads attraction
    magnet_module.engage(height_from_base = 14)
    protocol.delay(minutes = 5)

    ## Discarding supernatant - to be tested: pipette positioning.
    protocol.comment("STATUS: Discarding Supernatant")
    for i in range(Col_Number):
        Column = i*8 #Gives the index of the first well in the column
        m200.pick_up_tip()
        m200.transfer(volume = 160, source = Library_plate.wells()[Column].bottom(z = 0.25), dest = Waste1.top(), new_tip = 'never', rate=0.5) #
        m200.air_gap(40,20)
        m200.return_tip()

    ## Double ethanol washing
    protocol.comment("STATUS: Ethanol Wash Begun")
    for k in range(2): # Double wash
        ## Setting up the wash variables
        if k == 0:
            Ethanol_Tips = tiprack_200_3
            Ethanol = Ethanol1
            Waste = Waste2
            protocol.comment("STATUS: First Wash Begun")
        if k == 1:
            Ethanol_Tips = tiprack_200_4
            Ethanol = Ethanol2
            Waste = Waste3
            protocol.comment("STATUS: Second Wash Begun")

        ## Adding Ethanol.
        m200.pick_up_tip(Ethanol_Tips.wells_by_name()['A1']) # Using 1 set of tips for all rows
        for i in range(Col_Number):
            Column = i*8 # Gives the index for the first well in the column
            #m200.pick_up_tip(Ethanol_Tips.wells()[Column])
            m200.mix(repetitions = 2, volume = 200, location = Ethanol)
            m200.aspirate(volume = 200, location = Ethanol,rate = 0.7)
            m200.dispense(volume = 220, location = Library_plate.wells()[Column].top(z = 1.5)) # Dispenses ethanol from 1.5 mm above the top of the well.
        m200.blow_out(location = Waste) # Blow out to remove potential droplets before returning.
        m200.return_tip()

        ## Removing Ethanol - reusing the tips from above (should eliminate droplet formation due to pre-wetting).
        for i in range(Col_Number):
            Column = i*8 # Gives the index for the first well in the column
            m200.pick_up_tip(Ethanol_Tips.wells()[Column])
            m200.aspirate(volume = 200, location = Library_plate.wells()[Column].bottom(z = 0.25),rate = 0.4)
            m200.dispense(volume = 240, location = Waste.top(z = 10), rate = 0.8) # With extra blowout volume
            m200.air_gap(40, 20) #take in excess, outside droplets to limit cross-contamination.
            m200.return_tip()

    ## Extra ethanol removal step to remove leftover ethanol before drying beads.
    for i in range(Col_Number):
        Column = i*8
        m20.pick_up_tip()
        m20.transfer(volume = 10, source = Library_plate.wells()[Column].bottom(z = -0), dest = Waste3.top(), rate = 0.6, new_tip = 'never')
        m20.air_gap(5, 20)
        m20.return_tip()
        # z = 0 is at the bottom of the labware - here we use a well plate that is slightly deeper than the specified labaware, but be extra careful if changed.


    ## Drying beads (5 mins)
    protocol.comment("STATUS: Drying Beads - time autoadjusted based on number of columns")
    protocol.delay(seconds = BeadsTime) #Times to be verified given m20 step.

    protocol.pause("Check ethanol level")

    ## Disengaging magnet
    magnet_module.disengage()

    ## Adding EBT buffer.
    protocol.comment("STATUS: EBT Buffer Transfer begun")
    for i in range(Col_Number):
        Column = i*8 #Gives the index for the first well in the column
        m200.pick_up_tip()
        m200.aspirate(volume = 40, location = EBT, rate = 1)
        m200.dispense(volume = 40, location = Library_plate.wells()[Column], rate = 1)
        m200.mix(repetitions = 5, volume = 30, location = Library_plate.wells()[Column])
        m200.dispense(volume = 40, location = Library_plate.wells()[Column], rate = 0.7)
        protocol.delay(5)
        m200.move_to(location = Library_plate.wells()[Column].top(), speed = 100)
        m200.return_tip()


    ## Incubation of library plate
    protocol.pause('ACTION: Seal library plate and spin it down shortly. Incubate the library plate for 10 min at 37*C. Press RESUME, when library plate has been returned (without seal) to the magnet module.')

    ## Engaging Magnet. 5 mins wait for beads withdrawal
    magnet_module.engage(height_from_base = 14)
    protocol.delay(minutes = 5)

    ## Transferring purified library to a new plate (purified plate). Transfer is sat higher to remove all.
    protocol.comment("STATUS: Transfer of Purified Library")
    for i in range(Col_Number):
        Column = i*8 #Gives the index for the first well in the column
        m200.transfer(volume = 50, source = Library_plate.wells()[Column].bottom(z = 0.2), dest = Purified_plate.wells()[Column], new_tip = 'always', trash = False, rate = 1)

    ## Deactivating magnet module
    magnet_module.disengage()

    ## Protocol finished
    protocol.set_rail_lights(False)
    protocol.comment("STATUS: Protocol Completed.")
