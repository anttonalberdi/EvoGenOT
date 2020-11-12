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
    'protocolName': 'D-Rex Inital Extraction',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'update': 'Martina Cardinali <martina.cardinali.4@gmail.com>',
    'apiLevel': '2.2',
    'date': '2020/10/31',
    'description': 'Automation of D-Rex RNA and DNA seperation for extraction protocol of stool samples in SHIELD. ',
}

# These labwares must be re-created and added to the Opentrons App in the EHI computer

# ### Custom LABWARE load
# plate_name = '1ml_PCR'
# if plate_name not in labware.list():
#     custom_plate = labware.create(
#         plate_name,                    # name of you labware
#         grid=(12, 8),                    # specify amount of (columns, rows)
#         spacing=(9, 9),               # distances (mm) between each (column, row)
#         diameter=7.5,                     # diameter (mm) of each well on the plate
#         depth=26.4,                       # depth (mm) of each well on the plate
#         volume=1000)
#
# plate_name = '1ml_magPCR'
# if plate_name not in labware.list():
#     custom_plate = labware.create(
#         plate_name,                    # name of you labware
#         grid=(12, 8),                    # specify amount of (columns, rows)
#         spacing=(9, 9),               # distances (mm) between each (column, row)
#         diameter=7.5,                     # diameter (mm) of each well on the plate
#         depth=26.4,                       # depth (mm) of each well on the plate
#         volume=1000)


def run(protocol):
    #### LABWARE SETUP ####
    trough = protocol.load_labware('trough-12row', 9)
    RNA_plate = protocol.load_labware('1ml_PCR', 1)
    mag_deck = protocol.load_labware('magdeck', 7)
    sample_plate = protocol.load_labware('1ml_magPCR', 7, share=True)

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 6)

    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                    tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3))

    #### REAGENT SETUP                              description             Volume needed for protocol
    Binding_buffer1 = trough['A1']            # Buffer B:              11 ml
    Binding_buffer2 = trough['A2']			  # Buffer B:              11 ml
    EtOH_Bind1 = trough['A3']                 # EtOH + magnetic:       17.5 ml
    EtOH_Bind2 = trough['A4']                 # EtOH + magnetic:       17.5 ml
    BufferC_1 = trough['A5']                  # Buffer C:              10 ml
    BufferC_2 = trough['A6']                  # Buffer C:              10 ml

    #### Plate SETUP
    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']

    #### VOLUME SETUP
    Sample_vol = 200
    Binding_buffer_vol = Sample_vol*1
    EtOH_buffer_vol = 175
    BufferC_vol = 0.9*Sample_vol

    #### PROTOCOL ####

    ## add beads and sample binding buffer to DNA/sample plate
    mag_deck.disengage()

    ### Transfer buffer B1 and beads to sample plate (col 1 to 6)
    for i in list_of_cols[:6]:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(5, Binding_buffer_vol, Binding_buffer1.top(-28))
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(Binding_buffer_vol, Binding_buffer1.top(-28))
        m300.dispense(Binding_buffer_vol, sample_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, Binding_buffer_vol, sample_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.move_to(sample_plate[i].top(-4))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.drop_tip()


    ### Transfer buffer B2 and beads to sample plate (col 7 to 12)
    for i in list_of_cols[6:]:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(5, Binding_buffer_vol, Binding_buffer2.top(-28))
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(Binding_buffer_vol, Binding_buffer2.top(-28))
        m300.dispense(Binding_buffer_vol, sample_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, Binding_buffer_vol, sample_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.move_to(sample_plate[i].top(-4))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.drop_tip()

    protocol.pause('Cover DNA plate with foil and spin down. Incubate for 15 minutes at 10 ºC at 1500 rpm.')

    ## add beads and EtOH binding buffer 1 to RNA plate (col 1 to 6)
    for i in list_of_cols[:6]:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(5, 200, EtOH_Bind1.top(-12))
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.top(-12))
        m300.dispense(EtOH_buffer_vol, RNA_plate[i].bottom(4))
        m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.top(-12))
        m300.dispense(EtOH_buffer_vol, RNA_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        protocol.delay(seconds=5)
        m300.move_to(RNA_plate[i].top(-4))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()       # or drop tip?

    ## add beads and EtOH binding buffer 2 to RNA plate (col 7 to 12)
    for i in list_of_cols[6:]:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_2[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(5, 200, EtOH_Bind2.top(-12))
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(EtOH_buffer_vol, EtOH_Bind2.top(-12))
        m300.dispense(EtOH_buffer_vol, RNA_plate[i].bottom(4))
        m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.top(-12))
        m300.dispense(EtOH_buffer_vol, RNA_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        protocol.delay(seconds=5)
        m300.move_to(RNA_plate[i].top(-4))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()       # or drop tip?

    protocol.pause('Please, take DNA plate from incubator and shortly spin down at 1000 xg. Then, place it on the magnet.')

    ## Transfer supernatant
    mag_deck.engage(height=34)
    protocol.delay(minutes=5)

    #### Transfer supernatant to RNA_plate
    for i in list_of_cols:
        m300.pick_up_tip(tipracks_200_3[i]))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(175, sample_plate[i].bottom(2))
        m300.dispense(175, RNA_plate[i].top(-2))
        m300.blow_out()
        m300.aspirate(175, sample_plate[i].bottom(2))
        m300.dispense(175, RNA_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(3, 200, RNA_plate[i].bottom(2))
        protocol.delay(seconds=5)
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.move_to(RNA_plate[i].top(-4))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()

    mag_deck.disengage()

    protocol.pause('Please cover DNA plate with foil and store in the fridge until purification (same or following day)')
    protocol.pause('Please cover RNA plate with foil and spin it down. Incubate 15 min 10°C at 1000 rpm. \
    Let the beads settle 5 min. Shortly spin down the plate at 1000 xg.')
    ############################
    ###### Job is done! ######
    ############################
