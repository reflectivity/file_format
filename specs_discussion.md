---
layout: page  
title: "ORSO - file formats - discussions on specifications"  
author: "Jochen Stahn"  
---


## Feedback and discussions on the .ort specs

In the following you find a rather unsorted collection of feedback and ideas about the `.ort` specs and the related `orsopy` package.

### anonymous 2022 workshop participant

#### naming confusion *angle_of_incidence* vs. *alpha_i* etc

For the optional columns of wavelength and angle of incidence, are lambda and alpha_i the expected/standardized names? 
Or should they be wavelength and incident_angle, as written in the header? 
Or is this discrepancy in the example required because column names must be different from values in the header? 

> (Jochen) See also below. This problem arises from the fact that we try to make it right in the header, and use the *conventional*
> terms in the column description. 
> 
> The keywords in the header are taken form the *physical quantity* name, e.g. *incidence_angel*, 
> while in the (optional) column description there are two possible (and recommended) entries: `name` and `physical_property`. 
> The `name` is used to create the 1-line header right above the data array and thus a well-established *symbol* is the right choice there.
> And `physical_property` is used to avoid all ambiguities.

If there is no current standard name (understanding that this is optional information), this should be made clear, with a statement/explanation of whether or not a standard name is expected in the future. 

> (Jochen) I agree that we should define a set of key words here and recommend their use. Suggestions can be found below.

A third important quantity for which there could be a standard name in the future is photon energy (for synchrotron x-ray experiments). 

> (Jochen) I agree.

#### wrong declaration in specs

The documentation states Value can be a list, but it cannot. (ComplexValue can be a list though). 
This discrepancy should be corrected either by modifying the documentation or the implementation, 
otherwise people could attempt to write files with data which cannot be handled by orsopy. 

> (Jochen) Wrong in specs. I'll correct this.

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
> 
> The format allows for redundant and even for contradicting information. It is in the responsibility of the 
> programmer to write out a physically consistend data file. 
> 
> On the other hand we should give some recommendations like the ones mentioned above. 
> 
> Personally I also prefer option 3, but without any further restrictions for the header. 
> 
> We discussed the pointer from header to column entries in an early stage and it was dropped at some point. 
> With a priorisation *column over header* this is clear to the software.
 
#### Future feature request:

Ability to have an error defined for a quantity in the header, either implemented similar to how quantities are allowed to have a range, or similar to how columns are allowed to be an error of another column”        

> Very good point. Artur will make a suggestion fr this.

### confusion of physical terms 

(Jochen)

We have a confusion of what we use as key words. Since the german terms are different I had probplems figuring out the correct English definitions...

#### official definitions

What can be measured or calculated is a **physical quantity**.

> E.g. the *incident angle*

This has a **dimension** = dim(*physical quantity*) relating it to a set of base quantities like *length*, *time*, *charge*, *temperature* etc. The *dimension* is no unit, nor can it be used to unambigiously describe a *physical quantity* (*plane angle* does not tell between *scattering angle*, *incident angle*, *total reflection angle*, ...). 

> dim( *incident angle* ) = *plane angle*

The *physical quantity* is often refered to by using a **symbol**.

> one possible symbol for *incident angle* is $\alpha_i$ (or *alpha_i* in the orso header)

The *physical quantity* is composed of a **numerical magnitude** times **unit**. Depending on the chosen *unit*, the *numerical magnitude* changes.

> $\alpha_i = 2.3 \cdot \mathrm{deg}$

#### what we do wrong or inconsistent

- In the columns section, we use *dimension* instead of *physical quantity*. This is certainly wrong and we will change it.
- The the column *name* we use the *symbol* (R, Qz, alpha_i, ...) rather than *physical quantity*. But in the header above we use the latter as key words. Thus if the analysis software searches for example for information about the *incident angle*, it has to look ar various places (this is intended) for different keys. A solution might be that the software searches for standardised `physical_property` entries in the column description which match the keys in the header. 
 
## reserve key words 

suggestions:

- *physical quantity* | *symbol* | *self-explanatory key*

- *incident angle* | `alpha_i` | `incident_angle`
- *final angle* | `alpha_f` | `final_angle`
- *scattering_angle* | **?** | `two_theta`
- *in-plane angle* | `phi_f` | `in_plane_angle`
- *photon energy* | **?** | `photon_energy`
- *counting time* | **?** | `counting_time`
- *attenuation factor* | **?** | `attenuation_factor`
- *scaling factor* | **?** | `scaling_factor`

- *offset* of a quantity with respect to the value reported in the raw file. 

## stitched data

- Where do we store e.g. the angles for stitched tof measurements? These are no longer used for processing, but may help future planning.
- x-ray data obtained with different attenuator settings.

> In case this information is not provided in one of the optional columns or in the individual headers of multiple data sets,
> it can not be used by the analysis software. Good choices for this information might be extra entried e.g. in the `incident_angle` section:
>
> ``` YAML
>         incident_angle:
>              min: 1.0
>              max: 5.8
>              used_angles: 1.0, 2.7, 5.8
>              unit: deg
> ```
> 
> Or as atributes to the measurement files in the `data_files` section:
>
> ``` YAML
>         data_files:
>            - file: ....
>              timestamp: ....
>              angle: 1.0
>            - file:
>              ...
> ```
> 
> The best choice depends on the type and operation mode of the instrument and thus should be made by the instrument responsible.


## guidelines for writing and reading

- hirarchy for looking up information (e.g. column beats header content)
- avoid contradicting information (e.g. single incident angle in the header for angle-disperse measurement)
- 
