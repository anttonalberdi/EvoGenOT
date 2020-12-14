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
    'description': 'Automation of D-Rex RNA and DNA separation for extraction protocol',
}

# the volume is calculated for 110 samples instead of 96

def run(protocol):
    #### LABWARE SETUP ####
    trough = protocol.load_labware('usascientific_12_reservoir_22ml', 6)
    RNA_plate = protocol.load_labware('biorad_96_wellplate_1000ul', 3)
    mag_deck = protocol.load_module('magdeck', 7)
    sample_plate = mag_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 9)   # only first 2 cols needed for transfering beads and EtOH binding buffer to RNA_plate
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 5)

    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                    tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3))

    #### REAGENT SETUP                              description             Volume needed for protocol
    Binding_buffer1 = trough['A1']            # Buffer B:              11 ml
    Binding_buffer2 = trough['A2']			  # Buffer B:              11 ml
    EtOH_Bind1 = trough['A4']                 # EtOH + magnetic:       17.5 ml
    EtOH_Bind2 = trough['A5']                 # EtOH + magnetic:       17.5 ml

    #### Plate SETUP
    list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    list_of_cols = ['A1','A2','A7','A8']
    #### VOLUME SETUP
    Sample_vol = 200
    Binding_buffer_vol = Sample_vol*1
    EtOH_buffer_vol = 175

    #### PROTOCOL ####

    ## add beads and sample binding buffer to DNA/sample plate
    mag_deck.disengage()

    ### Transfer buffer B1 (trough col 1) and beads to sample plate (col 1 to 6)
    for i in list_of_cols[:6]:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(5, Binding_buffer_vol, Binding_buffer1.top(-28))
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(3))
        m300.dispense(Binding_buffer_vol, sample_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, Binding_buffer_vol, sample_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.move_to(sample_plate[i].top(-4))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()


    ### Transfer buffer B2 (trough col 2) and beads to sample plate (col 7 to 12)
    for i in list_of_cols[6:]:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(5, Binding_buffer_vol, Binding_buffer2.top(-28))
        # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (100), 'a': (50), 'b': (20), 'c': (20)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(Binding_buffer_vol, Binding_buffer2.bottom(3))
        m300.dispense(Binding_buffer_vol, sample_plate[i].bottom(4))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(5, Binding_buffer_vol, sample_plate[i].bottom(5))
        protocol.delay(seconds=5)
        m300.move_to(sample_plate[i].top(-4))
        m300.blow_out()
        # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
        # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
        m300.return_tip()

    protocol.pause('Cover DNA plate with foil. Incubate for 15 minutes at 10 ºC at 1500 rpm. Meanwhile proceed with next step.')

    ## Add beads and EtOH binding buffer (trough col 4) to RNA plate (col 1 to 6)
    m300.pick_up_tip(tipracks_200_2['A1'])
    for i in list_of_cols:
        m300.transfer(350, EtOH_Bind1.bottom(3), RNA_plate[i].bottom(4), mix_before=(5,200), new_tip='never')
    m300.drop_tip()
    # ## Add beads and EtOH binding buffer (trough col 4) to RNA plate (col 1 to 6)
    # for i in list_of_cols[:6]:
    #     m300.flow_rate.aspirate = 100
    #     m300.flow_rate.dispense = 100
    #     m300.pick_up_tip(tipracks_200_2['A1']) # Slow down head speed 0.5X for bead handling
    #     m300.mix(5, 200, EtOH_Bind1.top(-12))
    #     # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
    #     # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    #     m300.flow_rate.aspirate = 50
    #     m300.flow_rate.dispense = 50
    #     m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.bottom(2))
    #     m300.dispense(EtOH_buffer_vol, RNA_plate[i].bottom(4))
    #     m300.aspirate(EtOH_buffer_vol, EtOH_Bind1.bottom(2))
    #     m300.dispense(EtOH_buffer_vol, RNA_plate[i].bottom(4))
    #     m300.flow_rate.aspirate = 100
    #     m300.flow_rate.dispense = 100
    #     protocol.delay(seconds=5)
    #     m300.move_to(RNA_plate[i].top(-4))
    #     m300.blow_out()
    #     # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    #     # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    #     m300.return_tip()
    #
    # ## add beads and EtOH binding buffer (trough col 5) to RNA plate (col 7 to 12)
    # for i in list_of_cols[6:]:
    #     m300.flow_rate.aspirate = 100
    #     m300.flow_rate.dispense = 100
    #     m300.pick_up_tip(tipracks_200_2['A2']) # Slow down head speed 0.5X for bead handling
    #     m300.mix(5, 200, EtOH_Bind2.top(-12))
    #     # max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (50), 'b': (20), 'c': (20)}
    #     # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    #     m300.flow_rate.aspirate = 50
    #     m300.flow_rate.dispense = 50
    #     m300.aspirate(EtOH_buffer_vol, EtOH_Bind2.bottom(2))
    #     m300.dispense(EtOH_buffer_vol, RNA_plate[i].bottom(4))
    #     m300.aspirate(EtOH_buffer_vol, EtOH_Bind2.bottom(2))
    #     m300.dispense(EtOH_buffer_vol, RNA_plate[i].bottom(4))
    #     m300.flow_rate.aspirate = 100
    #     m300.flow_rate.dispense = 100
    #     protocol.delay(seconds=5)
    #     m300.move_to(RNA_plate[i].top(-4))
    #     m300.blow_out()
    #     # max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    #     # robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    #     m300.return_tip()       # or drop tip?

    protocol.pause('Please, take DNA plate from incubator and then, place it on the magnet.')

    # Reuse tiprack 1 to mix sample with beads and buffer after incubation
    for i in list_of_cols:
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(5, 200, sample_plate[i].bottom(4))
        m300.blow_out(sample_plate[i].top(-5))
        #m300.air_gap(height=2)
        m300.drop_tip()

    ## Transfer supernatant
    mag_deck.engage(height_from_base=0)
    #protocol.delay(minutes=7)

    #### Transfer supernatant to RNA_plate
    for i in list_of_cols:
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        #m300.transfer(350, sample_plate[i].bottom(2), RNA_plate[i].bottom(4), new_tip='once',  blow_out =True, air_gap=30)
        m300.aspirate(200, sample_plate[i].bottom(2))
        m300.dispense(200, RNA_plate[i].bottom(4))
        m300.blow_out(RNA_plate[i].top(-5))
        #m300.air_gap(height=2)
        m300.touch_tip(v_offset=-3)                    # remove comment if need to eliminate drops around the tip
        m300.aspirate(200, sample_plate[i].bottom(1))
        m300.dispense(200, RNA_plate[i].bottom(4))
        m300.blow_out(RNA_plate[i].top(-5))
        #m300.air_gap(height=2)
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

    protocol.pause("Cover DNA plate with aluminium seal and store in fridge until purification the same or following day.Continue with purification of RNA plate.")

    ############################
    ###### Job is done! ######
    ############################
