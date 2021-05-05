## Description of procedure ##
#
#
# Things to do before procedure
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
    trough = protocol.load_labware('usascientific_12_reservoir_22ml', 2)
    RNA_plate = protocol.load_labware('biorad_96_wellplate_1000ul', 1)
    mag_deck = protocol.load_module('magdeck', 10)
    sample_plate = mag_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')
    # Load a Temperature Module GEN1 in deck slot 10.
    temp_deck = protocol.load_module('tempdeck', 7)
    incubation_plate = temp_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')


    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)   # only first 2 cols needed for transfering beads and EtOH binding buffer to RNA_plate
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 9)

    #### PIPETTE SETUP ####
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                    tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3))

    #### REAGENT SETUP                              description             Volume needed for protocol
    Binding_buffer1 = trough['A1']            # Buffer B:              11 ml
    # Binding_buffer2 = trough['A2']			  # Buffer B:              11 ml   # not neeeded if running half plate
### If running complete plate, move EtOH1_Bind1 to trough['A3'] and EtOH1_Bind2 to trough['A4']
    EtOH_Bind1 = trough['A2']                 # EtOH + magnetic:       10.8 ml EtOH + 405ul beads
    EtOH_Bind2 = trough['A3']                 # EtOH + magnetic:       10.8 ml EtOH + 405ul beads
    #EtOH_Bind3 = trough['A5']                # EtOH + magnetic:       10.8 ml EtOH + 405ul beads    # not neeeded if running half plate
    #EtOH_Bind4 = trough['A6']                # EtOH + magnetic:       10.8 ml EtOH + 405ul beads    # not neeeded if running half plate

    #### Plate SETUP
    #list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    list_of_cols = ['A1','A2','A3','A4','A5','A6']
    #### VOLUME SETUP
    Sample_vol = 200
    Binding_buffer_vol = Sample_vol*1
    EtOH_buffer_vol = 175

    #### PROTOCOL ####
    ## Place plate with sample above temp_deck
    mag_deck.disengage()

    ### Transfer buffer B1 (trough col 1) and beads to incubation plate (col 1 to 6)
    for i in list_of_cols[:6]:
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(4, Binding_buffer_vol, Binding_buffer1.bottom(4.8))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(4.8))
        m300.dispense(Binding_buffer_vol, incubation_plate[i].bottom(5.8))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(4, Binding_buffer_vol, incubation_plate[i].bottom(6.8))
        m300.move_to(incubation_plate[i].top(-5))
        m300.blow_out()
        protocol.delay(seconds=5)
        m300.blow_out()
        m300.touch_tip(v_offset=-5, radius=0.7)
        m300.air_gap(height=2)
        m300.return_tip()


# to make equal to the part above ->    ### Transfer buffer B2 (trough col 2) and beads to incubation plate (col 7 to 12)
    for i in list_of_cols[6:]:
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.pick_up_tip(tipracks_200_1[i]) # Slow down head speed 0.5X for bead handling
        m300.mix(4, Binding_buffer_vol, Binding_buffer1.bottom(4.8))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(4.8))
        m300.dispense(Binding_buffer_vol, incubation_plate[i].bottom(5.8))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(4, Binding_buffer_vol, incubation_plate[i].bottom(6.8))
        m300.move_to(incubation_plate[i].top(-5))
        m300.blow_out()
        protocol.delay(seconds=5)
        m300.blow_out()
        m300.touch_tip(v_offset=-5, radius=0.7)
        m300.air_gap(height=2)
        m300.return_tip()

    temp_deck.set_temperature(10)

    # Incubate the samples at 10°C for 15 minutes
    protocol.delay(minutes=15)
    #protocol.delay(minutes=1)
    temp_deck.deactivate()

    # Transfer all the 400ul into the rack on the magnetic module (col 1 to 6) using same tips as before
    for i in list_of_cols[:6]:
        m300.pick_up_tip(tipracks_200_1[i])
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.mix(3, 170, incubation_plate[i].bottom(5))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(150, incubation_plate[i].bottom(4.8))
        m300.dispense(150, sample_plate[i].bottom(5.8))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.move_to(sample_plate[i].top(-5))
        m300.blow_out()
        protocol.delay(seconds=2)
        m300.touch_tip(v_offset=-5, radius=0.7)
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.mix(3, 150, incubation_plate[i].bottom(3))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(150, incubation_plate[i].bottom(2))
        m300.dispense(150, sample_plate[i].bottom(5.8))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.move_to(sample_plate[i].top(-5))
        m300.blow_out()
        protocol.delay(seconds=2)
        m300.touch_tip(v_offset=-5, radius=0.7)
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.mix(3, 100, incubation_plate[i].bottom(2))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(100, incubation_plate[i].bottom(0.8))
        m300.dispense(100, sample_plate[i].bottom(5.8))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.move_to(sample_plate[i].top(-5))
        m300.blow_out()
        protocol.delay(seconds=2)
        m300.touch_tip(v_offset=-5, radius=0.7)
        m300.air_gap(height=2)
        m300.return_tip()

    # for i in list_of_cols[3:6]:
    #     m300.pick_up_tip(tipracks_200_1[i])
    #     m300.flow_rate.aspirate = 150
    #     m300.flow_rate.dispense = 150
    #     m300.mix(3, 200, incubation_plate[i].bottom(5))
    #     m300.flow_rate.aspirate = 50
    #     m300.flow_rate.dispense = 50
    #     m300.aspirate(200, incubation_plate[i].bottom(4.8))
    #     m300.dispense(200, sample_plate[i].bottom(5.8))
    #     m300.flow_rate.aspirate = 100
    #     m300.flow_rate.dispense = 100
    #     m300.move_to(sample_plate[i].top(-5))
    #     m300.blow_out()
    #     protocol.delay(seconds=2)
    #     m300.touch_tip(v_offset=-5, radius=0.7)
    #     m300.flow_rate.aspirate = 150
    #     m300.flow_rate.dispense = 150
    #     m300.mix(3, 150, incubation_plate[i].bottom(2))
    #     m300.flow_rate.aspirate = 50
    #     m300.flow_rate.dispense = 50
    #     m300.aspirate(200, incubation_plate[i].bottom(1.5))
    #     m300.dispense(200, sample_plate[i].bottom(5.8))
    #     m300.flow_rate.aspirate = 100
    #     m300.flow_rate.dispense = 100
    #     m300.move_to(sample_plate[i].top(-5))
    #     m300.blow_out()
    #     protocol.delay(seconds=2)
    #     m300.touch_tip(v_offset=-5, radius=0.7)
    #     m300.air_gap(height=2)
    #     m300.return_tip()

    # engage the magnetic module
    mag_deck.engage(height=34)

    ## Prepare RNA_plate
    ## Add beads and EtOH binding buffer (trough col 4) to RNA plate (col 1 to 3)

    m300.pick_up_tip(tipracks_200_2['A1'])

    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind1.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind1.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind1.bottom(9.8))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind1.bottom(4.8))
    m300.dispense(175, RNA_plate['A1'].bottom(5.8))
    # m300.flow_rate.aspirate = 200
    # m300.flow_rate.dispense = 200
    # m300.mix(2, 200, EtOH_Bind1.bottom(3))
    # m300.mix(2, 200, EtOH_Bind1.bottom(5))
    # m300.mix(1, 200, EtOH_Bind1.bottom(8))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind1.bottom(9.8))
    m300.dispense(175, RNA_plate['A1'].bottom(5.8))
    m300.move_to(RNA_plate['A1'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind1.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind1.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind1.bottom(9.8))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind1.bottom(4.8))
    m300.dispense(175, RNA_plate['A2'].bottom(5.8))
    # m300.flow_rate.aspirate = 200
    # m300.flow_rate.dispense = 200
    # m300.mix(2, 200, EtOH_Bind1.bottom(5))
    # m300.mix(1, 200, EtOH_Bind1.bottom(8))
    # m300.mix(2, 200, EtOH_Bind1.bottom(3))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind1.bottom(6.8))
    m300.dispense(175, RNA_plate['A2'].bottom(5.8))
    m300.move_to(RNA_plate['A2'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind1.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind1.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind1.bottom(9.8))
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind1.bottom(4.8))
    m300.dispense(175, RNA_plate['A3'].bottom(5.8))
    # m300.flow_rate.aspirate = 200
    # m300.flow_rate.dispense = 200
    # m300.mix(2, 200, EtOH_Bind1.bottom(3))
    # m300.mix(2, 200, EtOH_Bind1.bottom(5))
    # m300.mix(1, 200, EtOH_Bind1.bottom(8))
    m300.aspirate(175, EtOH_Bind1.bottom(4.8))
    m300.dispense(175, RNA_plate['A3'].bottom(5.8))
    m300.move_to(RNA_plate['A3'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.return_tip()

    ## Add beads and EtOH binding buffer (trough col 5) to RNA plate (col 4 to 6)
    m300.pick_up_tip(tipracks_200_2['A2'])

    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind2.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(9.8))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(11.8))
    m300.dispense(175, RNA_plate['A4'].bottom(5.8))
    # m300.flow_rate.aspirate = 200
    # m300.flow_rate.dispense = 200
    # m300.mix(2, 200, EtOH_Bind2.bottom(3))
    # m300.mix(2, 200, EtOH_Bind2.bottom(5))
    # m300.mix(1, 200, EtOH_Bind2.bottom(8))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(9.8))
    m300.dispense(175, RNA_plate['A4'].bottom(5.8))
    m300.move_to(RNA_plate['A4'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind2.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(9.8))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(9.8))
    m300.dispense(175, RNA_plate['A5'].bottom(5.8))
    # m300.flow_rate.aspirate = 200
    # m300.mix(2, 200, EtOH_Bind2.bottom(3))
    # m300.flow_rate.dispense = 200
    # m300.mix(1, 200, EtOH_Bind2.bottom(8))
    # m300.mix(2, 200, EtOH_Bind2.bottom(5))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(6.8))
    m300.dispense(175, RNA_plate['A5'].bottom(5.8))
    m300.move_to(RNA_plate['A5'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind2.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(9.8))
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A6'].bottom(5.8))
    # m300.flow_rate.aspirate = 200
    # m300.flow_rate.dispense = 200
    # m300.mix(2, 200, EtOH_Bind2.bottom(3))
    # m300.mix(2, 200, EtOH_Bind2.bottom(5))
    # m300.mix(1, 200, EtOH_Bind2.bottom(8))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A6'].bottom(5.8))
    m300.move_to(RNA_plate['A6'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.return_tip()

    ## Add beads and EtOH binding buffer (trough col 5) to RNA plate (col 7 to 9)
    # m300.pick_up_tip(tipracks_200_2['A3'])
    #
    # m300.flow_rate.aspirate = 150
    # m300.flow_rate.dispense = 150
    # m300.mix(5, 200, EtOH_Bind3.bottom(3))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    # m300.transfer(350, EtOH_Bind3.bottom(7), RNA_plate['A7'].bottom(4), new_tip='never')
    # m300.move_to(RNA_plate['A7'].top(-6))
    # m300.blow_out()
    # protocol.delay(seconds=5)
    #
    # m300.flow_rate.aspirate = 150
    # m300.flow_rate.dispense = 150
    # m300.mix(5, 200, EtOH_Bind3.bottom(3))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    # m300.transfer(350, EtOH_Bind3.bottom(5), RNA_plate['A8'].bottom(4), new_tip='never')
    # m300.move_to(RNA_plate['A8'].top(-6))
    # m300.blow_out()
    # protocol.delay(seconds=5)
    #
    # m300.flow_rate.aspirate = 150
    # m300.flow_rate.dispense = 150
    # m300.mix(5, 200, EtOH_Bind3.bottom(3))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    # m300.transfer(350, EtOH_Bind3.bottom(3), RNA_plate['A9'].bottom(4), new_tip='never')
    # m300.move_to(RNA_plate['A9'].top(-6))
    # m300.blow_out()
    # protocol.delay(seconds=5)
    #
    # m300.return_tip()

    ## Add beads and EtOH binding buffer (trough col 5) to RNA plate (col 10 to 12)
    # m300.pick_up_tip(tipracks_200_2['A4'])
    #
    # m300.flow_rate.aspirate = 150
    # m300.flow_rate.dispense = 150
    # m300.mix(5, 200, EtOH_Bind4.bottom(3))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    # m300.transfer(350, EtOH_Bind4.bottom(7), RNA_plate['A10'].bottom(4), new_tip='never')
    # m300.move_to(RNA_plate['A10'].top(-6))
    # m300.blow_out()
    # protocol.delay(seconds=5)
    #
    # m300.flow_rate.aspirate = 150
    # m300.flow_rate.dispense = 150
    # m300.mix(5, 200, EtOH_Bind4.bottom(3))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    # m300.transfer(350, EtOH_Bind4.bottom(5), RNA_plate['A11'].bottom(4), new_tip='never')
    # m300.move_to(RNA_plate['A11'].top(-6))
    # m300.blow_out()
    # protocol.delay(seconds=5)
    #
    # m300.flow_rate.aspirate = 150
    # m300.flow_rate.dispense = 150
    # m300.mix(5, 200, EtOH_Bind4.bottom(3))
    # m300.flow_rate.aspirate = 50
    # m300.flow_rate.dispense = 50
    # m300.transfer(350, EtOH_Bind4.bottom(3), RNA_plate['A12'].bottom(4), new_tip='never')
    # m300.move_to(RNA_plate['A12'].top(-6))
    # m300.blow_out()
    # protocol.delay(seconds=5)
    #
    # m300.return_tip()

    ## Transfer supernatant from DNA_plate to RNA_plate
    # first 3 cols mixed at different heights to see if the solution gets mixed properly
    for i in list_of_cols[:3]:
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(175, sample_plate[i].bottom(3.8))
        m300.dispense(175, RNA_plate[i].top(-5))       # is height.bottom = 8 good?
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        #m300.mix(3, 200, RNA_plate[i].bottom(6)) # do not mix to avoid to touch the EtOH and in this way bring it back to the DNA_plate
        #protocol.delay(seconds=5)
        m300.blow_out(RNA_plate[i].top(-3))
        #m300.air_gap(height=2)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.flow_rate.dispense = 50
        m300.aspirate(175, sample_plate[i].bottom(2.8))
        m300.dispense(175, RNA_plate[i].bottom(5.8))
        #protocol.delay(seconds=5)
        #m300.blow_out(RNA_plate[i].top(-5))
        m300.flow_rate.aspirate = 80
        m300.flow_rate.dispense = 200
        #m300.air_gap(height=2)
        m300.mix(1, 200, RNA_plate[i].bottom(11.8))
        m300.mix(1, 200, RNA_plate[i].bottom(8.8))
        m300.mix(1, 200, RNA_plate[i].bottom(5.8))
        m300.move_to(RNA_plate[i].top(-3))
        protocol.delay(seconds=5)
        m300.blow_out(RNA_plate[i].top(-3))
        #m300.air_gap(height=2)
        m300.touch_tip(v_offset=-5, radius=0.8)
        protocol.delay(seconds=2)
        #m300.drop_tip()
        m300.return_tip()


    #### Transfer supernatant from DNA_plate to RNA_plate
    for i in list_of_cols[3:6]:
        m300.pick_up_tip(tipracks_200_3[i]) # Slow down head speed 0.5X for bead handling
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(175, sample_plate[i].bottom(3.8))
        m300.dispense(175, RNA_plate[i].top(-5))       # is height.bottom = 8 good?
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        #m300.mix(3, 200, RNA_plate[i].bottom(6)) # do not mix to avoid to touch the EtOH and in this way bring it back to the DNA_plate
        #protocol.delay(seconds=5)
        m300.blow_out(RNA_plate[i].top(-3))
        #m300.air_gap(height=2)
        m300.touch_tip(v_offset=-5, radius=0.8)
        m300.flow_rate.dispense = 50
        m300.aspirate(175, sample_plate[i].bottom(2.8))
        m300.dispense(175, RNA_plate[i].bottom(5.8))
        #protocol.delay(seconds=5)
        #m300.blow_out(RNA_plate[i].top(-5))
        #m300.air_gap(height=2)
        m300.flow_rate.aspirate = 80
        m300.flow_rate.dispense = 200
        m300.mix(1, 200, RNA_plate[i].bottom(5.8))
        m300.mix(1, 200, RNA_plate[i].bottom(8.8))
        m300.mix(1, 200, RNA_plate[i].bottom(11.8))
        m300.move_to(RNA_plate[i].top(-3))
        protocol.delay(seconds=5)
        m300.blow_out(RNA_plate[i].top(-3))
        #m300.air_gap(height=2)
        m300.touch_tip(v_offset=-5, radius=0.8)
        protocol.delay(seconds=2)
        m300.return_tip()

    mag_deck.disengage()

    protocol.pause("Cover DNA plate with aluminium seal and store in fridge until purification the same or following day. Continue with RNA purification.")

    ############################
    ###### Job is done! ######
    ############################
