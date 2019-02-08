# EvoGenOT
UCPH's EvoGenomics section's Opentrons protocol library.

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
