from opentrons import protocol_api

##########################
### Library build ###
##########################

## Author Jonas Greve Lauritsen
## Not complete*

#### METADATA ####

metadata = {
    'protocolName': 'Protocol_LibraryBuild_OT2',
    'apiLevel': '2.7',
    'author': 'Jonas Greve Lauritsen <jonas.lauritsen@sund.ku.dk>',
    'description': 'Automated library preparation of DNA samples (96 version)'
    }

def run(protocol: protocol_api.ProtocolContext):

    #### LABWARE SETUP ####
    ## Placement of smart and dumb labware.

    ## Smart labware, thermocycler and temperature modules.
    thermo_module = protocol.load_module('thermocycler')
    cold_module = protocol.load_module('temperature module',1) 

    ## Sample Plate - Placed in thermocycler
    Sample_plate = thermo_module.load_labware('biorad_96_wellplate_200ul_pcr')

    ## Tip racks (3x 10 µL)
    tiprack_10_1 = protocol.load_labware('opentrons_96_tiprack_10ul',9)
    tiprack_10_2 = protocol.load_labware('opentrons_96_tiprack_10ul',6)
    tiprack_10_3 = protocol.load_labware('opentrons_96_tiprack_10ul',3)

    ## Mastermix Setup
    cold_plate = cold_module.load_labware('opentrons_96_aluminumblock_nest_wellplate_100ul')

    MasterMix1 = cold_plate.wells()[0]
    MasterMix2 = cold_plate.wells()[12]
    MasterMix3 = cold_plate.wells()[24]
    MasterMix4 = cold_plate.wells()[36]

    ## Sample Setup
    sample_number = 96
    col_num = 12
    column = [0,8,16,24,32,40,48,56,64,72,80,88] #First 'well number' in a column



    #### PIPETTE SETUP ####
    m20 = protocol.load_instrument('p20_multi_gen2', mount='right', tip_racks=(tiprack_10_1,tiprack_10_2,tiprack_10_3))


    #### Lab Work Protocol ####
    ## The instructions for the robot to execute.
    protocol.comment("STATUS: Activating Modules")

    ## Activating temperature module
    cold_module.set_temperature(4)

    ## Initial set up of thermocycler module
    thermo_module.set_block_temperature(4)
    thermo_module.set_lid_temperature(105)
    thermo_module.open_lid()

    ### First round ###

    protocol.comment("STATUS: First library step begun")

    ## Transfering mastermix

    for i in range(col_num):
        ## Position / Settings
        sample=column[i]
        m20.flow_rate.aspirate = 2                      #µL/s
        m20.flow_rate.dispense = 2                      #µL/s

        ## Aspiration, mixing, and dispersion
        m20.pick_up_tip(tiprack_10_1.wells()[sample])
        m20.mix(2, 10, MasterMix1)
        m20.aspirate(5, MasterMix1)                         #µL
        m20.move_to(MasterMix1.top())
        protocol.delay(20)                                  #s
        m20.dispense(5,Sample_plate.wells()[sample])        #µL
        m20.mix(2, 10, Sample_plate.wells()[sample])
        m20.move_to(Sample_plate.wells()[sample].top())
        protocol.delay(20)                                  #s
        m20.return_tip()

    ## Thermocycling incubation
    protocol.comment("STATUS: First incubation step begun")

    thermo_module.close_lid()
    thermo_module.set_lid_temperature(105)
    profile = [
        {'temperature':20, 'hold_time_minutes':30},
        {'temperature':30, 'hold_time_minutes':30}]
    thermo_module.execute_profile(steps=profile,repetitions=1,block_max_volume=25)
    thermo_module.open_lid()


    ##### Early stop - remove later #####
    protocol.pause("Protocol Completed.")

    thermo_module.deactivate()
    cold_module.deactivate()


    ### Second round ###

    protocol.comment("STATUS: Second library step begun")

    ## Transfering mastermix

    for i in range(col_num):
        ## Position / Settings
        sample=column[i]
        m20.flow_rate.aspirate = 2                      #µL/s
        m20.flow_rate.dispense = 2                      #µL/s

        ## Aspiration, mixing, and dispersion
        m20.pick_up_tip(tiprack_10_2.wells()[sample])
        protocol.delay()
        m20.mix(2, 10, MasterMix2)
        m20.aspirate(5, MasterMix2)                     #µL
        protocol.delay(20)                                   #s
        m20.dispense(5,Sample_plate.wells()[sample])   #µL
        m20.mix(2, 10, Sample_plate.wells()[sample])
        protocol.delay(20)                              #s
        m20.return_tip()


    ## Thermocycling incubation
    protocol.comment("STATUS: Second incubation step begun")

    thermo_module.close_lid()
    thermo_module.set_lid_temperature(80)
    profile = [
        {'temperature':20, 'hold_time_minutes':30},
        {'temperature':20, 'hold_time_minutes':30}]
    thermo_module.execute_profile(steps=profile,repetitions=1,block_max_volume=25)
    thermo_module.open_lid()



    ### Third round ###

    protocol.comment("STATUS: Third library step begun")

    ## Transfering Mastermix

    for i in range(col_num):
        ## Position / Settings
        sample=column[i]
        m20.flow_rate.aspirate = 2                      #µL/s
        m20.flow_rate.dispense = 2                      #µL/s

        ## Aspiration, mixing, and dispersion
        m20.pick_up_tip(tiprack_10_3.wells()[sample])
        protocol.delay()
        m20.mix(2, 10, MasterMix3)
        m20.aspirate(5, MasterMix3)                     #µL
        protocol.delay(20)                                   #s
        m20.dispense(5,Sample_plate.wells()[sample])   #µL
        m20.mix(2, 10, Sample_plate.wells()[sample])
        protocol.delay(20)                              #s
        m20.return_tip()

    ## Thermocycling incubation
    protocol.comment("STATUS: Third incubation step begun")

    thermo_module.close_lid()
    thermo_module.set_lid_temperature(80)
    profile = [
        {'temperature':20, 'hold_time_minutes':30},
        {'temperature':20, 'hold_time_minutes':30}]
    thermo_module.execute_profile(steps=profile,repetitions=1,block_max_volume=25)
    thermo_module.open_lid()



    ## Protocol finished
    protocol.pause("STATUS: Protocol Completed.")

    thermo_module.deactivate()
    cold_module.deactivate()


    ####### Old Code ########


    """
    #Blunt end repair
    """
    #protocol.comment("Yay! \ Blunt-end Repair begins.")

    #temp_deck_1.set_temperature(10)
    #temp_deck_2.set_temperature(10)

    ### Addition of End repair mastermix to enzymes

    #m300.flow_rate.aspirate = 180
    #m300.flow_rate.dispense = 180
    #m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    #m300.move_to(ER_mastermix.bottom())
    #m300.mix(3, 50, ER_mastermix.bottom(4))
    #m300.flow_rate.aspirate = 25
    #m300.flow_rate.dispense = 25
    #m300.aspirate(MM_dist_ER,ER_mastermix.bottom(1))
    #m300.move_to(Enzyme_ER.bottom())
    #m300.dispense(MM_dist_ER,Enzyme_ER.bottom(4))
    #m300.flow_rate.aspirate = 50
    #m300.flow_rate.dispense = 50
    #m300.mix(5, 30, Enzyme_ER.bottom(4))
    #protocol.delay(seconds=5)
    #m300.move_to(Enzyme_ER.top(-4))
    #m300.return_tip()

    ### Addition of End repair mastermix to libraries

    #for i in list_of_cols:

        #m10.flow_rate.aspirate = 180
        #m10.flow_rate.dispense = 180
        #m10.pick_up_tip(tipracks_10_1[i]) # Slow down head speed 0.5X for bead handling
        #m10.mix(3, 10, Enzyme_ER)
        #m10.flow_rate.aspirate = 25
        #m10.flow_rate.dispense = 25
        #m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
        #m10.move_to(temp_plate[i].bottom())
        #m10.dispense(ER_vol, temp_plate[i].bottom(3))
        #m10.flow_rate.aspirate = 50
        #m10.flow_rate.dispense = 50
        #m10.mix(5, 10, temp_plate[i].bottom(2))
        #protocol.delay(seconds=5)
        #m10.flow_rate.aspirate = 100
        #m10.flow_rate.dispense = 100
        #m10.move_to(temp_plate[i].top(-4))
        #m10.return_tip()
