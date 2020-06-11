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
    'apiLevel': '2.0',
    'description': 'Purification procedure of Automated single tube library preparation after Carøe et al. 2017',
    }

def run(protocol):
    #### LABWARE SETUP ####
    mag_deck = protocol.load_module('magdeck', 10)


    trough = protocol.load_labware('usascientific_12_reservoir_22ml', 7)                       # to add proper model of labware from https://labware.opentrons.com/
    trash_box = protocol.load_labware('agilent_1_reservoir_290ml', 8)            # to add proper model of labware
    mag_plate = mag_deck.load_labware('biorad_96_wellplate_200ul_pcr')
    elution_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1)

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
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

    ## Plate SETUP

    MA1 = mag_plate['A1']
    MA2 = mag_plate['A2']
    MA3 = mag_plate['A3']
    MA4 = mag_plate['A4']
    MA5 = mag_plate['A5']
    MA6 = mag_plate['A6']
    MA7 = mag_plate['A7']
    MA8 = mag_plate['A8']
    MA9 = mag_plate['A9']
    MA10 = mag_plate['A10']
    MA11 = mag_plate['A11']
    MA12 = mag_plate['A12']

    ## Sample Setup
    sample_number = 96
    col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
    samples = [col for col in mag_plate.columns()[:col_num]]

    #### VOLUME SETUP

    sample_vol = 50
    bead_vol = 1.5*sample_vol
    EtOH_vol = 160
    EtOH_vol2 = 150
    Elution_vol = 35

    #### PROTOCOL ####
    ### Beads addition
    mag_deck.disengage()                   # or mag_mod.disengage() ???

    #### Transfer beads to MA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A1']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis                 ==> see end of protocol for info (if need to add them)
    # robot.head_speed                   ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA1.bottom(1))
    m300.dispense(bead_vol, MA1.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA1.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA1.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A2']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA2.bottom(1))
    m300.dispense(bead_vol, MA2.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA2.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA2.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A3']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA3.bottom(1))
    m300.dispense(bead_vol, MA3.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA3.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA3.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A4']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA4.bottom(1))
    m300.dispense(bead_vol, MA4.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA4.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA4.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A5']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA5.bottom(1))
    m300.dispense(bead_vol, MA5.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA5.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA5.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A6']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA6.bottom(1))
    m300.dispense(bead_vol, MA6.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA6.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA6.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA7
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A7']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA7.bottom(1))
    m300.dispense(bead_vol, MA7.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA7.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA7.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA8
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A8']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA8.bottom(1))
    m300.dispense(bead_vol, MA8.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA8.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA8.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA9
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A9']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA9.bottom(1))
    m300.dispense(bead_vol, MA9.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA9.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA9.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA10
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A10']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA10.bottom(1))
    m300.dispense(bead_vol, MA10.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA10.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA10.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA11
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A11']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA11.bottom(1))
    m300.dispense(bead_vol, MA11.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA11.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA11.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    #### Transfer beads to MA12
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A12']) # Slow down head speed 0.5X for bead handling
    m300.move_to(SPRI_beads.top(-30))
    m300.mix(3, bead_vol, SPRI_beads.bottom(2))
    # max_speed_per_axis    ==> see end of protocol for info
    # robot.head_speed      ==> see end of protocol for info
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(bead_vol, SPRI_beads.bottom(2))
    m300.move_to(MA12.bottom(1))
    m300.dispense(bead_vol, MA12.bottom(4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, bead_vol, MA12.bottom(4))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.move_to(MA12.top(-4))
    m300.blow_out()
    # max_speed_per_axis
    # robot.head_speed
    m300.return_tip()

    protocol.comment("Incubating the beads and PCR products at room temperature \
    for 5 minutes. Protocol will resume automatically.")

    protocol.delay(minutes=5)
    mag_deck.engage()           # or mag_mod.engage()
    protocol.delay(minutes=2)

    ### Remove supernatant, by re-using tiprack 1
    ### remove supernatant from MA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A1']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA1.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A2']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA2.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A3']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA3.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A4']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA4.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A5']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA5.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A6']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA6.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA7
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A7']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA7.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA8
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A8']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA8.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA9
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A9']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA9.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA10
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A10']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA10.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA11
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A11']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA11.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA12
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_1['A12']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(180, MA12.bottom(1))
    m300.dispense(180, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### Wash 1 with Ethanol, using tiprack 2
    ### Transfer Wash 1 to MA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A1']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA1.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA1.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA1.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A2']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA2.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA2.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA2.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A3']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA3.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA3.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA3.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A4']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA4.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA4.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA4.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A5']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA5.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA5.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA5.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A6']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA6.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA6.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA6.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA7
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A7']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA7.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA7.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA7.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA8
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A8']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA8.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA8.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA8.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA9
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A9']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA9.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA9.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA9.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA10
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A10']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA10.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA10.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA10.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA11
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A11']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA11.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA11.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA11.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 1 to MA12
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A12']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(EtOH_vol, EtOH1.top(-12))
    m300.dispense(EtOH_vol, MA12.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol, MA12.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA12.top(-10))
    m300.blow_out()
    m300.return_tip()

    mag_deck.engage(height=16)    # or mag_mod ?
    protocol.delay(minutes=2)

    ### Remove supernatant, by re-using tiprack 2
    ### remove supernatant from MA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A1']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA1.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A2']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA2.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A3']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA3.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A4']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA4.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A5']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA5.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A6']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA6.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA7
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A7']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA7.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA8
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A8']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA8.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA9
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A9']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA9.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA10
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A10']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA10.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA11
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A11']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA11.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA12
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_2['A12']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol, MA12.bottom(1))
    m300.dispense(EtOH_vol, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### Wash 2 with Ethanol, using tiprack 3
    ### Transfer Wash 2 to MA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A1']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA1.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA1.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA1.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A2']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA2.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA2.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA2.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A3']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA3.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA3.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA3.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A4']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA4.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA4.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA4.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A5']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA5.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA5.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA5.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A6']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA6.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA6.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA6.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA7
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A7']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA7.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA7.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA7.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA8
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A8']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA8.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA8.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA8.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA9
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A9']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA9.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA9.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA9.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA10
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A10']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA10.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA10.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA10.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA11
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A11']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA11.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA11.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA11.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 2 to MA12
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A12']) # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH2.top(-16))
    m300.aspirate(EtOH_vol2, EtOH2.top(-12))
    m300.dispense(EtOH_vol2, MA12.top(-4))
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.mix(5, EtOH_vol2, MA12.bottom(5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.move_to(MA12.top(-10))
    m300.blow_out()
    m300.return_tip()

    mag_deck.engage(height=16)    # or mag_mod ?
    protocol.delay(minutes=2)

    ### Remove supernatant, by re-using tiprack 3
    ### remove supernatant from MA1
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A1']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA1.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA2
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A2']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA2.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA3
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A3']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA3.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA4
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A4']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA4.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA5
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A5']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA5.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA6
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A6']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA6.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA7
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A7']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA7.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA8
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A8']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA8.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA9
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A9']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA9.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA10
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A10']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA10.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA11
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A11']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA11.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ### remove supernatant from MA12
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.pick_up_tip(tipracks_200_3['A12']) # Slow down head speed 0.5X for bead handling
    m300.aspirate(EtOH_vol2, MA12.bottom(1))
    m300.dispense(EtOH_vol2, trash_box['A1'].top(-5))
    protocol.delay(seconds=5)
    m300.flow_rate.aspirate = 130
    m300.flow_rate.dispense = 130
    m300.blow_out(trash_box['A1'].top(-5))
    m300.return_tip()

    ## Dry beads before elution
    #protocol.delay(minutes=4)

# #   for target in samples:
#        m300.flow_rate.aspirate = 180
#        m300.flow_rate.dispense = 180
#        m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
#        m300.flow_rate.aspirate = 40
#        m300.flow_rate.dispense = 40
#        m300.transfer(Elution_vol, Elution_buffer, target.top(-2), air_gap=0, new_tip='never')
#        m300.flow_rate.aspirate = 50
#        m300.flow_rate.dispense = 50
#        m300.mix(3, 100, target.bottom(6))
#        m300.delay(seconds=5)
#        m300.move_to(target.top(-3))
#        m300.blow_out()
#        m300.return_tip()



    ### Incubate elutes for 15 minutes at room temperature
#    protocol.pause("Please, incubate samples for 10 min at 37ºC and press resume after it")

    ### Transfer elutes to new plates.
    ### Transfer Elution buffer to elution_plate A1
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A1'])
#    m300.aspirate(Elution_vol, MA1.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A1'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A1'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A2
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A2'])
#    m300.aspirate(Elution_vol, MA2.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A2'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A2'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A3
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A3'])
#    m300.aspirate(Elution_vol, MA3.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A3'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A3'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A4
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A4'])
#    m300.aspirate(Elution_vol, MA4.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A4'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A4'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A5
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A5'])
#    m300.aspirate(Elution_vol, MA5.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A5'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A5'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A6
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A6'])
#    m300.aspirate(Elution_vol, MA6.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A6'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A6'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A7
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A7'])
#    m300.aspirate(Elution_vol, MA7.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A7'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A7'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A8
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A8'])
#    m300.aspirate(Elution_vol, MA8.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A8'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A8'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A9
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A9'])
#    m300.aspirate(Elution_vol, MA9.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A9'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A9'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A10
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A10'])
#    m300.aspirate(Elution_vol, MA10.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A10'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A10'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A11
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A11'])
#    m300.aspirate(Elution_vol, MA11.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A11'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A11'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

    ### Transfer Elution buffer to elution_plate A12
#    m300.flow_rate.aspirate = 50
#    m300.flow_rate.dispense = 50
#    m300.pick_up_tip(tipracks_200_4['A12'])
#    m300.aspirate(Elution_vol, MA12.bottom(1))
#    m300.dispense(Elution_vol, elution_plate['A12'].bottom(2))
#    protocol.delay(seconds=5)
#    m300.flow_rate.aspirate = 130
#    m300.flow_rate.dispense = 130
#    m300.move_to(elution_plate['A12'].top(-10))
#    m300.blow_out()
#    m300.return_tip()

#    mag_deck.disengage()    # or mag_mod ?

#    protocol.pause("Yay! \ Purification has finished \ Please store purified libraries as -20°C \ Press resume when finished.")


# max_speed_per_axis not reported, as in the other v2 protocols. Do we use the default ones?
# DEFAULT:
# X_MAX_SPEED = 600
# Y_MAX_SPEED = 400
# Z_MAX_SPEED = 125
# A_MAX_SPEED = 125
# B_MAX_SPEED = 40
# C_MAX_SPEED = 40
# Version_1 ==>             max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
# Same for head_speed ==>   robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
