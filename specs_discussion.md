---
layout: page  
title: "ORSO - file formats - discussions on specifications"  
author: "Jochen Stahn"  
---


## Feedback and discussions on the .ort specs

### anonymous 2022 workshop participant

#### naming confusion *angle_of_incidence* vs. *alpha_i* etc

For the optional columns of wavelength and angle of incidence, are lambda and alpha_i the expected/standardized names? 
Or should they be wavelength and incident_angle, as written in the header? 
Or is this discrepancy in the example required because column names must be different from values in the header? 
If there is no current standard name (understanding that this is optional information), this should be made clear, with a statement/explanation of whether or not a standard name is expected in the future. 
A third important quantity for which there could be a standard name in the future is photon energy (for synchrotron x-ray experiments). I have no opinion on what such names should or should not be

#### wrong declaration in specs

The documentation states Value can be a list, but it cannot. (ComplexValue can be a list though). 
This discrepancy should be corrected either by modifying the documentation or the implementation, 
otherwise people could attempt to write files with data which cannot be handled by orsopy. 

#### redundant information and priorisation

Specs are not clear about what should happen if there is a header entry and a column with the same name: 

1. is this invalid (see first point) 
2. do they have to be consistent or 
3. does the column overwrite any header information? 

E.g., if a column is supplied, would it be required that, if that is also in the header, 

- it is a range with matching min/max? 
- That it is a value with matching average? 
- Must it be left out of the header entirely? 
- Should it be overwritten if a column is found, 
- or should there be a pointer to a column, for example an optional keyword ‘column’, where the value or range could then be used by software which cannot support point-by-point calculation (the column data)? 

My vote is for 3 implemented in this last way, for the purpose that the header can still contain some human-readable information useful for experimental reproducibility even if the contents are overwritten by a column. 
 
#### Future feature request:

Ability to have an error defined for a quantity in the header, either implemented similar to how quantities are allowed to have a range, or similar to how columns are allowed to be an error of another column”
~                                                                               
