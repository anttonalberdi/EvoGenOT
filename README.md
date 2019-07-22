# EvoGenOT
UCPH's EvoGenomics section's Opentrons protocol library.

## OT2 usage basics

* Do NOT use the OT2 if you do not have the necessary training and have received the approval from Sarah Mak.
* Always use the OT2 [LogBook](https://goo.gl/forms/fcw7m5c86HYXqvbx1) to record usage.
* Use the Google Calendar to book OT2 robots. Ask Sarah Mak for details.
* Do NOT switch off the OT-2 unless there is a connection error (the power button is on the side).
* Do NOT press the button with BLUE light. It is just a light indicating whether the OT-2 is ready or not.

## OT2 protocols

At EvoGenomics we have our own library of OT2 protocols developed and validated by internal users. All protocols are expected to contain:

* A python script with a descriptive name and version number specified (e.g. 2ml_to_96plate_v1.py).
* Procedures requiring multiple protocol setups are required to have a prefix number in name for indication of procedure stage.
* A readme file explaining the procedures to run the protocol (e.g. 2ml_to_96plate_v1.md)
* Some protocols (aliquoting, PCR mixes, etc.) might require csv files with basic information about sample positions, volumes, etc.


## Opentrons API documentation

https://docs.opentrons.com/

## Protocol development steps

1. Write the python code
2. Validate the code in the Opentrons software
3. Test the protocol without plasticware (only pipettes)
4. Test the protocol with plasticware and dummy reagents
5. Test the protocol with actual reagents

## Common nomenclature

### Modules
* temp_deck (if multiple modules [1-n])
* temp_plate  (if multiple modules [1-n])
* mag_deck  (if multiple modules [1-n])
* mag_plate (if multiple modules [1-n])

### Pipettes
Code | Description
------------ | -------------
s10 | 1-10 ul single channel pipette
s50 | 5-50 ul single channel pipette
s300 | 30-300 ul single channel pipette
s1000 | 100-1000 ul single channel pipette
m10 | 1-10 ul multichannel pipette
m50 | 5-50 ul multichannel pipette
m300 | 30-300 ul multichannel pipette

### Robot spatial arrangement
![image](https://github.com/anttonalberdi/EvoGenOT/blob/master/images/DeckMapEmpty.png)
