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
# dNTP        0.5       48
# BSA         1.5       144
# TaqGold     0.5       48

h20=13.5
buffer=2.5
mgcl=2.5
dntp=0.5
bsa=1.5
taq=0.5

#############################
# To be added to each well) #
#############################
# Primer-F+R  2

primermix=2

################################
# To be added in the Green Lab #
################################
# DNA         2


####################

from opentrons import labware, instruments, modules, robot

#### METADATA ####

metadata = {
    'protocolName': '16S_v3-v4.tagsteady.96',
    'author': 'Antton Alberdi <anttonalberdi@gmail.com>',
    'version': '1.0',
    'date': '2019/02/05',
    'description': 'PCR mix for 16S rRNA (v3-v4) metabarcoding of bacteria',
    'primers': 'Forward: 341F (CCTAYGGGRBGCASCAG), Reverse: R806 (GGACTACNNGGGTATCTAAT)',
}

#### MODULES ####

#Deck 1 - Reagents and mastermixes
#temp_deck1 = modules.load('tempdeck', '9')
temp_plate1 = labware.load('opentrons-tuberack-2ml-eppendorf', '9', share=True)
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
#temp_deck1.set_temperature(4)
#temp_deck1.wait_for_temp()

#Deck 2 - PCR plate
#temp_deck2 = modules.load('tempdeck', '6')
temp_plate2 = labware.load('96-PCR-flat', '6', share=True)
    #Accessing Wells: single channel ['A1']-['H12'], 8-channel ['A1']-['A12']
#temp_deck2.set_temperature(4)
#temp_deck2.wait_for_temp()

#Deck 3 - Primer combinations (combined F and R primers)
#temp_deck3 = modules.load('tempdeck', '3')
temp_plate3 = labware.load('opentrons-aluminum-block-PCR-strips-200ul', '3', share=True)
    #Accessing Wells: single channel ['A1']-['H12'], 8-channel ['A1']-['A12']
    #A1     Tags 1-8
    #A2     Tags 9-16
    #A3     Tags 17-24
    #A4     Tags 25-32
#temp_deck3.set_temperature(4)
#temp_deck3.wait_for_temp()

#### TIP RACKS ####
tipracks_200 = labware.load('opentrons-tiprack-300ul', '11')
tipracks_10 = labware.load('tiprack-10ul', '8', share=True)

#### PIPETTES ####
s50 = instruments.P50_Single(mount='left', tip_racks=[tipracks_200])
m10 = instruments.P10_Multi(mount='right', tip_racks=[tipracks_10])

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

mmvol = (h20_tot+buffer_tot+mgcl_tot+bsa_tot+dntp_tot+taq_tot)/2 #mastermix volume per tube
samplevol= h20+buffer+mgcl+bsa+dntp+taq #mastermix volume per well (sample)

#### 1) MASTERMIX PREPARATION ####

#Transfer water (it goes too deep, move 3-4 mm upwards)
dispvol = h20_tot/2
s50.transfer(dispvol, temp_plate1.wells('A1'), temp_plate1.wells('C1','C2'), new_tip='never') #if larger volume it will automatically divide into smaller transfers. 

#Transfer 10x buffer
dispvol = buffer_tot/2
s50.transfer(dispvol, temp_plate1.wells('A2'), temp_plate1.wells('C1','C2'), new_tip='always')

#Transfer MgCl2
dispvol = mgcl_tot/2
s50.transfer(dispvol, temp_plate1.wells('A3'), temp_plate1.wells('C1','C2'), new_tip='always')

#Transfer dNTPs
dispvol = dntp_tot/2
s50.transfer(dispvol, temp_plate1.wells('A4'), temp_plate1.wells('C1','C2'), new_tip='always')

#Transfer BSA
dispvol = bsa_tot/2
s50.set_flow_rate(aspirate=5, dispense=15) # change aspiration and dispensation speed to better handle viscosity
s50.transfer(dispvol, temp_plate1.wells('A5'), temp_plate1.wells('C1','C2'), air_gap=10, new_tip='always')

#Transfer taq
dispvol = taq_tot/2
s50.transfer(dispvol, temp_plate1.wells('A6'), temp_plate1.wells('C1','C2'), air_gap=10, new_tip='always')
s50.set_flow_rate(aspirate=25, dispense=50) #return to normal aspiration and dispensation speed
#https://docs.opentrons.com/pipettes.html#p10-single

#### 2) MASTERMIX DISTRIBUTION ####

#Mix mastermixes
#s50.mix(4, 50, temp_plate1.wells('C1'))
#s50.mix(4, 50, temp_plate1.wells('C2'))

#Transfer Mastermix1 to first 48 wells A1-H6
s50.transfer(samplevol, temp_plate1.wells('C1'), temp_plate2.cols('1','2','3','4','5','6'))

#Transfer Mastermix2 to last 48 wells A7-H12
s50.transfer(samplevol, temp_plate1.wells('C2'), temp_plate2.cols('7','8','9','10','11','12'))
















#Fill PCR plate column 1
s300.aspirate(colvol, temp_plate1.wells('C1'))
s300.dispense(samplevol, temp_plate2.cols('1'))

#Fill PCR plate column 2
s300.aspirate(colvol, temp_plate1.wells('C1'))
s300.dispense(samplevol, temp_plate2.cols('2'))

#Fill PCR plate column 3
s300.aspirate(colvol, temp_plate1.wells('C1'))
s300.dispense(samplevol, temp_plate2.cols('3'))

#Fill PCR plate column 4
s300.aspirate(colvol, temp_plate1.wells('C1'))
s300.dispense(samplevol, temp_plate2.cols('4'))

#Fill PCR plate column 5
s300.aspirate(colvol, temp_plate1.wells('C1'))
s300.dispense(samplevol, temp_plate2.cols('5'))

#Fill PCR plate column 6
s300.aspirate(colvol, temp_plate1.wells('C1'))
s300.dispense(samplevol, temp_plate2.cols('6'))

s300.drop_tip(trash)
s300.pick_up_tip(tipracks_300.wells('A8'))

#Fill PCR plate column 7
s300.aspirate(colvol, temp_plate1.wells('C2'))
s300.dispense(samplevol, temp_plate2.cols('7'))

#Fill PCR plate column 8
s300.aspirate(colvol, temp_plate1.wells('C2'))
s300.dispense(samplevol, temp_plate2.cols('8'))

#Fill PCR plate column 9
s300.aspirate(colvol, temp_plate1.wells('C2'))
s300.dispense(samplevol, temp_plate2.cols('9'))

#Fill PCR plate column 10
s300.aspirate(colvol, temp_plate1.wells('C2'))
s300.dispense(samplevol, temp_plate2.cols('10'))

#Fill PCR plate column 11
s300.aspirate(colvol, temp_plate1.wells('C2'))
s300.dispense(samplevol, temp_plate2.cols('11'))

#Fill PCR plate column 12
s300.aspirate(colvol, temp_plate1.wells('C2'))
s300.dispense(samplevol, temp_plate2.cols('12'))

#### 3) PRIMER DISTRIBUTION ####

#Tags1-8 to columns 1, 4, 7, 10
m10.pick_up_tip(tipracks_10.wells('A1'))
m10.transfer(primermix, temp_plate3.wells('A1'), temp_plate2.wells('A1'))
s300.drop_tip(trash)

m10.pick_up_tip(tipracks_10.col('2'))
m10.transfer(primermix, temp_plate3.wells('A1'), temp_plate2.wells('A4'))
s300.drop_tip(trash)

m10.pick_up_tip(tipracks_10.col('3'))
m10.transfer(primermix, temp_plate3.wells('A1'), temp_plate2.wells('A7'))
s300.drop_tip(trash)

m10.pick_up_tip(tipracks_10.col('4'))
m10.transfer(primermix, temp_plate3.wells('A1'), temp_plate2.wells('A10'))
s300.drop_tip(trash)

#Tags9-16 to columns 2, 5, 8, 11
m10.pick_up_tip(tipracks_10.wells('A5'))
m10.transfer(primermix, temp_plate3.wells('A2'), temp_plate2.wells('A2'))
s300.drop_tip(trash)

m10.pick_up_tip(tipracks_10.wells('A6'))
m10.transfer(primermix, temp_plate3.wells('A2'), temp_plate2.wells('A5'))
s300.drop_tip(trash)

m10.pick_up_tip(tipracks_10.wells('A7'))
m10.transfer(primermix, temp_plate3.wells('A2'), temp_plate2.wells('A8'))
s300.drop_tip(trash)

m10.pick_up_tip(tipracks_10.wells('A8'))
m10.transfer(primermix, temp_plate3.wells('A2'), temp_plate2.wells('A11'))
s300.drop_tip(trash)

#Tags17-24 to columns 3, 6, 9, 12
m10.pick_up_tip(tipracks_10.wells('A9'))
m10.transfer(primermix, temp_plate3.wells('A3'), temp_plate2.wells('A3'))
s300.drop_tip(trash)

m10.pick_up_tip(tipracks_10.wells('A10'))
m10.transfer(primermix, temp_plate3.wells('A3'), temp_plate2.wells('A6'))
s300.drop_tip(trash)

m10.pick_up_tip(tipracks_10.wells('A11'))
m10.transfer(primermix, temp_plate3.wells('A3'), temp_plate2.wells('A9'))
s300.drop_tip(trash)

m10.pick_up_tip(tipracks_10.wells('A12'))
m10.transfer(primermix, temp_plate3.wells('A3'), temp_plate2.wells('A12'))
s300.drop_tip(trash)
