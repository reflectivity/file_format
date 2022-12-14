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
> The keywords in the header are taken form the *physical quantity* name, e.g. *incidence_angle*, 
> while in the (optional) column description there are two possible (and recommended) entries: `name` and `physical_quantity`. 
> The `name` is used to create the 1-line header right above the data array and thus a well-established *symbol* is the right choice there.
> And `physical_quantity` is used to avoid all ambiguities.

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
>
> ``` YAML
> #    measurement: 
> #         instrument_settings:  
> #             incident_angle:  
> #                 min:   <value>
> #                 max:   <value>
> #                 details_at_column: alpha_i
> #                 unit:  deg    
> ```

**item 1**: What is the ORSO recommendation for using redundand information? 
 
#### Future feature request:

Ability to have an error defined for a quantity in the header, either implemented similar to how quantities are allowed to have a range, or similar to how columns are allowed to be an error of another column”        

> (Jochen) Very good point. What about:
>
> ``` YAML
> #    measurement: 
> #         instrument_settings:  
> #             incident_angle:  
> #                 magnitude:        2.1
> #                 unit:             deg    
> #                 error:
> #                     magnitude:    0.01
> #                     error_type:   resolution
> #                     distribution: gaussian
> #                     value_is:     sigma
> ```
> 
> or the short notation
> 
> ``` YAML
> #    measurement: 
> #         instrument_settings:  
> #             incident_angle:  
> #                 magnitude:  2.1
> #                 unit:       deg    
> #                 error:      0.01
> ```

**item 2**: How are uncertainties of quantities in the header supplied?

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
- For the column *name* we use the *symbol* (R, Qz, alpha_i, ...) rather than the *physical quantity*. But in the header above we use the latter as key words. Thus if the analysis software searches for example for information about the *incident angle*, it has to look ar various places (this is intended) for different keys. A solution might be that the software searches for standardised `physical_property` entries in the column description which match the keys in the header. 

**item 3**: Do we agree to change the key `dimension` to `physical_quantity`?
 
## reserve key words 

suggestions for physical quantities:

| *physical quantity* | *symbol* | *self-explanatory key* |
|:---|:---|:---|
| *incident angle* | `alpha_i` | `incident_angle` |
| *final angle* | `alpha_f` | `final_angle` |
| *scattering angle* | `two_theta` | `scattering_angle` |
| *in-plane angle* | `phi_f` | `in_plane_angle` |
| | | |
| *photon energy* | `E` ? | `photon_energy`|
| *wavelength* | `lambda` | `wavelength` |
| | | |
| *absolute counts* | `cnts` ? | `counts`, `events` |
| *attenuation factor* | ? | `attenuation_factor` |
| *scaling factor* | `s` ? | `scaling_factor` |
| *counting time* | `t`, `tme` ? | `counting_time` |
| | | |
| *beam divergence* | `Delta_theta` | `beam_divergence` |
| | | |
| *intensity* | `I` | `intensity` |


other suggestions:

- `xxx.offset` of a quantity with respect to the value reported in the raw file. 
- `scan_type` steps or continous
 
**item 4**: Do we *reserve* key words for future use? 
 
**item 5**: How are key words reserved? Are there any warnings?
 
**item 6**: Which key words should we reserve?

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
>              individual_values: 1.0, 2.7, 5.8
>              unit: deg
> ```
> 
> Or as atributes to the measurement files in the `data_files` section
> (`details` is orso-undefined and thus treated as a string):
> 
> ``` YAML
>         data_files:
>            - file: ....
>              timestamp: ....
>              details: 1.0 deg, 42 min
>            - file:
>              ...
> ```

> The best choice depends on the type and operation mode of the instrument and thus should be made by the instrument responsible.
 
**item 7**: Do we introduce `individual_values` or `details` as special versions of `comment`? 


## guidelines for writing and reading

- hirarchy for looking up information (e.g. column beats header content)
- avoid contradicting information (e.g. single incident angle in the header for angle-disperse measurement)
- 

## open issues for lab x-ray reflectometers
 
**item 8**: Which of the keys discussed below should be included in the specs to (better) incorporate lab x-ray data files?

When attempting to convert the ASCII output files of various commercial lab x-ray reflectometers (diffractometers) 
it became obvious that the present dictionary misses several entries.
 
- It is not exactely clear where to put the *brand*, *model* and probably *configuration* information.

  ``` YAML
     experiment:
         title: ...
         instrument:
             type: x-ray lab source        (neutron reflectometer, synchrotron diffractometer, ....)
             brand: Brucker
             model: Discovery
             hardware_indicator: 65519
  ```
 
- The wavelength is often defiend via the anode material, the line(s) and probably the presence of a monochromator.
- The scan modes might be `steps` or `continous`.
- The slit sizes are reported to enable resolution calculation.
- Often a long list of hardware settings is supplied, e.g. tube current, temperature, configuration, etc. 
  These things do not really belong to a *reduced data* file, but we shoul at least recommend a place for
  these entries. In the example below I put it as a multy-line string in `instrument_settings.details`.
 
``` YAML 
     measurement: 
         instrument_settings:  
             incident_angle:           
                 min:          0.1
                 max:          6.0
                 unit:         deg
             wavelength:               
                 magnitude:    1.54184
                 unit:         angstrom
                 anode:        Cu 
                 lines:
                    - name:    K_alpha1
                      magnitude:  1.5405980
                      weight:  2/3
                    - name:    K_alpha2
                      magnitude:  1.5444260
                      weight:  1/3
             scan_type:        continuous
             details: |
                 "Configuration=Reflection-Transmission Spinner 3.0, Owner=user, Creation date=3/5/2021 8:12:09 AM"
                 "Goniometer=Theta/Theta; Minimum step size 2Theta:0.0001; Minimum step size Omega:0.0001"
                 "Sample stage=Reflection-transmission spinner 3.0; Minimum step size Phi:0.1"
```
 
- Most present day files report the *incident angle*, the *counting time* and probably the *attenuation factor* 
  as columns. We should define standard keys for the corresponding column descriptions.
 
  ``` YAML
      - name: alpha_i
        unit: deg
        physical_quantity: incident_angle
      - name: alpha_f
        unit: deg
        physical_quantity: final_angle
      - name: two_theta
        unit: deg
        physical_quantity: scattering_angle
      - name: tme ?
        unit: s
        physical_quantity: counting_time
      - name: abs ?
        physical_quantity: absorber_factor
  ```
 
- The `.ort` specs clearly separate data origin and data reduction. For lab reflectometers it often the same software for 
  instrument control and reduction.
- Information about the facility, the owner and the sample is often missing.
