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
    'date': '2021/08/23',
    'description': 'Automation of D-Rex RNA and DNA separation for extraction protocol',
}

# the total volume is calculated for 110 samples instead of 96

def run(protocol):

    ## MODULE SETUP ##
    mag_deck = protocol.load_module('magdeck', 10)
    # Load a Temperature Module GEN1 in deck slot 7
    temp_deck = protocol.load_module('tempdeck', 7)

    ## LABWARE SETUP ##
    # the sample plate is a deep-well plate with V-bottom + adaptor (the adaptor is used just on the magnetic module)
    sample_plate = mag_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')
    incubation_plate = temp_deck.load_labware('biorad_96_wellplate_1000ul_w_adaptor')
    trough = protocol.load_labware('usascientific_12_reservoir_22ml', 2)
    RNA_plate = protocol.load_labware('biorad_96_wellplate_1000ul', 1)

    tipracks_200_1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4)
    tipracks_200_2 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)   # only first 2 cols needed for transfering beads and EtOH binding buffer to RNA_plate
    tipracks_200_3 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 9)

    ## PIPETTE SETUP ##
    m300 = protocol.load_instrument('p300_multi_gen2', mount='left',
                                    tip_racks=(tipracks_200_1, tipracks_200_2, tipracks_200_3))

    ## REAGENT SETUP ##                       description             Volume needed for protocol
    Binding_buffer1 = trough['A1']            # Buffer B1:              11 ml
    #Binding_buffer2 = trough['A2'] 		  # Buffer B1:              11 ml   # not neeeded if running half plate

    ### If running complete plate, move EtOH1_Bind1 to trough['A3'] and EtOH1_Bind2 to trough['A4']
    EtOH_Bind1 = trough['A2']                 # EtOH + magnetic:       10.8 ml EtOH + 405ul beads
    EtOH_Bind2 = trough['A3']                 # EtOH + magnetic:       10.8 ml EtOH + 405ul beads
    #EtOH_Bind3 = trough['A5']                # EtOH + magnetic:       10.8 ml EtOH + 405ul beads    # not neeeded if running half plate
    #EtOH_Bind4 = trough['A6']                # EtOH + magnetic:       10.8 ml EtOH + 405ul beads    # not neeeded if running half plate

    ## Plate SETUP ##
    #list_of_cols = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']        # 12 columns
    list_of_cols = ['A1','A2','A3','A4','A5','A6']                                          # 6 columns

    ## VOLUME SETUP ##
    Sample_vol = 200
    Binding_buffer_vol = Sample_vol*1
    EtOH_buffer_vol = 175

    #### PROTOCOL ####

    ## Place plate with sample above temp_deck
    mag_deck.disengage()

    ### Transfer buffer B1 and beads (trough col 1) to incubation plate with samples (col 1 to 6)
    for i in list_of_cols[:6]:
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.pick_up_tip(tipracks_200_1[i])
        m300.mix(4, Binding_buffer_vol, Binding_buffer1.bottom(4.8))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(4.8))
        m300.dispense(Binding_buffer_vol, incubation_plate[i].bottom(5.8))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(4, Binding_buffer_vol, incubation_plate[i].bottom(6.8))
        m300.move_to(incubation_plate[i].top(-5))
        protocol.delay(seconds=5)
        m300.blow_out()
        m300.touch_tip(v_offset=-5, radius=0.7)
        m300.air_gap(height=2)
        m300.return_tip()


### Transfer buffer B2 and beads (trough col 2) to incubation plate (col 7 to 12)
    for i in list_of_cols[6:]:
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.pick_up_tip(tipracks_200_1[i])
        m300.mix(4, Binding_buffer_vol, Binding_buffer1.bottom(4.8))
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(Binding_buffer_vol, Binding_buffer1.bottom(4.8))
        m300.dispense(Binding_buffer_vol, incubation_plate[i].bottom(5.8))
        m300.flow_rate.aspirate = 100
        m300.flow_rate.dispense = 100
        m300.mix(4, Binding_buffer_vol, incubation_plate[i].bottom(6.8))
        m300.move_to(incubation_plate[i].top(-5))
        protocol.delay(seconds=5)
        m300.blow_out()
        m300.touch_tip(v_offset=-5, radius=0.7)
        m300.air_gap(height=2)
        m300.return_tip()

    temp_deck.set_temperature(10)

    # Incubate the samples at 10°C for 15 minutes
    protocol.delay(minutes=15)
    temp_deck.deactivate()

    # Transfer all the 400ul (buffer b1 and beads + sample) into the rack on the magnetic module (col 1 to 6) using same tips as before
    for i in list_of_cols[:6]:
        m300.pick_up_tip(tipracks_200_1[i])
        # velocity for mixing
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.mix(3, 170, incubation_plate[i].bottom(5))
        # velocity for aspiration and dispensing (slower)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(150, incubation_plate[i].bottom(4.8))
        m300.dispense(150, sample_plate[i].bottom(5.8))
        # velocity for blowing out
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
        m300.flow_rate.dispense = 100
        m300.move_to(sample_plate[i].top(-5))
        m300.blow_out()
        protocol.delay(seconds=2)
        m300.touch_tip(v_offset=-5, radius=0.7)
        m300.air_gap(height=2)
        m300.return_tip()

    for i in list_of_cols[6:]:
        m300.pick_up_tip(tipracks_200_1[i])
        # velocity for mixing
        m300.flow_rate.aspirate = 150
        m300.flow_rate.dispense = 150
        m300.mix(3, 170, incubation_plate[i].bottom(5))
        # velocity for aspiration and dispensing (slower)
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(150, incubation_plate[i].bottom(4.8))
        m300.dispense(150, sample_plate[i].bottom(5.8))
        # velocity for blowing out
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
        m300.flow_rate.dispense = 100
        m300.move_to(sample_plate[i].top(-5))
        m300.blow_out()
        protocol.delay(seconds=2)
        m300.touch_tip(v_offset=-5, radius=0.7)
        m300.air_gap(height=2)
        m300.return_tip()


    # Engage the magnetic module
    mag_deck.engage(height=34)

    ## Prepare RNA_plate
    ## Add beads and EtOH binding buffer (trough col 3) to RNA plate (col 1 to 3)
        # Here each chunk is for one RNA rack's column preparation since the height for aspirating
        # EtOH + beads has to change everytime to get a homogenous amount of beads across all columns
    # the tip is changed every 3 columns
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
    m300.aspirate(175, EtOH_Bind1.bottom(9.8))          # step where the height changes
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
    m300.aspirate(175, EtOH_Bind1.bottom(4.8))
    m300.dispense(175, RNA_plate['A3'].bottom(5.8))
    m300.move_to(RNA_plate['A3'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.return_tip()

    ## Add beads and EtOH binding buffer (trough col 4) to RNA plate (col 4 to 6)
    m300.pick_up_tip(tipracks_200_2['A2'])
    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind2.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(9.8))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A4'].bottom(5.8))
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
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A5'].bottom(5.8))
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
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A6'].bottom(5.8))
    m300.move_to(RNA_plate['A6'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.return_tip()

    ## Add beads and EtOH binding buffer (trough col 5) to RNA plate (col 7 to 9)
    m300.pick_up_tip(tipracks_200_2['A3'])
    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind2.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(9.8))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A7'].bottom(5.8))
    m300.aspirate(175, EtOH_Bind2.bottom(9.8))
    m300.dispense(175, RNA_plate['A7'].bottom(5.8))
    m300.move_to(RNA_plate['A7'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind2.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(9.8))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A8'].bottom(5.8))
    m300.aspirate(175, EtOH_Bind2.bottom(6.8))
    m300.dispense(175, RNA_plate['A8'].bottom(5.8))
    m300.move_to(RNA_plate['A8'].top(-5))
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
    m300.dispense(175, RNA_plate['A9'].bottom(5.8))
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A9'].bottom(5.8))
    m300.move_to(RNA_plate['A9'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.return_tip()

    ## Add beads and EtOH binding buffer (trough col 5) to RNA plate (col 10 to 12)
    m300.pick_up_tip(tipracks_200_2['A4'])
    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind2.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(9.8))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A10'].bottom(5.8))
    m300.aspirate(175, EtOH_Bind2.bottom(9.8))
    m300.dispense(175, RNA_plate['A10'].bottom(5.8))
    m300.move_to(RNA_plate['A10'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.flow_rate.aspirate = 200
    m300.flow_rate.dispense = 200
    m300.mix(2, 200, EtOH_Bind2.bottom(4.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(6.8))
    m300.mix(2, 200, EtOH_Bind2.bottom(9.8))
    m300.flow_rate.aspirate = 50
    m300.flow_rate.dispense = 50
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A11'].bottom(5.8))
    m300.aspirate(175, EtOH_Bind2.bottom(6.8))
    m300.dispense(175, RNA_plate['A11'].bottom(5.8))
    m300.move_to(RNA_plate['A11'].top(-5))
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
    m300.dispense(175, RNA_plate['A12'].bottom(5.8))
    m300.aspirate(175, EtOH_Bind2.bottom(4.8))
    m300.dispense(175, RNA_plate['A12'].bottom(5.8))
    m300.move_to(RNA_plate['A12'].top(-5))
    m300.blow_out()
    protocol.delay(seconds=5)

    m300.return_tip()

    ## Transfer supernatant from DNA_plate to RNA_plate
    # first 3 cols mixed at different heights to mix properly the solution
    for i in list_of_cols[:3]:
        m300.pick_up_tip(tipracks_200_3[i])
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
        m300.pick_up_tip(tipracks_200_3[i])
        m300.flow_rate.aspirate = 50
        m300.flow_rate.dispense = 50
        m300.aspirate(175, sample_plate[i].bottom(3.8))
        m300.dispense(175, RNA_plate[i].top(-5))
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
