from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': 'BEST_Purification',
    'author': 'Jacob Agerbo Rasmussen <genomicsisawesome@gmail.com>',
    'version': '1.0',
    'date': '2019/07/04',
    'description': 'Purification procedure of Automated single tube library preperation after Carøe et al. 2017',
}
#### LOADING CUSTOM LABWARE ####

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
trough = labware.load('trough-12row', '10')
Trash = labware.load('One-Column-reservoir','8')
mag_deck = modules.load('magdeck', '7')
mag_plate = labware.load('biorad-hardshell-96-PCR', '7', share=True)
elution_plate = labware.load('biorad-hardshell-96-PCR','1')


tipracks_200 = [labware.load('tiprack-200ul', slot, share=True)
                for slot in ['3','4','5','6']]


#### PIPETTE SETUP ####

m300 = instruments.P300_Multi(
    mount='right',
    min_volume=30,
    max_volume=200,
    aspirate_flow_rate=100,
    dispense_flow_rate=200,
    tip_racks=tipracks_200)


## Purification reagents SETUP
SPRI_beads = trough.wells('A1')
EtOH1 = trough.wells('A2')
EtOH2 = trough.wells('A3')
Elution_buffer = trough.wells('A12')

Liquid_trash = Trash.wells('A1')

## Sample Setup
sample_number = 96
col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
samples = [col for col in mag_plate.cols()[:col_num]]
samples_top = [well.top() for well in mag_plate.rows(0)[:col_num]]

SA1 = mag_plate.wells('A1')
SA2 = mag_plate.wells('A2')
SA3 = mag_plate.wells('A3')
SA4 = mag_plate.wells('A4')
SA5 = mag_plate.wells('A5')
SA6 = mag_plate.wells('A6')
SA7 = mag_plate.wells('A7')
SA8 = mag_plate.wells('A8')
SA9 = mag_plate.wells('A9')
SA10 = mag_plate.wells('A10')
SA11 = mag_plate.wells('A11')
SA12 = mag_plate.wells('A12')

sample_vol = 60
bead_vol = 1.5*sample_vol
EtOH_vol = 160
EtOH_vol2 = 150
elution_vol = 35

robot.comment("Yay! \ Purification begins!")

### Beads addition
mag_deck.engage(height=10)
m300.delay(seconds=10)
mag_deck.engage(height=12)
m300.delay(seconds=10)
mag_deck.engage(height=13)
m300.delay(seconds=10)
mag_deck.engage(height=14)
m300.delay(seconds=10)
mag_deck.engage(height=15)
m300.delay(seconds=10)
mag_deck.engage(height=16)
m300.delay(seconds=10)
mag_deck.engage(height=17)
m300.delay(seconds=10)
mag_deck.engage(height=18)
m300.delay(seconds=10)
mag_deck.disengage()


for target in samples:
    m300.set_flow_rate(aspirate=180, dispense=180)
    m300.pick_up_tip() # Slow down head speed 0.5X for bead handling
    max_speed_per_axis = {'x': (100), 'y': (100), 'z': (50), 'a': (20), 'b': (20), 'c': (20)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.set_flow_rate(aspirate=25, dispense=25)
    m300.aspirate(bead_vol, SPRI_beads)
    m300.move_to(target.bottom(1))
    m300.dispense(bead_vol,target.bottom(6))
    m300.set_flow_rate(aspirate=50, dispense=50)
    m300.delay(seconds=5)
    m300.move_to(target.top(-4))
    m300.blow_out()
    max_speed_per_axis = {'x': (600), 'y': (400), 'z': (100), 'a': (100), 'b': (40),'c': (40)}
    robot.head_speed(combined_speed=max(max_speed_per_axis.values()),**max_speed_per_axis)
    m300.drop_tip()
