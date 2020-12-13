## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Bead beat samples at maximum speed for 5 minutes (If needed do Proteinase K for digestion of tissue)
# 	2. Spin down samples 10.000 rpm for 1 minute
#	3. Transfer 200µl lysed sample to a deep well plate

### Procedure ###


######## IMPORT LIBRARIES ########
from opentrons import protocol_api

#### METADATA ####

metadata = {
    'protocolName': 'D-Rex RNA Extraction',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'update': 'Martina Cardinali <martina.cardinali.4@gmail.com>',
    'apiLevel': '2.2',
    'date': '2020/11/09',
    'description': 'Automation of D-Rex RNA protocol for stool samples in SHIELD',
}

def run(protocol):
    #### LABWARE SETUP ####
    elution_plate_RNA = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 1)
    trough = protocol.load_labware('usascientific_12_reservoir_22ml', 9)
    mag_deck = protocol.load_module('magdeck', 7)
    RNA_plate = mag_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')
    trash_box = protocol.load_labware('agilent_1_reservoir_290ml', 10)
    EtOH_wash = protocol.load_labware('agilent_1_reservoir_290ml', 6)

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 2)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tipracks_200_4 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)
    tipracks_10_1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 8)
    tipracks_10_2 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 11)


    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                        tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3, tipracks_200_4))
    m20 = protocol.load_instrument('p20_multi_gen2', mount='right', tip_racks=(tipracks_10_1, tipracks_10_2))

    #### REAGENT SETUP 1                           Description             Volume needed for protocol
    EtOH1 = EtOH_wash['A1']                 # 80% ethanol           88 ml in tot, but I would add 44 + 44

    #### REAGENT SETUP                             Description             Volume needed for protocol
    DNase = trough['A9']                    # DNase Buffer          3.3 ml
    BufferC_1 = trough['A7']                # Buffer C RNA rebind   11 ml
    BufferC_2 = trough['A8']                # Buffer C RNA rebind   11 ml
    Elution_buffer = trough['A12']          # Buffer D              5.5 ml

    Liquid_trash = trash_box['A1']


    #### Plate SETUP for Purification
    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    list_of_cols = ['A1','A2','A3','A4']

    #### VOLUME SETUP
    Sample_vol = 200
    EtOH_vol = 2.0*Sample_vol
    Wash_1_vol = 1.0*Sample_vol
    Wash_2_vol = 1.0*Sample_vol
    Elution_vol = 50
    BufferC_vol = 1.0*Sample_vol


    #### PROTOCOL ####
    mag_deck.engage(height=34)#(height=34)
    #protocol.delay(minutes=3)

    ## Remove supernatant, using tiprack 1
    for i in list_of_cols:
        m300.flow_rate.aspirate = 25
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i])
        m300.aspirate(200, RNA_plate[i].bottom(2))
        m300.dispense(200, Liquid_trash.top(-4))
        m300.blow_out(Liquid_trash.top(-4))
        protocol.delay(seconds=5)
        m300.aspirate(200, RNA_plate[i].bottom(2))
        m300.dispense(200, Liquid_trash.top(-4))
        m300.blow_out(Liquid_trash.top(-4))
        protocol.delay(seconds=5)
        m300.aspirate(200, RNA_plate[i].bottom(2))
        m300.dispense(200, Liquid_trash.top(-4))
        m300.blow_out(Liquid_trash.top(-4))
        protocol.delay(seconds=5)
        m300.aspirate(200, RNA_plate[i].bottom(2))
        m300.dispense(200, Liquid_trash.top(-4))
        m300.blow_out(Liquid_trash.top(-4))
        m300.air_gap(height = 2)
        protocol.delay(seconds=5)
        m300.return_tip()       # drop_tip()

    mag_deck.disengage()

    ### Wash 1 with Ethanol, using tiprack 2
    ### Transfer Wash 1 to RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i])
        m300.aspirate(Wash_1_vol, EtOH1.top(-12))
        m300.dispense(Wash_1_vol, RNA_plate[i].top(-4))
        m300.mix(5, Wash_1_vol, RNA_plate[i].bottom(4))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(RNA_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    # protocol.pause("Ensure enough buffer in the reservoir")
### probably to cancel:
    # #### Ensure enough buffer i reservoir by adding 3ml from backup
    # robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
    # p1000.set_flow_rate(aspirate=500, dispense=400)
    # p1000.pick_up_tip(tipracks_1000.wells('A1'))
    # p1000.aspirate(800, ETOH_backup.top(-20))
    # p1000.dispense(800, EtOH1.top(-4))
    # p1000.delay(seconds=2)
    # p1000.move_to(EtOH1.top(-4))
    # p1000.blow_out()
    # p1000.aspirate(800, ETOH_backup.top(-20))
    # p1000.dispense(800, EtOH1.top(-4))
    # p1000.delay(seconds=2)
    # p1000.move_to(EtOH1.top(-4))
    # p1000.blow_out()
    # p1000.aspirate(800, ETOH_backup.top(-20))
    # p1000.dispense(800, EtOH1.top(-4))
    # p1000.delay(seconds=2)
    # p1000.move_to(EtOH1.top(-4))
    # p1000.blow_out()
    # p1000.drop_tip()

    mag_deck.engage(height=34)
    #protocol.delay(minutes=2)

    ### Remove supernatant, by re-using tiprack 2
    ### remove supernatant from RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i])
        m300.aspirate(Wash_1_vol, RNA_plate[i].bottom(1))
        m300.dispense(Wash_1_vol, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.return_tip()       # drop_tip()

    mag_deck.disengage()

    ### Wash 2 with Ethanol, using tiprack 3
    ### Transfer Wash 2 to RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i])
        m300.aspirate(Wash_2_vol, EtOH1.top(-12))
        m300.dispense(Wash_2_vol, RNA_plate[i].top(-4))
        m300.mix(5, Wash_2_vol, RNA_plate[i].bottom(4))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(RNA_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    mag_deck.engage(height=34)
    #protocol.delay(minutes=2)

    ### Remove supernatant after Wash2, by re-using tiprack 3
    ### remove supernatant from RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i])
        m300.aspirate(Wash_2_vol, RNA_plate[i].bottom(1))
        m300.dispense(Wash_2_vol, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.return_tip()       # drop_tip()

    # remove the remaining supernatant with 20ul pipette
    for i in list_of_cols:
        ## Remove supernatant, by re-using tiprack 3
        ### remove supernatant from RNA_plate
        m20.flow_rate.aspirate = 50
        m20.flow_rate.dispense = 50
        m20.pick_up_tip(tipracks_10_1[i])
        m20.aspirate(10, RNA_plate[i].bottom(1))
        m20.dispense(10, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m20.return_tip()       # drop_tip()

    ## Dry beads before DNase treatment
    mag_deck.disengage()
    protocol.delay(minutes=1)


    ### Adding DNAse to RNA_plate, by using tiprack 4
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_4[i])
        m300.mix(2, 30, DNase.bottom(4))
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.aspirate(30, DNase.bottom(3))
        m300.dispense(30, RNA_plate[i].top(-10))
        m300.move_to(RNA_plate[i].top(-8))
        m300.blow_out()
        m300.air_gap(height = 2)
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()           # drop_tip()

    # incubating samples with DNase
    protocol.pause("Please substitute all tip racks (except 20ul one)  and refill the EtOH for wash 3 and 4 before continuing.")
    protocol.delay(minutes=10)

    ##Reset tipracks for more tips
    m300.reset_tipracks()

    ### Buffer C rebind, by using tiprack 1
    ### Transfer buffer C and beads to RNA_plate
    for i in list_of_cols[:6]:
        m300.pick_up_tip(tipracks_200_1[i])
        m300.mix(3, BufferC_vol, BufferC_1.bottom(4))
        # max_speed_per_axis = {'x':(300), 'y':(300), 'z': (50), 'a': (20), 'b': (20), 'c': 20}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()), **max_speed_per_axis)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
        m300.dispense(BufferC_vol, RNA_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, BufferC_vol, RNA_plate[i].bottom(2))
        protocol.delay(seconds=5)
        m300.move_to(RNA_plate[i].bottom(10))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()

    ### Transfer buffer C and beads to RNA_plate
    for i in list_of_cols[6:]:
        m300.pick_up_tip(tipracks_200_1[i])
        m300.mix(3, BufferC_vol, BufferC_2.bottom(4))
        # max_speed_per_axis = {'x':(300), 'y':(300), 'z': (50), 'a': (20), 'b': (20), 'c': 20}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()), **max_speed_per_axis)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
        m300.dispense(BufferC_vol, RNA_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, BufferC_vol, RNA_plate[i].bottom(2))
        protocol.delay(seconds=5)
        m300.move_to(RNA_plate[i].bottom(5))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()


    #protocol.delay(minutes=5)
    mag_deck.engage(height=34)#(height=34)
    #protocol.delay(minutes=1)

    for i in list_of_cols:
        ### Remove supernatant by re-using tiprack 1
        ### remove supernatant from RNA_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i])
        m300.aspirate(125, RNA_plate[i].bottom(1))
        m300.dispense(125, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.aspirate(125, RNA_plate[i].bottom(1))
        m300.dispense(125, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.blow_out(trash_box['A1'].top(-5))
        m300.return_tip()

    ## Ethanol Wash 3, using tiprack 2
    mag_deck.disengage()

    for i in list_of_cols:
    ### Transfer Wash 3 to RNA_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i])
        m300.aspirate(Wash_1_vol, EtOH1.top(-12))
        m300.dispense(Wash_1_vol, RNA_plate[i].top(-4))
        m300.mix(5, Wash_1_vol, RNA_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(RNA_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    mag_deck.engage(height=34)
    #protocol.delay(minutes=2)

    for i in list_of_cols:
        ## Remove supernatant, by re-using tiprack 2
        ### remove supernatant from RNA_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i])
        m300.aspirate(Wash_1_vol, RNA_plate[i].bottom(1))
        m300.dispense(Wash_1_vol, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.return_tip()       # drop_tip()

    ## Ethanol Wash 4, by using tiprack 3
    mag_deck.disengage()

    for i in list_of_cols:
        ### Transfer Wash 4 to RNA_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i])
        m300.aspirate(Wash_2_vol, EtOH1.top(-12))
        m300.dispense(Wash_2_vol, RNA_plate[i].top(-4))
        m300.mix(5, Wash_2_vol, RNA_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(RNA_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

    mag_deck.engage(height=34)
    #protocol.delay(minutes=2)

    for i in list_of_cols:
        ## Remove supernatant, by re-using tiprack 3
        ### remove supernatant from RNA_plate
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i])
        m300.aspirate(Wash_2_vol, RNA_plate[i].bottom(1))
        m300.dispense(Wash_2_vol, trash_box['A1'].top(-5))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.blow_out(trash_box['A1'].top(-5))
        m300.return_tip()       # drop_tip()

    # remove the remaining supernatant with 20ul pipette
    for i in list_of_cols:
        ## Remove supernatant, by re-using tiprack 3
        ### remove supernatant from RNA_plate
        m20.flow_rate.aspirate = 50
        m20.flow_rate.dispense = 50
        m20.pick_up_tip(tipracks_10_2[i])
        m20.aspirate(10, RNA_plate[i].bottom(1))
        m20.dispense(10, trash_box['A1'].top(-5))
        m20.blow_out()
        protocol.delay(seconds=5)
        m20.return_tip()       # drop_tip()

    ## Dry beads before elution (removing supernatant from all wells takes more than 5 mins, should be enough for beads to dry)

    ## Elution
    mag_deck.disengage()

    #### Transfer elution buffer to RNA_plate
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_4[i])
        m300.aspirate(Elution_vol, Elution_buffer.bottom(2))
        m300.dispense(Elution_vol, RNA_plate[i].top(-2))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.mix(5, 30, RNA_plate[i].bottom(2))
        protocol.delay(seconds=5)
        m300.move_to(RNA_plate[i].bottom(5))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()

    protocol.delay(minutes=5)
    # protocol.pause("Please cover the plate with film and incubate 5 min 25°C")
    mag_deck.engage(height=34)
    #protocol.delay(minutes=2)

    odd_cols = ['A1','A3']#,'A5','A7','A9','A11']
    even_cols = ['A2','A4']#,'A6','A8','A10','A12']

    from opentrons import types

    ### Transfer elutes to elution_plate
    for i in odd_cols:
        m300.pick_up_tip(tipracks_200_4[i])
        m300.flow_rate.aspirate = 5
        m300.flow_rate.dispense = 50
        center_location = RNA_plate[i].bottom(1.5)
        left_location = center_location.move(types.Point(x=-1.5, y=0, z=-1))
        m300.move_to(center_location)
        m300.aspirate(70, left_location)
        m300.dispense(70, elution_plate_RNA[i].bottom(2))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(elution_plate_RNA[i].top(-10))
        m300.blow_out()
        m300.return_tip()       # drop_tip()

    for i in even_cols:
        m300.pick_up_tip(tipracks_200_4[i])
        m300.flow_rate.aspirate = 5
        m300.flow_rate.dispense = 50
        center_location = RNA_plate[i].bottom(1.5)
        right_location = center_location.move(types.Point(x=1.5, y=0, z=-1))
        m300.move_to(center_location)
        m300.aspirate(70, right_location)
        m300.dispense(70, elution_plate_RNA[i].bottom(2))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(elution_plate_RNA[i].top(-10))
        m300.blow_out()
        m300.return_tip()       # drop_tip()


    mag_deck.disengage()
