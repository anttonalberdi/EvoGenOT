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

    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left', tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3, tipracks_200_4))
            # From the v1 the mount is right, but all the other protocols switch from right in v1 to left in v2. Why? Also here?

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

    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']

    for i in list_of_cols:
        #### Transfer beads to mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.move_to(SPRI_beads.top(-30))
        m300.mix(3, bead_vol, SPRI_beads.bottom(2))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(bead_vol, SPRI_beads.bottom(2))
        m300.move_to(mag_plate[i].bottom(1))
        m300.dispense(bead_vol, mag_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, bead_vol, mag_plate[i].bottom(4))
        protocol.delay(seconds=5)
        # m300.flow_rate.aspirate = 100
        # m300.flow_rate.dispense = 100
        m300.move_to(mag_plate[i].top(-4))
        m300.blow_out(mag_plate[i].top(-4))
        # max_speed_per_axis
        # robot.head_speed
        m300.return_tip()


    protocol.comment("Incubating the beads and PCR products at room temperature \
    for 5 minutes. Protocol will resume automatically.")

    protocol.delay(minutes=5)
    mag_deck.engage()
    protocol.delay(minutes=2)

    for i in list_of_cols:
        ### Remove supernatant, by re-using tiprack 1
        ### remove supernatant from mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(180, mag_plate[i].bottom(1))
        m300.dispense(180, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.air_gap(height = 3)
        m300.return_tip()


    for i in list_of_cols:
        ### Wash 1 with Ethanol, using tiprack 2
        ### Transfer Wash 1 to mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        m300.move_to(EtOH1.top(-16))
        m300.aspirate(EtOH_vol, EtOH1.bottom(2))
        m300.dispense(EtOH_vol, mag_plate[i].top(-4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, wash_mix, mag_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        #m300.move_to(mag_plate[i].top(-4))
        m300.blow_out(mag_plate[i].top(-4))
        m300.air_gap(height = 3)
        # m300.touch_tip()
        m300.return_tip()

    mag_deck.engage(height=16)    # or mag_mod ?
    protocol.delay(minutes=2)

    for i in list_of_cols:
        ### Remove supernatant, by re-using tiprack 2
        ### remove supernatant from mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(EtOH_vol, mag_plate[i].bottom(1))
        m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.air_gap(height = 3)
        m300.drop_tip()


    for i in list_of_cols:
        ### Wash 2 with Ethanol, using tiprack 3
        ### Transfer Wash 2 to mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
        m300.move_to(EtOH2.top(-16))
        m300.aspirate(EtOH_vol2, EtOH2.bottom(2))
        m300.dispense(EtOH_vol2, mag_plate[i].top(-4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, wash_mix, mag_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        # m300.move_to(mag_plate[i].top(-4))
        m300.blow_out(mag_plate[i].top(-4))
        m300.air_gap(height = 3)
        # m300.touch_tip()
        m300.return_tip()


    mag_deck.engage(height=16)
    protocol.delay(minutes=2)

    for i in list_of_cols:
        ### Remove supernatant, by re-using tiprack 3
        ### remove supernatant from mag_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(EtOH_vol2, mag_plate[i].bottom(1))
        m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.air_gap(height = 3)
        m300.return_tip()


    # Dry beads before elution
    protocol.delay(minutes=4)

    for i in list_of_cols:
        ### Transfer Elution Buffer to mag_plate
        m300.flow_rate.aspirate = 40
        m300.flow_rate.dispense = 40
        m300.pick_up_tip(tipracks_200_4[i]) # Slow down head speed 0.5X for bead handling
        m300.move_to(Elution_buffer.top(-16))
        m300.aspirate(Elution_vol, Elution_buffer.bottom(2))
        m300.dispense(Elution_vol, mag_plate[i].top(-4))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.mix(3, Elution_vol, mag_plate[i].bottom(5))
        protocol.delay(seconds=5)
        # m300.move_to(mag_plate[i].top(-10))
        m300.blow_out(mag_plate[i].top(-10))
        m300.return_tip()

    ## Incubate elutes for 15 minutes at room temperature
    protocol.pause("Please, incubate samples for 10 min at 37ºC and press resume after it")

    for i in list_of_cols:
        ## Transfer elutes to new plates.
        ## Transfer Elution buffer to elution_plate
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_4[i])
        m300.aspirate(Elution_vol, mag_plate[i].bottom(1))
        m300.dispense(Elution_vol, elution_plate[i].bottom(2))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(elution_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    mag_deck.disengage()

    protocol.pause("Yay! \ Purification has finished \ Please store purified libraries as -20°C \ Press resume when finished.")
