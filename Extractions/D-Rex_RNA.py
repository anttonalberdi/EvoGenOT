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
elution_plate_DNA = labware.load('96-flat', '1')
trough = labware.load('trough-12row', '2')
RNA_plate = labware.load('96-deep-well', '7')
mag_deck = modules.load('magdeck', '7')
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
Wash_2_vol = 0.9*Sample_vol
Elution_vol = 50


#### PROTOCOL ####
## Ethanol Wash 1
mag_deck.disengage()
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('1').top(-2) , new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('2').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('3').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('4').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('5').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('6').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('7').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('8').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('9').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('10').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('11').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH1, RNA_plate.cols('12').top(-2) , new_tip='never',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)

m300.transfer(Wash_1_vol, RNA_plate.cols('1').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('2').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('3').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('4').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('5').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('6').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('7').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('8').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('9').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('10').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('11').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('12').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)


## Ethanol Wash 2
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('1').top(-2) , new_tip='once',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('2').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('3').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('4').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('5').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('6').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('7').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('8').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('9').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('10').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('11').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH2, RNA_plate.cols('12').top(-2) , new_tip='never',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)
m300.transfer(200, RNA_plate.cols('1').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('2').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('3').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('4').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('5').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('6').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('7').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('8').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('9').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('10').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('11').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('12').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)

## Dry beads before DNase treatment
m300.delay(minutes=5)
m300.distribute(30, DNase, RNA_plate.cols('1').top(-2), new_tip='once',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('2').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('3').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('4').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('5').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('6').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('7').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('8').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('9').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('10').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('11').top(-2), new_tip='never',  blow_out =True)
m300.distribute(30, DNase, RNA_plate.cols('12').top(-2), new_tip='never',  blow_out =True)

m300.delay(minutes=10)

## Buffer C rebind
mag_deck.disengage()
m300.distribute(200, BufferC, RNA_plate.cols('1').top(), new_tip='once',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('2').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('3').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('4').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('5').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('6').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('7').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('8').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('9').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('10').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('11').top(), new_tip='never',  blow_out =True)
m300.distribute(200, BufferC, RNA_plate.cols('12').top(), new_tip='never',  blow_out =True)


m300.delay(minutes=10)
mag_deck.engage(height=12)
m300.delay(minutes=2)
m300.transfer(200, RNA_plate.cols('1').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('2').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('3').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('4').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('5').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('6').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('7').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('8').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('9').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('10').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('11').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('12').bottom(2), Liquid_trash, new_tip='always',  blow_out =True)

## Ethanol Wash 3
mag_deck.disengage()
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('1').top(-2) , new_tip='once',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('2').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('3').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('4').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('5').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('6').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('7').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('8').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('9').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('10').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('11').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_1_vol, EtOH3, RNA_plate.cols('12').top(-2) , new_tip='never',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)

m300.transfer(Wash_1_vol, RNA_plate.cols('1').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('2').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('3').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('4').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('5').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('6').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('7').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('8').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('9').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('10').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('11').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(Wash_1_vol, RNA_plate.cols('12').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)

## Ethanol Wash 4
mag_deck.disengage()
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('1').top(-2) , new_tip='once',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('2').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('3').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('4').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('5').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('6').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('7').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('8').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('9').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('10').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('11').top(-2) , new_tip='never',  blow_out =True)
m300.transfer(Wash_2_vol, EtOH4, RNA_plate.cols('12').top(-2) , new_tip='never',  blow_out =True)
mag_deck.engage(height=12)
m300.delay(minutes=2)
m300.transfer(200, RNA_plate.cols('1').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('2').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('3').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('4').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('5').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('6').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('7').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('8').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('9').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('10').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('11').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)
m300.transfer(200, RNA_plate.cols('12').bottom(1), Liquid_trash, new_tip='always',  blow_out =True)

## Dry beads before elution
m300.delay(minutes=10)

## Elution
mag_deck.disengage()
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('1').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('2').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('3').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('4').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('5').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('6').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('7').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('8').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('9').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('10').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('11').bottom(5), new_tip='always',  blow_out =True])
m300.distribute(Elution_vol, Elution_buffer, RNA_plate.cols('12').bottom(5), new_tip='always',  blow_out =True])
mag_deck.engage(height=12)
m300.delay(minutes=5)

m300.transfer(40, RNA_plate.cols('1').bottom(2),elution_plate_DNA.cols('1').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('2').bottom(2),elution_plate_DNA.cols('2').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('3').bottom(2),elution_plate_DNA.cols('3').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('4').bottom(2),elution_plate_DNA.cols('4').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('5').bottom(2),elution_plate_DNA.cols('5').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('6').bottom(2),elution_plate_DNA.cols('6').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('7').bottom(2),elution_plate_DNA.cols('7').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('8').bottom(2),elution_plate_DNA.cols('8').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('9').bottom(2),elution_plate_DNA.cols('9').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('10').bottom(2),elution_plate_DNA.cols('10').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('11').bottom(2),elution_plate_DNA.cols('11').bottom(), new_tip='always',  blow_out =True])
m300.transfer(40, RNA_plate.cols('12').bottom(2),elution_plate_DNA.cols('12').bottom(), new_tip='always',  blow_out =True])

robot.comment("Job's done")
