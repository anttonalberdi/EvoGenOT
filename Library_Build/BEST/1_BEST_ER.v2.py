##########################
### BEST Library build ###
##########################

## Description of procedure
#
#                           x1          x96(+10) #the extra amount shoud be optimised based on robot behavior
# T4 DNA ligase buffer	    4           424
# Reaction enhancer	        2.2         233.2
# T4 PNK	                1           106
# T4 polymerase	            0.4         42.4
# dNTP 25 mM	            0.4         42.4
# Mix                       8           848
# Sample                    32
# Total                     40
#
# 1) Pre-mix buffers in 1.5ml tube and distribute to strip tubes (B-Str) #Should be done before and keep frozen
#      T4 DNA ligase buffer	 424
#      Reaction enhancer     233.2
#      dNTP 25 mM	         42.4
#      Total                 699.6
#      For each well         87.45
#
# 2) Pre-mix enzymes in 1.5ml tube and distribute to strip tubes (E-Str) #Should be done before and keep frozen
#       T4 PNK	             106
#       T4 polymerase	     42.4
#       Total                148.4
#       For each well        18.55
#
# 3) Place B-Str in Column 1 of chill_rack_96 and E-Str in Column 3 of chill_rack_96 #Open the leads just before starting the protocol
#
# 4) Place the plate (biorad-hardshell-96-PCR) with the 96 samples in the tempdeck. NEED TO DECIDE ON THE FOIL! X-CROSSED?
#
# ROBOT PROTOCOL BEGINS
#
# 5) Transfer 87.45 ul from B-Str to E-Str (total should be around 77 ul) and mix well
#
# 6) Distribute 8 ul to each column in the plate and mix thoroughly (each well should have ca 30 ul and there should be around 7ul spare mix in the strip-tube)
#
# ROBOT PROTOCOL ENDS
#
# 7) Seal the plate with thin aluminium foil
#
# 8) Incubate the plate 30 min 20 ºC, 30 min 65 ºC
#
###########
#
#	Good Luck!
#
#
######## IMPORT LIBRARIES ########
from opentrons import protocol_api


#### METADATA ####

metadata = {
    'protocolName': 'BEST_Lib_build_96_sample',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'apiLevel': '2.0',
    'description': 'End Repair of Automated single tube library preperation after Carøe et al. 2017',
    }

def run(protocol):

    #### LABWARE SETUP ####
    temp_deck_1 = protocol.load_module('tempdeck', '4')
    temp_deck_2 = protocol.load_module('tempdeck', '10')

    temp_deck_1._port = '/dev/ttyACM0'
    temp_deck_2._port = '/dev/ttyACM1'


    cold_plate = temp_deck_1.load_labware('biorad_96_wellplate_200ul_pcr')
    # trough = labware.load('trough-12row', '2')
    # Trash = labware.load('One-Column-reservoir','3')
    temp_plate = temp_deck_2.load_labware('96_wellplate_200ul_covaris')
    #mag_deck = modules.load('magdeck', '7')
    #mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)

    tipracks_10_1 = protocol.load_labware('opentrons_96_filtertiprack_10ul', '5')
    tipracks_10_2 = protocol.load_labware('opentrons_96_filtertiprack_10ul', '8')

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '9')
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', '11')




    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi', mount='left', tip_racks=(tipracks_200_1,tipracks_200_2))

    m10 = protocol.load_instrument('p10_multi', mount='right', tip_racks=(tipracks_10_1, tipracks_10_2))

    ## Enzyme SETUP
    Enzyme_ER = cold_plate['A1']
    # Enzyme_Lig = Cold_plate.wells('A2')
    # Enzyme_Fill = Cold_plate.wells('A3')

    ## Reagent SETUP
    ER_mastermix = cold_plate['A4']
    # BGI_adapter = Cold_plate.wells('A5')
    # Lig_mastermix = Cold_plate.wells('A6')
    # Fill_mastermix = Cold_plate.wells('A7')

    ## Purification reagents SETUP
    # SPRI_beads = trough.wells('A8')
    # ethanol = trough.wells('A9')
    # elution_buffer = trough.wells('A10')
    # Liquid_trash = Trash.wells('A1')

    ## Sample Setup
    sample_number = 96
    col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
    samples = [col for col in temp_plate.columns()[:col_num]]

    ## Volume setup
    ER_vol = 8
    #Lig_vol = 8
    #Fill_vol = 10
    MM_dist_ER = ER_vol * col_num
    #MM_dist_Lig = Lig_vol * col_num
    #MM_dist_Fill = Fill_vol * col_num



    """
    Blund end repair
    """
    protocol.comment("Yay! \ Blund-end Repair begins.")

    temp_deck_1.set_temperature(10)
    temp_deck_2.set_temperature(10)

    ### Addition of End repair mastermix to enzymes

    m300.flow_rate.aspirate = 180
    m300.flow_rate.dispense = 180
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(ER_mastermix.bottom())
    m300.mix(3, 50, ER_mastermix.bottom(4))
    m300.flow_rate.aspirate = 25
    m300.flow_rate.dispense = 25
    m300.aspirate(MM_dist_ER,ER_mastermix.bottom(1))
    m300.move_to(Enzyme_ER.bottom())
    m300.dispense(MM_dist_ER,Enzyme_ER.bottom(4))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.mix(5, 30, Enzyme_ER.bottom(4))
    protocol.delay(seconds=5)
    m300.move_to(Enzyme_ER.top(-4))
    m300.return_tip()

    ### Addition of End repair mastermix to libraries

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A1']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A1'].bottom())
    m10.dispense(ER_vol, temp_plate['A1'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A1'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A1'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A2']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A2'].bottom())
    m10.dispense(ER_vol, temp_plate['A2'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A2'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A2'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A3']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A3'].bottom())
    m10.dispense(ER_vol, temp_plate['A3'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A3'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A3'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A4']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A4'].bottom())
    m10.dispense(ER_vol, temp_plate['A4'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A4'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A4'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A5']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A5'].bottom())
    m10.dispense(ER_vol, temp_plate['A5'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A5'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A5'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A6']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A6'].bottom())
    m10.dispense(ER_vol, temp_plate['A6'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A6'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A6'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A7']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A7'].bottom())
    m10.dispense(ER_vol, temp_plate['A7'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A7'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A7'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A8']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A8'].bottom())
    m10.dispense(ER_vol, temp_plate['A8'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A8'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A8'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A9']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A9'].bottom())
    m10.dispense(ER_vol, temp_plate['A9'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A9'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A9'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A10']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A10'].bottom())
    m10.dispense(ER_vol, temp_plate['A10'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A10'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A10'].top(-4))
    m10.return_tip()


    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A11']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A11'].bottom())
    m10.dispense(ER_vol, temp_plate['A11'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A11'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A11'].top(-4))
    m10.return_tip()

    m10.flow_rate.aspirate = 180
    m10.flow_rate.dispense = 180
    m10.pick_up_tip(tipracks_10_1['A12']) # Slow down head speed 0.5X for bead handling
    m10.mix(3, 10, Enzyme_ER)
    m10.flow_rate.aspirate = 25
    m10.flow_rate.dispense = 25
    m10.aspirate(ER_vol, Enzyme_ER.bottom(1))
    m10.move_to(temp_plate['A12'].bottom())
    m10.dispense(ER_vol, temp_plate['A12'].bottom(3))
    m10.flow_rate.aspirate = 50
    m10.flow_rate.dispense = 50
    m10.mix(5, 10, temp_plate['A12'].bottom(2))
    protocol.delay(seconds=5)
    m10.flow_rate.aspirate = 100
    m10.flow_rate.dispense = 100
    m10.move_to(temp_plate['A12'].top(-4))
    m10.return_tip()



    protocol.pause("Yay! \ Please incubate in PCR machine \ at 20°C for 30 minutes, followed by 30 minutes at 65°C. \ Press resume when finished.")

    temp_deck_1.deactivate()
    temp_deck_2.deactivate()
