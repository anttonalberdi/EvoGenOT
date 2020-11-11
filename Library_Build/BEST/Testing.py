#######################################
### BEST Library build Purification ###
#######################################

## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Ensure samples are room temperature and place libraries in magnetic module
# 	2. Ensure SPRI beads are room temperature
#   3. Make freshly made 80% Ethanol for purification
#   4. Distribute:
#                   SPRI beads to Column 1,
#                   Ethanol to Column 2 and 3
#                   Elution Buffer to Column 12
#
# Procedure
#
#		Purification
# 	1.	Distribute 1.5x beads to library and mixes
#	2.	Removes supernatant and adds ethanol for washing, washing will be processed twice
#   3.  Beads will air dry for 4 minutes and 35µl elution buffer will be added
#	4.	Elutes will incubate for 15 minutes at room temperature and be eluted to a new plate in slot 1
#
#	Good Luck!
#
######## IMPORT LIBRARIES ########
from opentrons import protocol_api

#### METADATA ####

metadata = {
    'protocolName': 'BEST_Purification',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'update': 'Martina Cardinali <martina.cardinali.4@gmail.com'
    'apiLevel': '2.2',
    'description': 'Purification procedure of Automated single tube library preparation after Carøe et al. 2017',
    }

def run(protocol):
    #### LABWARE SETUP ####
    mag_deck = protocol.load_module('magdeck', 10)


    trough = protocol.load_labware('usascientific_12_reservoir_22ml', 7)                       # to add proper model of labware from https://labware.opentrons.com/
    trash_box = protocol.load_labware('agilent_1_reservoir_290ml', 8)            # to add proper model of labware
    mag_plate = mag_deck.load_labware('biorad_96_wellplate_200ul_pcr')
    elution_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 2)

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 1)
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)
    tipracks_200_4 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 6)
    tipracks_10_1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 3)
    tipracks_10_2 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 9)

    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                    tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3, tipracks_200_4))
    m20 = protocol.load_instrument('p20_multi_gen2', mount='right', tip_racks=(tipracks_10_1, tipracks_10_2))

    ## Purification reagents SETUP
    SPRI_beads = trough['A1']
    EtOH1 = trough['A2']
    EtOH2 = trough['A3']
    Elution_buffer = trough['A12']

    Liquid_trash = trash_box['A1']

    ## Sample Setup
    sample_number = 96
    col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
    samples = [col for col in mag_plate.columns()[:col_num]]

    #### VOLUME SETUP

    sample_vol = 50
    bead_vol = 1.5*sample_vol
    EtOH_vol = 120
    EtOH_vol2 = 120
    Elution_vol = 35
    wash_mix = 90
    #### PROTOCOL ####
    ### Beads addition
    mag_deck.disengage()

    #### Plate SETUP
    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    list_of_cols = ['A1','A2','A3','A4']

    #### Transfer beads to mag_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        #m300.move_to(SPRI_beads.top(-30))
        m300.mix(5, bead_vol, SPRI_beads.bottom(4))
        # max_speed_per_axis                 ==> see end of protocol for info (if need to add them)
        # robot.head_speed                   ==> see end of protocol for info
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(bead_vol, SPRI_beads.bottom(4))
        m300.move_to(mag_plate[i].bottom(1))
        m300.dispense(bead_vol, mag_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, bead_vol, mag_plate[i].bottom(4))
        protocol.delay(seconds=5)
        # m300.flow_rate.aspirate = 100
        # m300.flow_rate.dispense = 100
        m300.move_to(mag_plate[i].top(-4))
        m300.blow_out()
        m300.return_tip()


    protocol.comment("Incubating the beads and PCR products at room temperature \
    for 5 minutes. Protocol will resume automatically.")

    #protocol.delay(minutes=5)
    mag_deck.engage(22)
    #protocol.delay(minutes=2)

    ### Remove supernatant, by re-using tiprack 1
    ### remove supernatant from mag_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(200, mag_plate[i].bottom(0.5))
        m300.dispense(200, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.air_gap(height = 2)
        m300.drop_tip()


    for i in list_of_cols:
        ### Wash 1 with Ethanol, using tiprack 2
        ### Transfer Wash 1 to mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(EtOH_vol, EtOH1.bottom(4))
        m300.dispense(EtOH_vol, mag_plate[i].top(-4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, wash_mix, mag_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(mag_plate[i].top(-4))
        m300.blow_out()
        m300.return_tip()

    #protocol.delay(minutes=2)

    for i in list_of_cols:
        ### Remove supernatant after Wash1, by re-using tiprack 2
        ### remove supernatant from mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(180, mag_plate[i].bottom(0.5))
        m300.dispense(180, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.air_gap(height = 2)
        m300.drop_tip()


    for i in list_of_cols:
        ### Wash 2 with Ethanol, using tiprack 3
        ### Transfer Wash 2 to mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(EtOH_vol2, EtOH2.bottom(4))
        m300.dispense(EtOH_vol2, mag_plate[i].top(-4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, wash_mix, mag_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(mag_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    #protocol.delay(minutes=2)

    for i in list_of_cols:
        ### Remove supernatant after Wash2, by re-using tiprack 3
        ### remove supernatant from mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(200, mag_plate[i].bottom(0.5))
        m300.dispense(200, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.air_gap(height = 2)
        m300.drop_tip()

    ### Remove remaining supernatant of Wash 2 with pipette 20
    for i in list_of_cols:
        m20.flow_rate.aspirate = 100
        m20.flow_rate.dispense = 100
        m20.pick_up_tip(tipracks_10_1[i]) # Slow down head speed 0.5X for bead handling
        m20.aspirate(10, mag_plate[i].bottom(0.2))
        m20.dispense(10, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m20.flow_rate.aspirate = 130
        m20.flow_rate.dispense = 130
        m20.blow_out(trash_box['A1'].top(-5))
        m20.air_gap(height = 2)
        m20.return_tip()

    # Dry beads before elution
    #protocol.delay(minutes=4)
    mag_deck.disengage()

    for i in list_of_cols:
        ### Transfer Elution Buffer to mag_plate
        m300.flow_rate.aspirate = 40
        m300.flow_rate.dispense = 40
        m300.pick_up_tip(tipracks_200_4[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(Elution_vol, Elution_buffer.bottom(4))
        m300.dispense(Elution_vol, mag_plate[i].bottom(4))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.mix(5, 20, mag_plate[i].bottom(2))
        protocol.delay(seconds=5)
        m300.move_to(mag_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()


    ## Incubate elutes for 15 minutes at room temperature
    protocol.pause("Please, incubate samples for 10 min at 37ºC and press resume after it")
    mag_deck.engage(height=22)
    #protocol.delay(minutes=5)

    odd_cols = ['A1','A3']#,'A5','A7','A9','A11']
    even_cols = ['A2','A4']#,'A6','A8','A10','A12']

    from opentrons import types

    for i in odd_cols:
        m300.flow_rate.aspirate = 5
        m300.flow_rate.dispense = 5
        m300.pick_up_tip(tipracks_200_4[i])
        center_location = mag_plate[i].bottom(1.5)
        left_location = center_location.move(types.Point(x=-1.5, y=0, z=-1))
        m300.move_to(center_location)
        m300.aspirate(55, left_location)
        m300.dispense(55, elution_plate[i].bottom(2))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(elution_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    for i in even_cols:
        m300.flow_rate.aspirate = 5
        m300.flow_rate.dispense = 5
        m300.pick_up_tip(tipracks_200_4[i])
        center_location = mag_plate[i].bottom(1.5)
        right_location = center_location.move(types.Point(x=1.5, y=0, z=-1))
        m300.move_to(center_location)
        m300.aspirate(55, right_location)
        m300.dispense(55, elution_plate[i].bottom(2))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(elution_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    # for i in list_of_cols:
    #     m300.flow_rate.aspirate = 5
    #     m300.flow_rate.dispense = 5
    #     m300.pick_up_tip(tipracks_200_4[i])
    #     center_location = mag_plate[i].bottom(1.5)
    #     left_location = center_location.move(types.Point(x=-1.5, y=0, z=-1))
    #     right_location = center_location.move(types.Point(x=1.5, y=0, z=-1))
    #     for l in range(0, len(list_of_cols)):
    #         if l % 2:   # if the index is even, the col is odd
    #             m300.move_to(left_location)
    #             m300.aspirate(55)    # here the arm should move to left (1, 2 mm)
    #         else:       # if the index is odd, the col is even
    #             m300.move_to(right_location)
    #             m300.aspirate(55)   # here the arm should move to the right
    #     # continue toward the bottom of the well, probably we cannot use bottom for the aspirate
    #     # as it corresponds to the bottom-center of the well
    #     m300.dispense(55, elution_plate[i].bottom(2))
    #     protocol.delay(seconds=5)
    #     m300.flow_rate.aspirate = 130
    #     m300.flow_rate.dispense = 130
    #     m300.move_to(elution_plate[i].top(-10))
    #     m300.blow_out()
    #     m300.return_tip()

    mag_deck.disengage()    # or mag_mod ?

    protocol.pause("Yay! \ Purification has finished \ Please store purified libraries as -20°C \ Press resume when finished.")
