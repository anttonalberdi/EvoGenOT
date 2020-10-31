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
    'update': 'Martina Cardinali <martina.cardinali.4@gmai.com',
    'apiLevel': '2.2',
    'date': '2020/10/31',
    'description': 'Automation of D-Rex RNA protocol for stool samples in SHIELD',
}

# These labwares must be re-created and added to the Opentrons App in the EHI computer

### Custom LABWARE load

# plate_name = '1ml_magPCR'
# if plate_name not in labware.list():
#     custom_plate = labware.create(
#         plate_name,                    # name of you labware
#         grid=(12, 8),                    # specify amount of (columns, rows)
#         spacing=(9, 9),               # distances (mm) between each (column, row)
#         diameter=7.5,                     # diameter (mm) of each well on the plate
#         depth=26.4,                       # depth (mm) of each well on the plate
#         volume=1000)
#
# plate_name = 'One-Column-reservoir'
# if plate_name not in labware.list():
#     custom_plate = labware.create(
#         plate_name,                    # name of you labware
#         grid=(1, 1),                    # specify amount of (columns, rows)
#         spacing=(0, 0),               # distances (mm) between each (column, row)
#         diameter=81,                     # diameter (mm) of each well on the plate
#         depth=35,                       # depth (mm) of each well on the plate
#         volume=350000)

def run(protocol):
    #### LABWARE SETUP ####
    elution_plate_RNA = protocol.load_labware('biorad-hardshell-96-PCR', 1)
    trough = protocol.load_labware('trough-12row', 9)
    mag_deck = protocol.load_labware('magdeck', 7)
    RNA_plate = protocol.load_labware('1ml_magPCR', 7)
    trash_box = protocol.load_labware('One-Column-reservoir', 8)
    EtOH_wash = protocol.load_labware('One-Column-reservoir', 6)

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 2)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tipracks_200_4 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)


    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                        tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3, tipracks_200_4))

    #### REAGENT SETUP 1                           Description             Volume needed for protocol
    EtOH1 = EtOH_wash['A1']                 # 80% ethanol           82.5 ml

    #### REAGENT SETUP                             Description             Volume needed for protocol
    DNase = trough['A9']                    # DNase Buffer          3.2 ml
    BufferC_1 = trough['A7']                # Buffer C RNA rebind   10 ml
    BufferC_2 = trough['A8']                 # Buffer C RNA rebind   10 ml
    Elution_buffer = trough['A12']          # Buffer D              6 ml

    Liquid_trash = trash_box['A1']


    #### Plate SETUP for Purification
    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']

    #### VOLUME SETUP
    Sample_vol = 200
    EtOH_vol = 2.0*Sample_vol
    Wash_1_vol = 1.0*Sample_vol
    Wash_2_vol = 0.9*Sample_vol
    Elution_vol = 50
    BufferC_vol = 0.9*Sample_vol


    #### PROTOCOL ####
    mag_deck.engage(height=34)
    protocol.delay(minutes=3)

    ## Remove supernatant, using tiprack 1
    for i in list_of_cols:
        m300.flow_rate.aspirate = 25
        m300.flow_rate.dispense = 25
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(200, RNA_plate[i].bottom(2))
        m300.dispense(200, Liquid_trash.top(-4))
        m300.blow_out(Liquid_trash.top(-4))
        m300.aspirate(200, RNA_plate[i].bottom(2))
        m300.dispense(200, Liquid_trash.top(-4))
        m300.blow_out(Liquid_trash.top(-4))
        m300.aspirate(200, RNA_plate[i].bottom(2))
        m300.dispense(200, Liquid_trash.top(-4))
        m300.blow_out(Liquid_trash.top(-4))
        m300.aspirate(100, RNA_plate[i].bottom(2))
        m300.dispense(100, Liquid_trash.top(-4))
        m300.blow_out(Liquid_trash.top(-4))
        m300.return_tip()

    mag_deck.disengage()

    ### Wash 1 with Ethanol, using tiprack 2
    ### Transfer Wash 1 to RNA_plate
    for i list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        m300.aspirate(Wash_1_vol, EtOH1.top(-12))
        m300.dispense(Wash_1_vol, RNA_plate[i].top(-4))
        m300.mix(5, Wash_1_vol, RNA_plate[i].bottom(4))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 130
        m300.flow_rate.dispense = 130
        m300.move_to(RNA_plate[i].top(-10))
        m300.blow_out()
        m300.return_tip()

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
    m300.delay(minutes=2)

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
        m300.return_tip()

        mag_deck.disengage()

    ### Wash 2 with Ethanol, using tiprack 3
    ### Transfer Wash 2 to RNA_plate
    for i list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
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
        m300.delay(minutes=2)

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
        m300.return_tip()

    ## Dry beads before DNase treatment
    mag_deck.disengage()
    m300.delay(minutes=1)


    ### Adding DNAse to RNA_plate, by using tiprack 4
    for i in list_of_cols:
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.pick_up_tip(tipracks_200_4[i])
        m300.mix(2, 30, DNase.bottom(4))
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.aspirate(30, DNase.bottom(1))
        m300.dispense(30, RNA_plate[i].top(-10))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.move_to(RNA_plate[i].top(-8))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.drop_tip()

    # incubating samples with DNase
    protocol.pause("Please cover the plate with film and incubate 10 min 25°C at 1300 rpm. Please fill up tips before continuing process")
    ##Reset tipracks for more tips
    m300.reset_tipracks()

    ### Buffer C rebind, by using tiprack 1
    ### Transfer buffer C and beads to RA1
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip()
    m300.move_to(BufferC_1.top(-16))
    m300.mix(3, BufferC_vol, BufferC_1.top(-12))
    max_speed_per_axis = {'x':(300), 'y':(300), 'z': (50), 'a': (20), 'b': (20), 'c': 20}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()), **max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_1.top(-12))
    m300.move_to(RA1.bottom(1))
    m300.dispense(BufferC_vol, RA1.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA1.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA1.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()


    ### Transfer buffer C and beads to RA2
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(BufferC_1.top(-20))
    m300.mix(3, BufferC_vol, BufferC_1.top(-16))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_1.top(-16))
    m300.move_to(RA2.bottom(1))
    m300.dispense(BufferC_vol, RA2.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA2.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA2.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA3
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.mix(3, BufferC_vol, BufferC_1)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
    m300.move_to(RA3.bottom(1))
    m300.dispense(BufferC_vol, RA3.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA3.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA3.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA4
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.mix(3, BufferC_vol, BufferC_1)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
    m300.move_to(RA4.bottom(1))
    m300.dispense(BufferC_vol, RA4.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA4.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA4.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA5
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.mix(3, BufferC_vol, BufferC_1)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_1.bottom(2))
    m300.move_to(RA5.bottom(1))
    m300.dispense(BufferC_vol, RA5.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA5.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA5.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA6
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.mix(3, BufferC_vol, BufferC_1)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_1.bottom(1))
    m300.move_to(RA6.bottom(1))
    m300.dispense(BufferC_vol, RA6.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA6.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA6.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA7
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(BufferC_2.top(-16))
    m300.mix(3, BufferC_vol, BufferC_2.top(-12))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_2.top(-12))
    m300.move_to(RA7.bottom(1))
    m300.dispense(BufferC_vol, RA7.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA7.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA7.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA8
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(BufferC_2.top(-20))
    m300.mix(3, BufferC_vol, BufferC_2.top(-16))
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_2.top(-16))
    m300.move_to(RA8.bottom(1))
    m300.dispense(BufferC_vol, RA8.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA8.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA8.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA9
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.mix(3, BufferC_vol, BufferC_2)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
    m300.move_to(RA9.bottom(1))
    m300.dispense(BufferC_vol, RA9.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA9.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA9.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA10
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.mix(3, BufferC_vol, BufferC_2)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
    m300.move_to(RA10.bottom(1))
    m300.dispense(BufferC_vol, RA10.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA10.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA10.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA11
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.mix(3, BufferC_vol, BufferC_2)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
    m300.move_to(RA11.bottom(1))
    m300.dispense(BufferC_vol, RA11.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA11.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA11.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    ### Transfer buffer C and beads to RA12
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.mix(3, BufferC_vol, BufferC_2)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(BufferC_vol, BufferC_2.bottom(2))
    m300.move_to(RA12.bottom(1))
    m300.dispense(BufferC_vol, RA12.bottom(4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(8, BufferC_vol, RA12.bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(RA12.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.return_tip()

    m300.delay(minutes=5)
    mag_deck.engage(height=34)
    m300.delay(minutes=1)

    ### Remove supernatant by re-using tiprack 1
    ### remove supernatant from RA1
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A1'))
    m300.aspirate(125, RA1.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA1.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA2
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A2'))
    m300.aspirate(125, RA2.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA2.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA3
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A3'))
    m300.aspirate(125, RA3.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA3.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA4
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A4'))
    m300.aspirate(125, RA4.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA4.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA5
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A5'))
    m300.aspirate(125, RA5.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA5.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA6
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A6'))
    m300.aspirate(125, RA6.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA6.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA7
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A7'))
    m300.aspirate(125, RA7.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA7.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA8
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A8'))
    m300.aspirate(125, RA8.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA8.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA9
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A9'))
    m300.aspirate(125, RA9.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA9.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA10
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A10'))
    m300.aspirate(125, RA10.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA10.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA11
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A11'))
    m300.aspirate(125, RA11.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA11.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA12
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_1.wells('A12'))
    m300.aspirate(125, RA12.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA12.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ## Ethanol Wash 3, using tiprack 2
    mag_deck.disengage()

    ### Transfer Wash 3 to RA1
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(Wash_1_vol, EtOH1.top(-12))
    m300.dispense(Wash_1_vol, RA1.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA1.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA1.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA2
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.bottom())
    m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
    m300.dispense(Wash_1_vol, RA2.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA2.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA2.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA3
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
    m300.dispense(Wash_1_vol, RA3.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA3.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA3.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA4
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_1_vol, EtOH1.bottom())
    m300.dispense(Wash_1_vol, RA4.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA4.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA4.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA5
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_1_vol, EtOH1.bottom())
    m300.dispense(Wash_1_vol, RA5.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA5.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA5.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA6
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.bottom())
    m300.aspirate(Wash_1_vol, EtOH1.bottom())
    m300.dispense(Wash_1_vol, RA6.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA6.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA7.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA7
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_1_vol, EtOH1.bottom())
    m300.dispense(Wash_1_vol, RA7.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA7.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA7.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA8
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_1_vol, EtOH1.bottom())
    m300.dispense(Wash_1_vol, RA8.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA8.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA8.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA9
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_1_vol, EtOH1.bottom())
    m300.dispense(Wash_1_vol, RA9.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA9.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA9.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA10
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_1_vol, EtOH1.bottom())
    m300.dispense(Wash_1_vol, RA10.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA10.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA10.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA11
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_1_vol, EtOH1.bottom())
    m300.dispense(Wash_1_vol, RA11.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA11.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA11.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 3 to RA12
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_1_vol, EtOH1.bottom())
    m300.dispense(Wash_1_vol, RA12.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_1_vol, RA12.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA12.top(-10))
    m300.blow_out()
    m300.return_tip()

    mag_deck.engage(height=34)
    m300.delay(minutes=2)

    ## Remove supernatant, by re-using tiprack 2
    ### remove supernatant from RA1
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A1'))
    m300.aspirate(Wash_1_vol, RA1.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA2
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A2'))
    m300.aspirate(Wash_1_vol, RA2.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA3
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A3'))
    m300.aspirate(Wash_1_vol, RA3.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA4
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A4'))
    m300.aspirate(Wash_1_vol, RA4.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA5
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A5'))
    m300.aspirate(Wash_1_vol, RA5.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA6
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A6'))
    m300.aspirate(Wash_1_vol, RA6.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA7
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A7'))
    m300.aspirate(Wash_1_vol, RA7.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA8
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A8'))
    m300.aspirate(Wash_1_vol, RA8.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA9
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A9'))
    m300.aspirate(Wash_1_vol, RA9.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA10
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A10'))
    m300.aspirate(Wash_1_vol, RA10.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA11
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A11'))
    m300.aspirate(Wash_1_vol, RA11.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA12
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_2.wells('A12'))
    m300.aspirate(Wash_1_vol, RA12.bottom(1))
    m300.dispense(Wash_1_vol, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ## Ethanol Wash 4, by using tiprack 3
    mag_deck.disengage()

    ### Transfer Wash 4 to RA1
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.top(-16))
    m300.aspirate(Wash_2_vol, EtOH1.top(-12))
    m300.dispense(Wash_2_vol, RA1.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA1.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA1.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA2
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.bottom())
    m300.aspirate(Wash_2_vol, EtOH1.bottom(1))
    m300.dispense(Wash_2_vol, RA2.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA2.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA2.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA3
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_2_vol, EtOH1.bottom(1))
    m300.dispense(Wash_2_vol, RA3.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA3.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA3.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA4
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_2_vol, EtOH1.bottom())
    m300.dispense(Wash_2_vol, RA4.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA4.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA4.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA5
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_2_vol, EtOH1.bottom())
    m300.dispense(Wash_2_vol, RA5.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA5.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA5.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA6
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.move_to(EtOH1.bottom())
    m300.aspirate(Wash_2_vol, EtOH1.bottom())
    m300.dispense(Wash_2_vol, RA6.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA6.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA6.top(-10))
    m300.blow_out()
    m300.return_tip()


    ### Transfer Wash 4 to RA7
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_2_vol, EtOH1.bottom())
    m300.dispense(Wash_2_vol, RA7.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA7.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA7.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA8
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_2_vol, EtOH1.bottom())
    m300.dispense(Wash_2_vol, RA8.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA8.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA8.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA9
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_2_vol, EtOH1.bottom())
    m300.dispense(Wash_2_vol, RA9.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA9.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA9.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA10
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_2_vol, EtOH1.bottom())
    m300.dispense(Wash_2_vol, RA10.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA10.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA10.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA11
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_2_vol, EtOH1.bottom())
    m300.dispense(Wash_2_vol, RA11.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA11.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA11.top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Wash 4 to RA12
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    m300.aspirate(Wash_2_vol, EtOH1.bottom())
    m300.dispense(Wash_2_vol, RA12.top(-4))
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.mix(5, Wash_2_vol, RA12.bottom(5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(RA12.top(-10))
    m300.blow_out()
    m300.return_tip()

    mag_deck.engage(height=34)
    m300.delay(minutes=2)


    ## Remove supernatant, by re-using tiprack 3
    ### remove supernatant from RA1
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A1'))
    m300.aspirate(125, RA1.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA1.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA2
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A2'))
    m300.aspirate(125, RA2.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA2.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA3
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A3'))
    m300.aspirate(125, RA3.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA3.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA4
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A4'))
    m300.aspirate(125, RA4.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA4.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA5
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A5'))
    m300.aspirate(125, RA5.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA5.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA6
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A6'))
    m300.aspirate(125, RA6.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA6.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA7
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A7'))
    m300.aspirate(125, RA7.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA7.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA8
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A8'))
    m300.aspirate(125, RA8.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA8.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA9
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A9'))
    m300.aspirate(125, RA9.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA9.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA10
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A10'))
    m300.aspirate(125, RA10.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA10.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA11
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A11'))
    m300.aspirate(125, RA11.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA11.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ### remove supernatant from RA12
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.pick_up_tip(tipracks_200_3.wells('A12'))
    m300.aspirate(125, RA12.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.aspirate(125, RA12.bottom(1))
    m300.dispense(125, trash_box.wells('A1').top(-5))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.blow_out(trash_box.wells('A1').top(-5))
    m300.return_tip()

    ## Dry beads before elution (removing supernatant from all wells takes more than 5 mins, should be enough for beads to dry)

    ## Elution
    mag_deck.disengage()
    for target in samples: # Slow down head speed 0.5X for bead handling
        m300.pick_up_tip()
        max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
        robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.set_flow_rate(aspirate=50, dispense=50)
        m300.aspirate(Elution_vol, Elution_buffer.bottom(1))
        m300.dispense(Elution_vol, target.top(-2))
        m300.delay(seconds=5)
        m300.set_flow_rate(aspirate=100, dispense=100)
        m300.move_to(target.bottom(5))
        m300.blow_out()
        max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()

    robot.pause("Please cover the plate with film and incubate 5 min 25°C at 1500 rpm")
    mag_deck.engage(height=34)
    m300.delay(minutes=2)

    ### Transfer Elution buffer to elution_plate A1
    m300.pick_up_tip(tipracks_200_4.wells('A1'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA1.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A1').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A1').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA2
    m300.pick_up_tip(tipracks_200_4.wells('A2'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA2.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A2').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A2').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA3
    m300.pick_up_tip(tipracks_200_4.wells('A3'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA3.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A3').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A3').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA4
    m300.pick_up_tip(tipracks_200_4.wells('A4'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA4.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A4').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A4').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA5
    m300.pick_up_tip(tipracks_200_4.wells('A5'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA5.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A5').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A5').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA6
    m300.pick_up_tip(tipracks_200_4.wells('A6'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA6.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A6').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A6').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA7
    m300.pick_up_tip(tipracks_200_4.wells('A7'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA7.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A7').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A7').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA8
    m300.pick_up_tip(tipracks_200_4.wells('A8'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA8.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A8').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A8').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA9
    m300.pick_up_tip(tipracks_200_4.wells('A9'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA9.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A9').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A9').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA10
    m300.pick_up_tip(tipracks_200_4.wells('A10'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA10.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A10').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A10').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA11
    m300.pick_up_tip(tipracks_200_4.wells('A11'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA11.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A11').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A11').top(-10))
    m300.blow_out()
    m300.return_tip()

    ### Transfer Elution buffer to EA12
    m300.pick_up_tip(tipracks_200_4.wells('A12'))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(Elution_vol, RA12.bottom())
    m300.dispense(Elution_vol, elution_plate_RNA.wells('A12').bottom(2))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=130, dispense=130)
    m300.move_to(elution_plate_RNA.wells('A12').top(-10))
    m300.blow_out()
    m300.return_tip()

    mag_deck.disengage()
