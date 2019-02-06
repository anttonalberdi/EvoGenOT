####################################
# PCR MIX PROTOCOL FOR OPENTRONS 2 #
####################################

nsamples=96

#############
# Mastermix #
#############
#             1x        96x
# ddH20       13.50     1296
# 10x buffer  2.5       240
# MgCl2       2.5       240
# BSA         1.5       144
# dNTP        0.5       48
# TaqGold     0.5       48

h20=13.5
buffer=2.5
mgcl=2.5
bsa=1.5
dntp=0.5
taq=0.5

####################################
# To be added later (to each well) #
####################################
# Primer-F    1
# Primer-R    1
# DNA         2
####################

from opentrons import labware, instruments, modules, robot

# METADATA
metadata = {
    'protocolName': '16S_v3-v4.tagsteady.96',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'date': '2019/02/05',
    'description': 'PCR mix for 16S rRNA (v3-v4) metabarcoding of bacteria',
    'primers': 'Forward: 341F (CCTAYGGGRBGCASCAG), Reverse: R806 (GGACTACNNGGGTATCTAAT)',
}

# MODULES
temp_deck1 = modules.load('tempdeck', '9')
temp_plate1 = labware.load('opentrons-aluminum-block-2ml-eppendorf', '9', share=True)
    #Accessing Wells: single channel ['A1']-['D6']
    #Spin down all reagents before placing them in the temp deck
    #A1     H20         1500 ul 
    #A2     10x buffer  260 ul
    #A3     MgCl2       260 ul
    #A4     BSA         150 ul
    #A5     dNTP        50 ul
    #A6     Taq         50 ul
    #C1     Mastermix1  empty
    #C2     Mastermix2  empty
temp_deck2 = modules.load('tempdeck', '6')
temp_plate2 = labware.load('opentrons-aluminum-block-2ml-eppendorf', '9', share=True)
   
  
temp_plate1.set_temperature(4)
temp_deck.wait_for_temp()

# TIP RACKS (to be updated)
tipracks_300 = [labware.load('tiprack-200ul', slot, share=True) for slot in ['1','2','4','5','6	']]
tipracks_50 = [labware.load('tiprack-200ul', slot, share=True) for slot in ['1','2','4','5','6	']]

# PIPETTES
s300 = instruments.P300_Single(mount='left', tip_racks=tipracks_300)
m50 = instruments.P50_Multi(mount='right', tip_racks=tipracks_50)

############
# PROTOCOL #
############

#Calculate total volumes
h20_tot= h20 * nsamples
buffer_tot= buffer * nsamples
mgcl_tot= mgcl * nsamples
bsa_tot= bsa * nsamples
dntp_tot= dntp * nsamples
taq_tot= taq * nsamples

# 1) MASTERMIX PREPARATION #

#Transfer water
dispvol = h20_tot/2
s300.pick_up_tip(tipracks_300.wells('A1'))
if dispvol < 300:
    s300.transfer(dispvol, temp_plate1.wells('A1'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol, temp_plate1.wells('A1'), temp_plate1.wells('C2'))
elif dispvol < 600:
    s300.transfer(dispvol/2, temp_plate1.wells('A1'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/2, temp_plate1.wells('A1'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/2, temp_plate1.wells('A1'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/2, temp_plate1.wells('A1'), temp_plate1.wells('C2'))
elif dispvol < 900:
    s300.transfer(dispvol/3, temp_plate1.wells('A1'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/3, temp_plate1.wells('A1'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/3, temp_plate1.wells('A1'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/3, temp_plate1.wells('A1'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A1'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A1'), temp_plate1.wells('C2'))
s300.drop_tip(trash)

#Transfer 10x buffer
dispvol = buffer_tot/2
s300.pick_up_tip(tipracks_300.wells('A2'))
if dispvol < 300:
    s300.transfer(dispvol, temp_plate1.wells('A2'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol, temp_plate1.wells('A2'), temp_plate1.wells('C2'))
elif dispvol < 600:
    s300.transfer(dispvol/2, temp_plate1.wells('A2'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/2, temp_plate1.wells('A2'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/2, temp_plate1.wells('A2'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/2, temp_plate1.wells('A2'), temp_plate1.wells('C2'))
elif dispvol < 900:
    s300.transfer(dispvol/3, temp_plate1.wells('A2'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/3, temp_plate1.wells('A2'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/3, temp_plate1.wells('A2'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/3, temp_plate1.wells('A2'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A2'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A2'), temp_plate1.wells('C2'))
s300.drop_tip(trash)

#Transfer MgCl2
dispvol = mgcl_tot/2
s300.pick_up_tip(tipracks_300.wells('A3'))
if dispvol < 300:
    s300.transfer(dispvol, temp_plate1.wells('A3'), temp_plate1.wells('C1'), mix_before=(2, 50), mix_after=(3, 100))
    s300.transfer(dispvol, temp_plate1.wells('A3'), temp_plate1.wells('C2'), mix_after=(3, 100))
elif dispvol < 600:
    s300.transfer(dispvol/2, temp_plate1.wells('A3'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/2, temp_plate1.wells('A3'), temp_plate1.wells('C1'), mix_after=(3, 100))
    s300.transfer(dispvol/2, temp_plate1.wells('A3'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/2, temp_plate1.wells('A3'), temp_plate1.wells('C2'), mix_after=(3, 100))
elif dispvol < 900:
    s300.transfer(dispvol/3, temp_plate1.wells('A3'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/3, temp_plate1.wells('A3'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/3, temp_plate1.wells('A3'), temp_plate1.wells('C1'), mix_after=(3, 100))
    s300.transfer(dispvol/3, temp_plate1.wells('A3'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A3'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A3'), temp_plate1.wells('C2'), mix_after=(3, 100))
s300.drop_tip(trash)

#Transfer dNTPs
dispvol = bsa_tot/2
s300.pick_up_tip(tipracks_300.wells('A4'))
if dispvol < 300:
    s300.transfer(dispvol, temp_plate1.wells('A4'), temp_plate1.wells('C1'), mix_before=(2, 50), mix_after=(3, 100))
    s300.transfer(dispvol, temp_plate1.wells('A4'), temp_plate1.wells('C2'), mix_after=(3, 100))
elif dispvol < 600:
    s300.transfer(dispvol/2, temp_plate1.wells('A4'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/2, temp_plate1.wells('A4'), temp_plate1.wells('C1'), mix_after=(3, 100))
    s300.transfer(dispvol/2, temp_plate1.wells('A4'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/2, temp_plate1.wells('A4'), temp_plate1.wells('C2'), mix_after=(3, 100))
elif dispvol < 900:
    s300.transfer(dispvol/3, temp_plate1.wells('A4'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/3, temp_plate1.wells('A4'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/3, temp_plate1.wells('A4'), temp_plate1.wells('C1'), mix_after=(3, 100))
    s300.transfer(dispvol/3, temp_plate1.wells('A4'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A4'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A4'), temp_plate1.wells('C2'), mix_after=(3, 100))
s300.drop_tip(trash)

#Transfer BSA
dispvol = dntp_tot/2
s300.pick_up_tip(tipracks_300.wells('A4'))
s300.set_flow_rate(aspirate=50, dispense=50) # change aspiration and dispensation speed to better handle biscosity
if dispvol < 300:
    s300.transfer(dispvol, temp_plate1.wells('A5'), temp_plate1.wells('C1'), mix_before=(2, 50), mix_after=(3, 100))
    s300.transfer(dispvol, temp_plate1.wells('A5'), temp_plate1.wells('C2'), mix_after=(3, 100))
elif dispvol < 600:
    s300.transfer(dispvol/2, temp_plate1.wells('A5'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/2, temp_plate1.wells('A5'), temp_plate1.wells('C1'), mix_after=(3, 100))
    s300.transfer(dispvol/2, temp_plate1.wells('A5'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/2, temp_plate1.wells('A5'), temp_plate1.wells('C2'), mix_after=(3, 100))
elif dispvol < 900:
    s300.transfer(dispvol/3, temp_plate1.wells('A5'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/3, temp_plate1.wells('A5'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/3, temp_plate1.wells('A5'), temp_plate1.wells('C1'), mix_after=(3, 100))
    s300.transfer(dispvol/3, temp_plate1.wells('A5'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A5'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A5'), temp_plate1.wells('C2'), mix_after=(3, 100))
s300.drop_tip(trash)

#Transfer taq
dispvol = taq_tot/2
s300.pick_up_tip(tipracks_300.wells('A4'))
if dispvol < 300:
    s300.transfer(dispvol, temp_plate1.wells('A6'), temp_plate1.wells('C1'), mix_before=(2, 50), mix_after=(3, 100))
    s300.transfer(dispvol, temp_plate1.wells('A6'), temp_plate1.wells('C2'), mix_after=(3, 100))
elif dispvol < 600:
    s300.transfer(dispvol/2, temp_plate1.wells('A6'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/2, temp_plate1.wells('A6'), temp_plate1.wells('C1'), mix_after=(3, 100))
    s300.transfer(dispvol/2, temp_plate1.wells('A6'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/2, temp_plate1.wells('A6'), temp_plate1.wells('C2'), mix_after=(3, 100))
elif dispvol < 900:
    s300.transfer(dispvol/3, temp_plate1.wells('A6'), temp_plate1.wells('C1'), mix_before=(2, 50))
    s300.transfer(dispvol/3, temp_plate1.wells('A6'), temp_plate1.wells('C1'))
    s300.transfer(dispvol/3, temp_plate1.wells('A6'), temp_plate1.wells('C1'), mix_after=(3, 100))
    s300.transfer(dispvol/3, temp_plate1.wells('A6'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A6'), temp_plate1.wells('C2'))
    s300.transfer(dispvol/3, temp_plate1.wells('A6'), temp_plate1.wells('C2'), mix_after=(3, 100))
s300.drop_tip(trash)
s300.set_flow_rate(aspirate=None, dispense=None) #return to normal aspiration and dispensation speed

# 2) MASTERMIX DISPENSATION #
