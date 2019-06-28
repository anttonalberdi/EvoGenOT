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
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'D-Rex RNA Extraction',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/03/28',
    'description': 'Automation of D-Rex RNA protocol for stool samples in SHIELD',
}


#### LABWARE SETUP ####
elution_plate_DNA = labware.load('96-flat', '3')
trough = labware.load('trough-12row', '2')
RNA_plate = labware.load('96-deep-well', '7')
mag_deck = modules.load('magdeck', '7')
temp_deck = modules.load('tempdeck', '10')
trash_box = labware.load('trash-box', '8')

tipracks_200 = [labware.load('tiprack-200ul', slot)
               for slot in ['4','5','6','11']]



#### PIPETTE SETUP ####
p50 = instruments.P50_Single(
    mount='left',
    tip_racks=tipracks_200)

m300 = instruments.P300_Multi(
    mount='right',
    tip_racks=tipracks_200)

#### REAGENT SETUP
Elution_buffer = trough.wells('A4')

EtOH1 = trough.wells('A5')
EtOH2 = trough.wells('A6')
EtOH3 = trough.wells('A7')
EtOH4 = trough.wells('A8')
Wash = trough.wells('A9')
BufferC = trough.wells('A10')
DNase = trough.wells('A11')


Liquid_trash = trash_box.wells('A1')

#### VOLUME SETUP


Sample_vol = 200
EtOH_vol = 2.0*Sample_vol
Wash_1_vol = 1.0*Sample_vol
Wash_2_vol = 1.0*Sample_vol
Elution_vol = 50


#### PROTOCOL ####
## Ethanol Wash 1
mag_deck.disengage()
m300.distribute(Wash_1_vol, EtOH1, [well.top() for well in RNA_plate.wells()] , new_tip='once',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)
m300.transfer(Wash_1_vol, [well.bottom() for well in RNA_plate.wells()], Liquid_trash, new_tip='always',  blow_out =True)

## Ethanol Wash 2
mag_deck.disengage()
m300.distribute(Wash_2_vol, EtOH2, [well.top() for well in RNA_plate.wells()], new_tip='once',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)
m300.transfer(Wash_2_vol, [well.bottom() for well in RNA_plate.wells()], Liquid_trash, new_tip='always',  blow_out =True)

## Dry beads before DNase treatment
m300.delay(minutes=5)
m300.distribute(30, DNase, [well.top() for well in RNA_plate.wells()], new_tip='once',  blow_out =True)
m300.delay(minutes=10)

## Buffer C rebind
mag_deck.disengage()
m300.distribute(200, BufferC, [well.top() for well in RNA_plate.wells()], new_tip='once',  blow_out =True)
m300.delay(minutes=10)
mag_deck.engage(height=12)
m300.delay(minutes=2)
m300.transfer(200, [well.bottom() for well in RNA_plate.wells()], Liquid_trash, new_tip='always',  blow_out =True)

## Ethanol Wash 3
mag_deck.disengage()
m300.distribute(EtOH_vol, Ethanol_1, [well.top() for well in RNA_plate.wells()], new_tip='once',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=5)
m300.transfer(Wash_1_vol, [well.bottom() for well in RNA_plate.wells()], Liquid_trash, new_tip='always',  blow_out =True)

## Ethanol Wash 4
mag_deck.disengage()
m300.distribute(EtOH_vol, Ethanol_2, [well.top() for well in RNA_plate.wells()], new_tip='once',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=5)
m300.transfer(500, [well.bottom() for well in RNA_plate.wells()], Liquid_trash, new_tip='always',  blow_out =True)

## Dry beads before elution
m300.delay(minutes=10)

## Elution
mag_deck.disengage()
m300.distribute(Elution_vol, Elution_buffer, [well.bottom() for well in RNA_plate.wells(), new_tip='always',  blow_out =True])
mag_deck.engage(height=12)
m300.delay(minutes=5)
m300.transfer(40, [well.bottom() for well in RNA_plate.wells(), [well.bottom() for well in elution_plate_DNA.wells(), new_tip='always',  blow_out =True])

robot.comment("Job's done")
