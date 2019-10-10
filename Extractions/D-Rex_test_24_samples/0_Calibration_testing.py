## Description of procedure ##

# Should be run before running the actual protocol

# This protocol is to verify that the calibration of the robot is working correctly

# Use model labwares for this step

### Procedure ###


######## IMPORT LIBRARIES ########
from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'D-Rex Inital Extraction',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/03/28',
    'description': 'Automation of D-Rex RNA and DNA seperation for extraction protocol of stool samples in SHIELD',
}

### Custom LABWARE load
plate_name = '1ml_PCR'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7.5,                     # diameter (mm) of each well on the plate
        depth=26.4,                       # depth (mm) of each well on the plate
        volume=1000)

plate_name = '1ml_magPCR'                 # Model for calibration
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7.5,                     # diameter (mm) of each well on the plate
        depth=26.4,                       # depth (mm) of each well on the plate
        volume=1000)

#### LABWARE SETUP ####
trough = labware.load('trough-12row', '9')          # Model for calibration
RNA_plate = labware.load('1ml_PCR', '1')            # Model for calibration
mag_deck = modules.load('magdeck', '7')
sample_plate = labware.load('1ml_magPCR', '7', share=True)
backup = labware.load('opentrons-tuberack-50ml', '6')

tipracks_200 = [labware.load('tiprack-200ul', slot, share=True)
               for slot in ['3','4','5']]

tipracks_1000 = labware.load('tiprack-1000ul', '11', share=True)



#### PIPETTE SETUP ####
m300 = instruments.P300_Multi(
    mount='right',
    min_volume=25,
    max_volume=300,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)

p1000 = instruments.P1000_Single(
    mount='left',
    aspirate_flow_rate=500,
    dispense_flow_rate=500,
    tip_racks=tipracks_1000)

#### REAGENT SETUP
Binding_buffer1 = trough.wells('A1')
ETOH_backup = backup.wells('A1')

#### Plate SETUP
SA1 = sample_plate.wells('A1')
SA2 = sample_plate.wells('A2')
SA3 = sample_plate.wells('A3')
SA4 = sample_plate.wells('A4')
SA5 = sample_plate.wells('A5')
SA6 = sample_plate.wells('A6')
SA7 = sample_plate.wells('A7')
SA8 = sample_plate.wells('A8')
SA9 = sample_plate.wells('A9')
SA10 = sample_plate.wells('A10')
SA11 = sample_plate.wells('A11')
SA12 = sample_plate.wells('A12')

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
Binding_buffer_vol = Sample_vol*1

#### PROTOCOL ####


## Magdeck engagement height
mag_deck.disengage()
m300.delay(minutes=2)
mag_deck.engage(height=34)

#Magdeck PCR plate depth verification if using the adaptor
p1000.pick_up_tip(tipracks_1000.wells('A1'))
p1000.aspirate(300, ETOH_backup.top(-20))
p1000.dispense(300, Binding_buffer1.top(-12))
p1000.aspirate(300, ETOH_backup.top(-24))
p1000.delay(seconds=3)
p1000.dispense(300, Binding_buffer1.top(-12))
p1000.aspirate(300, ETOH_backup.top(-28))
p1000.delay(seconds=3)
p1000.dispense(300, Binding_buffer1.top(-12))
p1000.return_tip()


m300.pick_up_tip()
m300.aspirate(300, Binding_buffer1.top(-12))
m300.dispense(30, SA1.bottom(20))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(18))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(16))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(14))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(12))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(10))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(8))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(6))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(5))
m300.delay(seconds=3)
m300.blow_out()
m300.aspirate(300, Binding_buffer1.top(-12))
m300.dispense(30, SA1.bottom(4))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(2))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom(1))
m300.delay(seconds=3)
m300.dispense(30, SA1.bottom())
m300.delay(seconds=3)
m300.dispense(30, SA1.top())
m300.delay(seconds=3)
m300.dispense(30, SA1.top(-5))
m300.delay(seconds=3)
m300.dispense(30, SA1.top(-10))
m300.delay(seconds=3)
m300.dispense(30, SA1.top(-20))
m300.delay(seconds=3)
m300.dispense(30, SA1.top(-26))
m300.delay(seconds=3)
m300.return_tip()
