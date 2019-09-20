from opentrons import labware, instruments, modules

### USER INPUT ###

OT2user = 'Mandy' # First name of user
OT2useremail = 'mandy.boltbotnen@gmail.com' # email of user

USERsample_number = 16 # number of samples. Minimum 8, maximum 96
USERsample_vol = 100 # volume of sample in ul
USERbead_ratio = 1.4 # ratio of SPRI bead to sample
USERelution_vol = 35 # volume of final elution, in ul

USERincubation_time = 1 # Incubation time after adding SPRI beads, in minutes
USERsettling_time = 1 # Time for beads to seperate, in minutes
USERdrying_time = 1 # Time for beads to dry, in minutes

############################################
### DO NOT ALTER CODING BELOW THIS POINT ###
############################################

ProtocolName = 'DNA Bead Purification'

metadata = {
    'protocolName': 'DNA Bead Purification',
    'author': 'Mandy <mandy.boltbotnen@gmail.com>',
    'version': '1.7',
    'date': '2019/09/12',
    'description': 'DNA purification of FTA eluted extracts',
	'latestUpdate': 'Adding feature for <48 samples, to spread out in the sample plates',
}

# CUSTOM LABWEAR #

plate_name = 'One-Column-reservoir'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(1, 1),                    # specify amount of (columns, rows)
        spacing=(0, 0),               # distances (mm) between each (column, row)
        diameter=81,                     # diameter (mm) of each well on the plate
        depth=35,                       # depth (mm) of each well on the plate
        volume=350000)

plate_name = '1ml_PCR' #Used on the magdeck together with adaptor
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7.5,                     # diameter (mm) of each well on the plate
        depth=26.4,                       # depth (mm) of each well on the plate
        volume=1000)

mag_deck = modules.load('magdeck', '7')
mag_plate = labware.load('1ml_PCR', '7', share=True)
output_plate = labware.load('biorad-hardshell-96-PCR', '10')


def run_custom_protocol(
        pipette_type: 'StringSelection...'='p300_Multi',
        pipette_mount: 'StringSelection...'='left',
        sample_number: int=24,
        sample_volume: float=20,
        bead_ratio: float=1.8,
        elution_buffer_volume: float=200,
        incubation_time: float=1,
        settling_time: float=1,
        drying_time: float=5):

    total_tips = sample_number*8
    tiprack_num = total_tips//96 + (1 if total_tips % 96 > 0 else 0)
    slots = ['1', '2', '3', '4', '5', '6', '9'][:tiprack_num]
    if pipette_type == 'p1000_Single':
        tipracks = [labware.load('tiprack-1000ul', slot) for slot in slots]
        pipette = instruments.P1000_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p300_Single':
        tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
        pipette = instruments.P300_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p50_Single':
        tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
        pipette = instruments.P50_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p10_Single':
        tipracks = [labware.load('tiprack-10ul', slot) for slot in slots]
        pipette = instruments.P10_Single(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p10_Multi':
        tipracks = [labware.load('tiprack-10ul', slot) for slot in slots]
        pipette = instruments.P10_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p50_Multi':
        tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
        pipette = instruments.P50_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)
    elif pipette_type == 'p300_Multi':
        tipracks = [labware.load('tiprack-200ul', slot) for slot in slots]
        pipette = instruments.P300_Multi(
            mount=pipette_mount,
            tip_racks=tipracks)

    mode = pipette_type.split('_')[1]

    if mode == 'Single':
        if sample_number <= 5:
            reagent_container = labware.load('tube-rack-2ml', '11')
            liquid_waste = labware.load('One-Column-reservoir', '9')
        else:
            reagent_container = labware.load('trough-12row', '11')
            liquid_waste = labware.load('One-Column-reservoir', '9')
        samples = [well for well in mag_plate.wells()[:sample_number]]
        output = [well for well in output_plate.wells()[:sample_number]]
    else:
            reagent_container = labware.load('trough-12row', '11')
            liquid_waste = labware.load('One-Column-reservoir', '9')
        if sample_number <= 48:
            col_num = (sample_number // 8 + (1 if sample_number % 8 > 0 else 0))*2
            samples = [col for col in mag_plate.cols()[:col_num] if sample_number % 2 == 1]
            output = [col for col in output_plate.cols()[:col_num] if sample_number % 2 == 1]
        else:
            col_num = sample_number // 8 + (1 if sample_number % 8 > 0 else 0)
            samples = [col for col in mag_plate.cols()[:col_num]]
            output = [col for col in output_plate.cols()[:col_num]]

    # Define reagents and liquid waste
    beads = reagent_container.wells(1)
    ethanol = reagent_container.wells(3)
    elution_buffer = reagent_container.wells(12)

    # Define bead and mix volume
    bead_volume = sample_volume*bead_ratio
    if bead_volume/2 > pipette.max_volume:
        mix_vol = pipette.max_volume
    else:
        mix_vol = bead_volume/2
    total_vol = bead_volume + sample_volume + 5

    # Mix beads and PCR samples
    for target in samples:
        pipette.pick_up_tip()
        pipette.mix(5, mix_vol, beads)
        pipette.transfer(bead_volume, beads, target, new_tip='never')
        pipette.mix(10, mix_vol, target)
        pipette.blow_out()
        pipette.drop_tip()

    # Incubate beads and PCR product at RT for 5 minutes
    pipette.delay(minutes=incubation_time)

    # Engagae MagDeck and incubate
    mag_deck.engage()
    pipette.delay(minutes=settling_time)

    # Remove supernatant from magnetic beads
    pipette.set_flow_rate(aspirate=25, dispense=150)
    for target in samples:
        pipette.transfer(total_vol, target, liquid_waste, blow_out=True)

    # Wash beads twice with 70% ethanol
    air_vol = pipette.max_volume * 0.1
    for cycle in range(2):
        for target in samples:
            pipette.transfer(200, ethanol, target, air_gap=air_vol,
                             new_tip='once')
        pipette.delay(minutes=1)
        for target in samples:
            pipette.transfer(200, target, liquid_waste, air_gap=air_vol)

    # Dry at RT
    pipette.delay(minutes=drying_time)

    # Disengage MagDeck
    mag_deck.disengage()

    # Mix beads with elution buffer
    if elution_buffer_volume/2 > pipette.max_volume:
        mix_vol = pipette.max_volume
    else:
        mix_vol = elution_buffer_volume/2
    for target in samples:
        pipette.pick_up_tip()
        pipette.transfer(
            elution_buffer_volume, elution_buffer, target, new_tip='never')
        pipette.mix(20, mix_vol, target)
        pipette.drop_tip()

    # Incubate at RT for 3 minutes
    pipette.delay(minutes=5)

    # Engagae MagDeck for 1 minute and remain engaged for DNA elution
    mag_deck.engage()
    pipette.delay(minutes=settling_time)

    # Transfer clean PCR product to a new well
    for target, dest in zip(samples, output):
        pipette.transfer(elution_buffer_volume, target, dest, blow_out=True)


run_custom_protocol(**{'pipette_type': 'p300_Multi', 'pipette_mount': 'right', 'sample_number': USERsample_number, 'sample_volume': USERsample_vol, 'bead_ratio': USERbead_ratio, 'elution_buffer_volume': USERelution_vol, 'incubation_time': USERincubation_time, 'settling_time': USERsettling_time, 'drying_time': USERdrying_time})

### Send email to OT2user at end of protocol
import smtplib

gmail_user = 'ot2.evogen@gmail.com'
gmail_password = 'nomoreacdc'
to = [OT2useremail]
sent_from = gmail_user
subject = ProtocolName + ' completed'
body = 'Dear ' + OT2user + ', \n\nThe OpenTron2 has completed the ' + ProtocolName + ' protocol. Please remove your samples and clean the robot.\nThank you for using the OpenTron2!\n\nComputationally yours,\nOpenTron2'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print ('Email sent!')
except:
    print ('Something went wrong...')
