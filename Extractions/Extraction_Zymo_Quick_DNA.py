## Description of procedure ##
#
#
# Things do before procedure
#
#	1. Bead beat samples at maximum speed for 5 minutes
# 	2. Spin down samples 10.000 rpm for 1 minute
#	3. Transfer 200µl lysed sample to a deep well plate

### Procedure ###
#
#	https://files.zymoresearch.com/protocols/_r2130_r2131_quick-dna_rna_magbead.pdf
#	Purification of DNA (p. 6)
#

######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'Extraction_Quick_DNA',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/03/28',
    'description': 'Automation of Zymo Quick DNA protocol for stool samples in SHIELD',
}


#### LABWARE SETUP ####
elution_plate_DNA = labware.load('96-flat', '3')
trough = labware.load('trough-12row', '2')
buffer = labware.load('opentrons-tuberack-50ml', '8')
trash_box = labware.load('trash-box', '1')
mag_deck = modules.load('magdeck', '7')
sample_plate = labware.load('96-deep-well', '7', share=True)
temp_deck = modules.load('tempdeck', '10')


tipracks_200 = [labware.load('tiprack-200ul', slot)
               for slot in ['4','5','6','11']]

tipracks_1000 = [labware.load('tiprack-1000ul', slot, share=True)
                for slot in ['9']]


#### PIPETTE SETUP ####
s1000 = instruments.P1000_Single(
    mount='right',
    tip_racks=tipracks_1000)

m300 = instruments.P300_Multi(
    mount='left',
    tip_racks=tipracks_200)

#### REAGENT SETUP

Beads = trough.wells('A1')
Elution_buffer = trough.wells('A2')

Liquid_trash = trash_box.wells('A1')


Sample_buffer = buffer.wells('A1')
Ethanol_1 = buffer.wells('A2')
Ethanol_2 = buffer.wells('A3')
Wash_1 = buffer.wells('B2')
Wash_2 = buffer.wells('B3')


#### VOLUME SETUP


Sample_vol = 200
Sample_buffer_vol = 2.5*Sample_vol
Bead_vol = 30
EtOH_vol = 2.5*Sample_vol
Wash_1_vol = 2.5*Sample_vol
Wash_2_vol = 2.5*Sample_vol
Elution_vol = 75


#### PROTOCOL ####
## add beads and sample buffer
mag_deck.disengage()
s1000.distribute(Sample_buffer_vol, Sample_buffer, [well.top() for well in sample_plate.wells()],mix_after=(3,500) , new_tip='once',  blow_out =True)
m300.distribute(Bead_vol, Beads, sample_plate.wells(), mix_after=(3,150) , new_tip='always',  blow_out =True)
m300.delay(minutes=10)
m300.distribute(0, Beads, sample_plate.wells(), mix_after=(3,150) , new_tip='always',  blow_out =True)
m300.delay(minutes=5)

## Remove supernatant
mag_deck.engage()
s1000.delay(minutes=5)
m300.transfer(700, [well.bottom() for well in sample_plate.wells()], Liquid_trash , new_tip='always',  blow_out =True)

## Wash 1
mag_deck.disengage()
s1000.distribute(Wash_1_vol, Wash_1, [well.top() for well in sample_plate.wells()] , new_tip='once',  blow_out =True)
mag_deck.engage()
m300.delay(minutes=5)
m300.transfer(500, [well.bottom() for well in sample_plate.wells()], Liquid_trash, new_tip='always',  blow_out =True)

robot.pause("The 300 uL tips have run out. Please replace tipracks. Resume \
when the tips are replenished.")
m300.reset_tip_tracking()

## Wash 2
mag_deck.disengage()
s1000.distribute(Wash_2_vol, Wash_2, [well.top() for well in sample_plate.wells()], new_tip='once',  blow_out =True)
mag_deck.engage()
m300.delay(minutes=5)
m300.transfer(500, [well.bottom() for well in sample_plate.wells()], Liquid_trash, new_tip='always',  blow_out =True)

## Ethanol Wash 1
mag_deck.disengage()
s1000.distribute(EtOH_vol, Ethanol_1, [well.top() for well in sample_plate.wells()], new_tip='once',  blow_out =True)
mag_deck.engage()
m300.delay(minutes=5)
m300.transfer(500, [well.bottom() for well in sample_plate.wells()], Liquid_trash, new_tip='always',  blow_out =True)

## Ethanol Wash 2
mag_deck.disengage()
s1000.distribute(EtOH_vol, Ethanol_2, [well.top() for well in sample_plate.wells()], new_tip='once',  blow_out =True)
mag_deck.engage()
m300.delay(minutes=5)
m300.transfer(500, [well.bottom() for well in sample_plate.wells()], Liquid_trash, new_tip='always',  blow_out =True)

## Dry beads
temp_deck.set_temperature(55)
temp_deck.wait_for_temp()
robot.pause("Put the plate on the Temperature Module for 20 minutes at 55°C \The 300 uL tips have run out. Please replace tipracks. Resume \
when the tips are replenished.")

m300.reset_tip_tracking()

## Elution
mag_deck.disengage()
m300.distribute(Elution_vol, Elution_buffer, [well.bottom() for well in sample_plate.wells()], new_tip='always',  blow_out =True)
mag_deck.engage()
m300.delay(minutes=5)
m300.distribute(Elution_vol, [well.bottom() for well in sample_plate.wells()], [well.bottom() for well in elution_plate_DNA.wells()], new_tip='always',  blow_out =True)


robot.comment("Job's done")
