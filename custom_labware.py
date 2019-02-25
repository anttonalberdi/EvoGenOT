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
plate_name = '96_Chill_rack'
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
plate_name = '2ml_chill_rack'
if plate_name not in labware.list():
    custom_plate = labware.create(
        plate_name,                    # name of you labware
        grid=(6, 4),                    # specify amount of (columns, rows)
        spacing=(18, 18),               # distances (mm) between each (column, row)
        diameter=10,                     # diameter (mm) of each well on the plate
        depth=74,                       # depth (mm) of each well on the plate
        volume=2000)

#########################
