##################
# Custom labware #
##################

#Template for all custom labware definitions
    #See https://docs.opentrons.com/labware.html

#plate_name = '3x6_plate'
#if plate_name not in labware.list():
#    custom_plate = labware.create(
#        plate_name,                    # name of you labware
#        grid=(3, 6),                    # specify amount of (columns, rows)
#        spacing=(12, 12),               # distances (mm) between each (column, row)
#        diameter=5,                     # diameter (mm) of each well on the plate
#        depth=10,                       # depth (mm) of each well on the plate
#        volume=200)

#########################
# 96 Well chilling rack #
#########################
# Description: blue/purple eppendorf ice-racks available in the modern lab freezers
# Created by Jacob Agerbo (2019/02/25)
# Modified by Antton Alberdi (2019/02/26) - plate_name changed from '96_Chill_rack' to 'chill_rack_96' to keep consistency with Opentrons presets

plate_name = 'chill_rack_96'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(12, 12),               # distances (mm) between each (column, row)
        diameter=6.4,                     # diameter (mm) of each well on the plate
        depth=38,                       # depth (mm) of each well on the plate
        volume=200)

##########################
# 24 x 2ml chilling rack #
##########################
# Description: white ice-racks available in the modern lab freezers
# Created by Jacob Agerbo (2019/02/25)
# Modified by Antton Alberdi (2019/02/26) - plate_name changed from '2ml_Chill_rack' to 'chill_rack_2ml' to keep consistency with Opentrons presets

plate_name = 'chill_rack_2ml'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(6, 4),                    # specify amount of (columns, rows)
        spacing=(18, 18),               # distances (mm) between each (column, row)
        diameter=10,                     # diameter (mm) of each well on the plate
        depth=74,                       # depth (mm) of each well on the plate
        volume=2000)

##########################
# labsolute 10µl TipRack #
##########################
# Description: modern lab common stock long 10ul pipette tips (red box) with adaptor
# Created by Jacob Agerbo (2019/02/25)
# Modified by Antton Alberdi (2019/02/26) - Changed name from 'tiprack-Labsolute_10µl' to 'labsolute-tiprack-10µl' to keep consistency with Opentrons presets

plate_name = 'labsolute-tiprack-10µl'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=4.5,                     # diameter (mm) of each well on the plate
        depth=52,                       # depth (mm) of each well on the plate
        volume=10)

###########################
# labsolute 200µl TipRack #
###########################
# Description: modern lab common stock long 10ul pipette tips (red box) with adaptor
# Created by Jacob Agerbo (2019/02/25)
# Modified by Antton Alberdi (2019/02/26) - Changed name from 'tiprack-Labsolute_200µl' to 'labsolute-tiprack-200µl' to keep consistency with Opentrons presets

plate_name = 'labsolute-tiprack-200µl'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=7,                     # diameter (mm) of each well on the plate
        depth=54,                       # depth (mm) of each well on the plate
        volume=200)

############################
# labsolute 1000µl TipRack #
############################
# Description: modern lab common stock long 10ul pipette tips (red box) with adaptor
# Created by Jacob Agerbo (2019/02/25)
# Modified by Antton Alberdi (2019/02/26) - Changed name from 'tiprack-Labsolute_1000µl' to 'labsolute-tiprack-1000µl' to keep consistency with Opentrons presets
# Modified by Antton Alberdi (2019/02/26) - Changed volume from 2000 to 1000

plate_name = 'labsolute-tiprack-1000µl'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(12, 8),                    # specify amount of (columns, rows)
        spacing=(9, 9),               # distances (mm) between each (column, row)
        diameter=8,                     # diameter (mm) of each well on the plate
        depth=76,                       # depth (mm) of each well on the plate
        volume=1000)
