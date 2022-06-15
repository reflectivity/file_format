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

> (Jochen) See also below. This problem arises from the fact that we try to make it right in the header, and use the *conventional*
> terms in the column description.

If there is no current standard name (understanding that this is optional information), this should be made clear, with a statement/explanation of whether or not a standard name is expected in the future. 
A third important quantity for which there could be a standard name in the future is photon energy (for synchrotron x-ray experiments). 

> (Jochen) I agree that we should define a set of key words here and recommend their use.


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

> (Jochen) Here we have to diferentiate between the data format rules and recommendations for software using this format. 
> The format allows for redundant and even for contradicting information. It is in the responsibility of the 
> programmer to write out a physically consistend data file. 
> On the other hand we should give some recommendations like the ones mentioned above. 
> Personally I also prefer option 3, but without any further restrictions for the header. 
> We discussed the pointer from header to column entries in an early stage and it was dropped at some point. Does anyone remember the
> reason? 
 
#### Future feature request:

Ability to have an error defined for a quantity in the header, either implemented similar to how quantities are allowed to have a range, or similar to how columns are allowed to be an error of another column”                                                                              

### confusion of physical terms 

(Jochen)

We have a confusion of what we use as key words. Since the german terms are different I had probplems figuring out the correct English definitions...

#### official definitions

What can be measured or calculated is a **physical quantity**.

> E.g. the *incident angle*

This has a **dimension** = dim(*physical quantity*) relating it to a set of base quantities like *lenth*, *time*, *charge*, *temperature* etc. The *dimension* is no unit, nor can it be used to unambigiously describe a *physical quantity* (*plane angle* does not tell between *scattering angle*, *incident angle*, *total reflection angle*, ...). 

> dim( *incident angle* ) = *plane angle*

The *physical quantity* is often refered to by using a **symbol**.

> one possible symbol for *incident angle* is $\alpha_i$ (or *alpha_i* in the orso header)

The *physical quantity* is composed of a **numerical magnitude** times **unit**. Depending on the chosen *unit*, the *numerical magnitude* changes.

> $\alpha_i = 2.3 \cdot \mathrm{deg}$

#### what we do wrong or inconsistent

- In the columns section, we use *dimension* instead of *physical quantity*. This is certainly wrong and we should change it.
- The *numerical magnitude* is just called *magnitude*. This might be fine.
- For the *error_of* we specify the meaning of *magnitude unit* using the term *value_is*. Consistent would be *physival quantity*. Here *value_is* is easier to read and might stay.
- The the column *name* we use the *symbol* (R, Qz, alpha_i, ...) rather than *physical quantity*. But in the header above we use the latter as key words. Thus if the analysis software searches for example for information about the *incident angle*, it has to look ar various places (this is intended) for different keys. 
 
