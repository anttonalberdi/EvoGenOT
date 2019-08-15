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
    'version': '1.0-optimized',
    'date': '2019/08/15',
    'description': 'Automation of D-Rex RNA protocol for stool samples in SHIELD',
}

### Custom LABWARE load
plate_name = '1ml_magPCR'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7.5,                     # diameter (mm) of each well on the plate
        depth=26.4,                       # depth (mm) of each well on the plate
        volume=1000)

plate_name = 'One-Column-reservoir'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(1, 1),                    # specify amount of (columns, rows)
        spacing=(0, 0),               # distances (mm) between each (column, row)
        diameter=81,                     # diameter (mm) of each well on the plate
        depth=35,                       # depth (mm) of each well on the plate
        volume=350000)

#### LABWARE SETUP ####
elution_plate_RNA = labware.load('biorad-hardshell-96-PCR', '1')
trough = labware.load('trough-12row', '9')
mag_deck = modules.load('magdeck', '7')
RNA_plate = labware.load('1ml_magPCR', '7', share=True)
trash_box = labware.load('One-Column-reservoir', '8')
backup = labware.load('opentrons-tuberack-50ml', '6')

tipracks_200_1 = labware.load('tiprack-200ul', 2, share=True)
tipracks_200_2 = labware.load('tiprack-200ul', 3, share=True)
tipracks_200_3 = labware.load('tiprack-200ul', 4, share=True)
tipracks_200_4 = labware.load('tiprack-200ul', 5, share=True)

tipracks_1000 = labware.load('tiprack-1000ul', 11, share=True)



#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=([tipracks_200_1, tipracks_200_2, tipracks_200_3, tipracks_200_4]))

p1000 = instruments.P1000_Single(
    mount='left',
    aspirate_flow_rate=500,
    dispense_flow_rate=500,
    tip_racks=tipracks_1000)

#### REAGENT SETUP
EtOH1 = trough.wells('A5')
EtOH2 = trough.wells('A6')
EtOH3 = trough.wells('A7')
EtOH4 = trough.wells('A8')
DNase = trough.wells('A9')
BufferC_1 = trough.wells('A10')
BufferC_2 = trough.wells('A11')
Elution_buffer = trough.wells('A12')

Liquid_trash = trash_box.wells('A1')

#### Backup SETUP
ETOH_backup = backup.wells('A1')
BufferC_backup = backup.wells('A2')

#### Plate SETUP for Purification
RA1 = RNA_plate.wells('A1')
RA2 = RNA_plate.wells('A2')
RA3 = RNA_plate.wells('A3')
RA4 = RNA_plate.wells('A4')
RA5 = RNA_plate.wells('A5')
RA6 = RNA_plate.wells('A6')
RA7 = RNA_plate.wells('A7')
RA8 = RNA_plate.wells('A8')
RA9 = RNA_plate.wells('A9')
RA10 = RNA_plate.wells('A10')
RA11 = RNA_plate.wells('A11')
RA12 = RNA_plate.wells('A12')

#### VOLUME SETUP
Sample_vol = 200
EtOH_vol = 2.0*Sample_vol
Wash_1_vol = 1.0*Sample_vol
Wash_2_vol = 0.9*Sample_vol
Elution_vol = 50
BufferC_vol = 0.9*Sample_vol


#### PROTOCOL ####
## Remove supernatant, using tiprack 1
mag_deck.engage(height=34)
m300.delay(minutes=3)
m300.transfer(700, RA1.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA2.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA3.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA4.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA5.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA6.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA7.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA8.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA9.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA10.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA11.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)
m300.transfer(700, RA12.bottom(2), Liquid_trash.top(-4), new_tip='once',  blow_out =True)


mag_deck.disengage()

### Wash 1 with Ethanol, using tiprack 2
### Transfer Wash 1 to RA1
m300.set_flow_rate(aspirate=100, dispense=100)
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

### Transfer Wash 1 to RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH1.top(-20))
m300.aspirate(Wash_1_vol, EtOH1.top(-16))
m300.dispense(Wash_1_vol, RA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA2.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA3
m300.set_flow_rate(aspirate=100, dispense=100)
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

### Transfer Wash 1 to RA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, RA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA4.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, RA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA5.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, RA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA7.top(-10))
m300.blow_out()
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, ETOH_backup.top(-12))
p1000.dispense(800, EtOH1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH1.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-16))
p1000.dispense(800, EtOH1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH1.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-20))
p1000.dispense(800, EtOH1.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH1.top(-4))
p1000.blow_out()
p1000.return_tip()

### Transfer Wash 1 to RA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, RA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA7.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA7.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, RA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA8.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA8.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, RA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA9.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA9.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, RA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA10.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA10.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
m300.dispense(Wash_1_vol, RA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA11.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA11.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH1.bottom(1))
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

### Remove supernatant, by re-using tiprack 2
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

mag_deck.disengage()

## Ethanol Wash 2, by using tiprack 3
### Transfer Wash 2 to RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH2.top(-16))
m300.aspirate(Wash_2_vol, EtOH2.top(-12))
m300.dispense(Wash_2_vol, RA1.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA1.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA1.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.move_to(EtOH2.top(-20))
m300.aspirate(Wash_2_vol, EtOH2.top(-16))
m300.dispense(Wash_2_vol, RA2.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA2.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA2.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 2 to RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA3.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA3.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA3.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 2 to RA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA4.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA4.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA4.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 2 to RA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA5.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA5.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA5.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 2 to RA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA7.top(-10))
m300.blow_out()
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer in reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=500)
p1000.pick_up_tip()
p1000.aspirate(800, ETOH_backup.top(-12))
p1000.dispense(800, EtOH2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH2.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-16))
p1000.dispense(800, EtOH2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH2.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-20))
p1000.dispense(800, EtOH2.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH2.top(-4))
p1000.blow_out()
p1000.return_tip()

### Transfer Wash 1 to RA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA7.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA7.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA7.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA8.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA8.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA8.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA9.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA9.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA9.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA10.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA10.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA10.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
m300.dispense(Wash_2_vol, RA11.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA11.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA11.top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Wash 1 to RA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH2.bottom(1))
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

### Remove supernatant, by using re-using tiprack 3
mag_deck.engage(height=34)
m300.delay(minutes=2)

### remove supernatant from RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A1'))
m300.aspirate(Wash_2_vol, RA1.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA2
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A2'))
m300.aspirate(Wash_2_vol, RA2.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA3
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A3'))
m300.aspirate(Wash_2_vol, RA3.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA4
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A4'))
m300.aspirate(Wash_2_vol, RA4.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA5
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A5'))
m300.aspirate(Wash_2_vol, RA5.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA6
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A6'))
m300.aspirate(Wash_2_vol, RA6.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA7
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A7'))
m300.aspirate(Wash_2_vol, RA7.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA8
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A8'))
m300.aspirate(Wash_2_vol, RA8.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA9
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A9'))
m300.aspirate(Wash_2_vol, RA9.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA10
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A10'))
m300.aspirate(Wash_2_vol, RA10.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA11
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A11'))
m300.aspirate(Wash_2_vol, RA11.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

### remove supernatant from RA12
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip(tipracks_200_3.wells('A12'))
m300.aspirate(Wash_2_vol, RA12.bottom(1))
m300.dispense(Wash_2_vol, trash_box.wells('A1').top(-5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.blow_out(trash_box.wells('A1').top(-5))
m300.return_tip()

## Dry beads before DNase treatment
mag_deck.disengage()
m300.delay(minutes=1)

sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in RNA_plate.cols()[:col_num]]

### Adding DNAse, by using tiprack 4
m300.pick_up_tip()
for target in samples: # Slow down head speed 0.5X for bead handling
    m300.mix(2, 30, DNase)
    max_speed_per_axis = {'x': (300), 'y': (300), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.aspirate(30, DNase.bottom(1))
    m300.dispense(30, target.top(-10))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(target.top(-8))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
m300.drop_tip()

#incubating samples with DNase
robot.pause("Please cover the plate with film and incubate 10 min 25°C at 1300 rpm. Please fill up tips before continuing process")
##Reset tipracks for more tips
m300.reset()


### Buffer C rebind, by using tiprack 1
### Transfer buffer C and beads to RA1
m300.set_flow_rate(aspirate=100, dispense=100)
m300.pick_up_tip()
m300.move(BufferC_1.top(-16))
m300.mix(3, BufferC_vol, BufferC_1.top(-12))
max_speed_per_axis = {'x':(300), 'y':(300), 'z': (50), 'a': (20), 'b': (20), 'c': 20}
robot.head_speed(combined_speed=max(max_speed_per_axis.values()), **max_speed_per_axis)
m.set_flow_rate(aspirate=50, dispense=50)
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
m300.move_to(EtOH3.top(-16))
m300.aspirate(Wash_1_vol, EtOH3.top(-12))
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
m300.move_to(EtOH3.bottom())
m300.aspirate(Wash_1_vol, EtOH3.bottom(1))
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
m300.aspirate(Wash_1_vol, EtOH3.bottom(1))
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
m300.aspirate(Wash_1_vol, EtOH3.bottom())
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
m300.aspirate(Wash_1_vol, EtOH3.bottom())
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
m300.move_to(EtOH3.bottom())
m300.aspirate(Wash_1_vol, EtOH3.bottom())
m300.dispense(Wash_1_vol, RA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_1_vol, RA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA7.top(-10))
m300.blow_out()
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, ETOH_backup.top(-12))
p1000.dispense(800, EtOH3.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH3.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-16))
p1000.dispense(800, EtOH3.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH3.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-20))
p1000.dispense(800, EtOH3.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH3.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Wash 3 to RA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_1_vol, EtOH3.bottom())
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
m300.aspirate(Wash_1_vol, EtOH3.bottom())
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
m300.aspirate(Wash_1_vol, EtOH3.bottom())
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
m300.aspirate(Wash_1_vol, EtOH3.bottom())
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
m300.aspirate(Wash_1_vol, EtOH3.bottom())
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
m300.aspirate(Wash_1_vol, EtOH3.bottom())
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
m300.move_to(EtOH4.top(-16))
m300.aspirate(Wash_2_vol, EtOH4.top(-12))
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
m300.move_to(EtOH4.bottom())
m300.aspirate(Wash_2_vol, EtOH4.bottom(1))
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
m300.aspirate(Wash_2_vol, EtOH4.bottom(1))
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
m300.aspirate(Wash_2_vol, EtOH4.bottom())
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
m300.aspirate(Wash_2_vol, EtOH4.bottom())
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
m300.move_to(EtOH4.bottom())
m300.aspirate(Wash_2_vol, EtOH4.bottom())
m300.dispense(Wash_2_vol, RA6.top(-4))
m300.set_flow_rate(aspirate=100, dispense=100)
m300.mix(5, Wash_2_vol, RA6.bottom(5))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(RA7.top(-10))
m300.blow_out()
m300.return_tip()

#### Ensure enough buffer i reservoir by adding 3ml from backup
robot.comment("Ensure enough buffer i reservoir by adding 3ml from backup")
p1000.set_flow_rate(aspirate=500, dispense=400)
p1000.pick_up_tip()
p1000.aspirate(800, ETOH_backup.top(-12))
p1000.dispense(800, EtOH4.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH4.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-16))
p1000.dispense(800, EtOH4.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH4.top(-4))
p1000.blow_out()
p1000.aspirate(800, ETOH_backup.top(-20))
p1000.dispense(800, EtOH4.top(-4))
p1000.delay(seconds=2)
p1000.move_to(EtOH4.top(-4))
p1000.blow_out()
p1000.drop_tip()

### Transfer Wash 4 to RA7
m300.set_flow_rate(aspirate=50, dispense=50)
m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
m300.aspirate(Wash_2_vol, EtOH4.bottom())
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
m300.aspirate(Wash_2_vol, EtOH4.bottom())
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
m300.aspirate(Wash_2_vol, EtOH4.bottom())
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
m300.aspirate(Wash_2_vol, EtOH4.bottom())
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
m300.aspirate(Wash_2_vol, EtOH4.bottom())
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
m300.aspirate(Wash_2_vol, EtOH4.bottom())
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
    m300.dispense(Elution_vol, target.bottom(1))
    m300.mix(5, 30, target.bottom(3))
    m300.delay(seconds=5)
    m300.set_flow_rate(aspirate=100, dispense=100)
    m300.move_to(target.bottom(5))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.drop_tip()

robot.pause("Please cover the plate with film and incubate 5 min 25°C at 1500 rpm")
mag_deck.engage(height=34)
m300.delay(minutes=2)

### Transfer Elution buffer to elution_plate A1
m300.pick_up_tip(tipracks_200_4.wells('A1'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA1.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A1').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A1').top(-10))
m300.blow_out()
m300.drop_tip()

### Transfer Elution buffer to EA2
m300.pick_up_tip(tipracks_200_4.wells('A2'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA2.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A2').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A2').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA3
m300.pick_up_tip(tipracks_200_4.wells('A3'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA3.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A3').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A3').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA4
m300.pick_up_tip(tipracks_200_4.wells('A4'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA4.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A4').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A4').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA5
m300.pick_up_tip(tipracks_200_4.wells('A5'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA5.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A5').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A5').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA6
m300.pick_up_tip(tipracks_200_4.wells('A6'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA6.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A6').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A6').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA7
m300.pick_up_tip(tipracks_200_4.wells('A7'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA7.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A7').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A7').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA8
m300.pick_up_tip(tipracks_200_4.wells('A8'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA8.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A8').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A8').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA9
m300.pick_up_tip(tipracks_200_4.wells('A9'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA9.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A9').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A9').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA10
m300.pick_up_tip(tipracks_200_4.wells('A10'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA10.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A10').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A10').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA11
m300.pick_up_tip(tipracks_200_4.wells('A11'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA11.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A11').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A11').top(-10))
m300.blow_out()
m300.return_tip()

### Transfer Elution buffer to EA12
m300.pick_up_tip(tipracks_200_4.wells('A12'))
m300.set_flow_rate(aspirate=50, dispense=50)
m300.aspirate(Elution_buffer_vol, RA12.bottom())
m300.dispense(Elution_buffer_vol, elution_plate_RNA.wells('A12').bottom(2))
m300.delay(seconds=5)
m300.set_flow_rate(aspirate=130, dispense=130)
m300.move_to(elution_plate_RNA.wells('A12').top(-10))
m300.blow_out()
m300.return_tip()

mag_deck.disengage()
