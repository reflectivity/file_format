---
layout: page  
title: "ORSO - file formats - specifications for the text reflectivity file"  
author: "Jochen Stahn"  
---

This document contains the specifications and some examples for the text representation of the ORSO reflectivity file. 
It is the basis for the development of python modules to read and write these files.

The main contributors are: 
Andrew McCluskey,
Andrew Nelson,
Artur Glavic,
Brian Maranville,
Maximilian Skoda
and
Jochen Stahn.

Comments and contributions are welcome and should be 
communicated to <Jochen.Stahn@psi.ch>.

last modified: 2021-09-25

---

## general specifications

### file extension

It is recommended to use the suffix `.ort` (**o**rso **r**eflectivity **t**extfile) for reflectivity files following this standard.

### placeholders

If there is no entry available for a keyword, the default value for both, string and numbers is the string `null` 

### language

In line with canSAS and NeXus, we use American English for the keywords. 
E.g. `polarization` rather than `polarisation`. 

### encoding

The text representation allows for UNICODE characters. 
For the keywords only ASCII Basic Latin encoding is allowed. 

### date and time format

For time stamps we use the ISO8601 format for **date and time**: 'yyyy-mm-ddThh:mm:ss'.
This is local time.
Do not use UTC (hence no suffix Z).
If the time zone shall be specified (e.g. for disambiguation of summer/winter time),
then append the UTC time offset in the form "+09:30", i.e. 'yyyy-mm-ddThh:mm:ss+09:30'.

If just the date is of interest, only the **date** part of the same standard is used: 'yyyy-mm-dd'.


### units

In the header, physical quantities shall always be stored with magnitude and unit in the form

```
<quantity>:
     magnitude: <magnitude>
     unit: <unit>
```

Rules for using units:

- only ASCII symbols are to be used;
  - the greek letter μ is written as `mu` (e.g. `mum` for micrometer);
  - `angstrom` cannot be abbreviated (`Å` is not allowed, `A` stands for Ampere);
- composition with `*` and `/`, exponentiation with `**`
  - reciprocal units are written e.g. as `1/nm` for wavenumbers, `1/angstrom**2` for the scattering length density

Recommended units include:
- for angles, `rad`, `deg`;
- for lengths, `m`, `mm`, `nm`, `angstrom`;
- for durations, `s`;
- for energies, `eV`, `keV`;
- for temperatures, `K`.


### comments

There are 2 kinds of comments possible:

The key word `comment:` allows to add free text, e.g. to describe a related entry
in more detail. E.g.

    comment: |
        Attention! These data have been collected without the frame overlap mirror
        and contain thus some highly structured background.

        Still the peak positions can be analysed.

A hash (`#`) declares everything that follows on the same line to be outside the
hierarchical structure and will be ignored by YAML (or JSON) based information
processing. E.g. the first line of the text representation contains information
not structured due to YAML rules and thus starts with `# # `, where the first
hash means *header* and the second *non-YAML entry*.

Example:

    sample:
        name: Ni1000 
        # there is a scratch on the surface!

---


## the header

The header may contain more sections than presented below - and also the sections may
contain user-defined `key: <value>` pairs on all levels. These of course should not
interfere with defined content, and the rules for units and formats should be applied as
stated above.

The header follows a hierarchical structure and is formatted according to YAML (see below) 
or JSON rules. In addition, each line of the header starts with a hash and a space `# `
(wrapped YAML), which is the default header marker in Python (and other languages).


### first line

The first line contains information about

- the general content;
- the ORSO file format version (and level of strictness) used;
- the encoding;
- a link to orso.

Since it is not part of the YAML hierarchy, a second hash is needed.

    # # ORSO reflectivity data file | 0.1 standard | YAML encoding | https://www.reflectometry.org/`  

### second line

optional, recommended

This (comment) line should help the user to identify the content based on a few key words.
It is free format and no further rules apply.

    # # <title> | <date> | <sample name> | <what>
    
e.g.

    # # Interdiffusion in Fe | 2020-12-24 | sample fe-457-2 | R(q_z)

### data source

mandatory

This section contains information about the origin and ownership of the raw data, 
together with details !!!

All entries marked with an asterisk `*` are optional.

    # data_source:           This information should be available from the raw data 
                             file. If not, one has to find ways to provide it.  

    #     owner:             This refers to the actual owner of the data set, i.e.
                             the main proposer or the person doing the measurement
                             on a lab reflectometer
    #         name:          
    #         affiliation:     
    #         contact:       * 
    #     experiment:  
    #         title:         * proposal or project title
    #         instrument:    
    #         start_date:    yyyy-mm-dd
    #         probe:         neutrons or x-rays
    #         facility:      
    #         proposalID:    *
    #         doi:           * might be provided by the facility
    #     sample:  
    #         name:          string identifying the individual sample or the subject and state being measured
    #         type:          * one of solid/liquid, liquid/solid, gas/liquid, liquid/liquid, solid/gas, gas/solid 
    #         composition:   * free text notes on the nominal composition of the sample  
                               e.g. Si | SiO2 (20 A) | Fe (200 A) | air (beam side)
                               this line/section might contain information to be understood by analysis software
    #         description:   * free text, further details of the sample, e.g. size
    #         environment:   * free text, name of the sample environment device(s)

The following list of sample parameters is incomplete and expandable.
All these entries are optional.

    #         temperature:
    #             unit:
    #             value:
    #             min: 
    #             max:

In case there are several temperatures:

    #           - description:
    #             unit:
    #             value:
    #             min:
    #             max:
    #           - description:
    #             unit:
    #             value:
    #             min:
    #             max:

    #         magnetic_field:
    #             unit:
    #             value:
    #             direction: 
    #         electric_potential:
    #             unit:      V
    #             value:    
    #         electric_current:
    #             unit:      A
    #             value:
    #         electric_ac_field: 
    #             amplitude:
    #                 unit:
    #                 value:
    #             frequency: 
    #                 unit:
    #                 value:
    
and so on for `pressure`, `surface_pressure`, `pH`, ....



    #    measurement: 
    #         scheme:               * one of angle-dispersive / energy-dispersive / angle- and energy-dispersive 
    #         instrument_settings:  
    #             configuration:    * half / full polarized | liquid_surface | ....   free text
    #             incident_angle:  
    #                 unit:        
    #                 value:
    #                 min:  
    #                 max:   
    #             wavelength:
    #                 unit:       
    #                 value:
    #                 min: 
    #                 max: 
    #             polarization:     for neutrons one of  unpolarized / p / m / pp / pm / mp / mm  / vector
                                    for x-rays one of ...  

    #         data_files:  
    #             - file:           free text (file name or identifier doi)
    #               timestamp:      yyyy-mm-ddThh:mm:ss
    #             - file:       
    #               timestamp:  
    #         references:  
    #             - file:   
    #               timestamp: 
  
  
### data reduction

This section is mandatory whenever some kind of data reduction was performed. 

An example where it is not required is the output of an x-ray lab source, as 
long as no normalisation or absorber correction has been performed.

The content of this section should contain enough information to rerun
the reduction, either by explicitly hosing all the required information,
or by referring to a Nexus representation, a notebook or a log file. 

    # reduction:  
    #      software:
    #          name:         name of the reduction software
    #          version:      
    #          platform:     * operating system
    #      computer:         * computer name
    #      call:             * if applicable, command line call or similar 
    #      script:           * path to e.g. notebook
    #      binary:           * path to full information file
    #      timestamp:        date and time of file creation

The following subsection identifies the person or routine who created this file.
She/he is the one responsible for the content.

    #      creator:           
    #          name:         
    #          affiliation:   
    #          contact:       *

Optional, but recommended is a list of corrections performed in free text.
This helps the user to set the respective parameters for the data analysis.

In case a correction step follows a certain published algorithm, a link
to the publication or homepage might be given.

This part might be expanded by defined entries, which are understood by
data analysis software.

    #      corrections:          free text to inform user
    #         - footprint
    #         - background
    #         - polarisation
    #         - ballistic correction
    #         - incident intensity
    #         - detector efficiency 
    #         - scaling / normalisation
    #      comment: |
    #         Normalisation performed with a reference sample            

The `comment` is used to give some more information. 

### column description

This data representation is meant to store a physical observable *R* / *I*
as a function of a variable *Qz*. Together with the related information about
the error of *R* / *I* and the resolution of *Qz* this leads to the defined leading 4 
columns of the data set. I.e.

1. *Qz* with units
2. *I* or *R* with units (if applicable)
3. *sigma* of *I* or *R* with units (if applicable)
4. *sigma* of resolution of *Qz* with units 

where for columns 3 and 4, *sigma* is the standard deviation of a Gaussian
distribution.

- The first column must be called *Qz*, the units must either be `1/angstrom` or `1/nm`.
- The second column must be the physically observed value. It is strongly advised that
this be normalised reflectivity (called *R*), but can also be un-normalised intensity
(called *I*). In the latter case units should be provided, e.g. 1/s. The naming of the
third column is then *sR* or *sI*.
- It's strongly advised that the third and fourth columns are provided. If these are
unknown then a value of 'nan' can be used in the data array. The fourth column must
have the same units as the first.

The example given refers to *R(Qz)* which has unit 1

    # columns:
    #      - name:        Qz
    #        unit:        1/angstrom 
    #        description: wavevector transfer
    #      - name:        R
    #        description: reflectivity
    #      - name:        sR 
    #        description: standard deviation of reflectivity
    #      - name:        sQz
    #        unit:        1/angstrom 
    #        description: standard deviation of wavevector transfer resolution

Further columns can be of any type, content and order. But always with
description and units. These further columns correspond to the fifth column onwards,
meaning that the third and fourth columns must be specified.

    #     - name:        alpha_i
    #       unit:        deg  
    #       description: angle of incidence
    #     - name:        lambda
    #       unit:        angstrom 
    #       description: wavelength

If there are multiple data sets in one file, the first one can be given an identifier
with the optional line:

    # data_set:   * <identifier>

Also optionally there might be a short-notation column description preceded with
a hash, since this line is outside the YAML structure

    # #         Qz             R              sR              sQz

---

## data set

The data set is organised as a rectangular array, where all entries in a column have the
same physical meaning. The leading 4 columns strictly have to follow the rules stated
in the *column description* section.

- All entries have to be of the same data type, preferably float.
- There is no leading space.
- Separators are spaces, tabs are not allowed.
- Whilst it's strongly advised to provide values for the third and fourth columns, if
these are unknown then use `nan` for the values.

- It is recommended to use the same format for all columns,
  preferably `'%-22.16e'`.

```
1.0356329600000000e-02 3.8810006800000001e+00 4.3390906800000000e+00 5.1781647800000000e-05
1.0671729400000000e-02 1.1643051099999999e+01 8.8925271899999991e+00 5.3358647100000001e-05
...
```

## multiple data sets

In case there are several data sets in one file, e.g. for different spin states or temperatures, 
the following rules apply:

### separator

Optionally, the beginning of a new data set is marked by an empty line.
This is recognised by gnuplot as a separator for 3 dimensional data sets.

The mandatory separator between data sets is the string

    # data_set: <identifier>

where `<identifier>` is either an unique name or a number. The default numbering of data sets starts with 0, the first additional one thus gets number 1 and so on.

### overwrite meta data

Below the separator line, metadata might be added. These overwrite the metadata supplied in the header 
(i.e. data set 2 does not know anything about the changes made for data set 1).


For the case of additional input data with different spin state this might look like

    #     data_source:
    #         measurement:
    #             polarization: m
    #     reduction:
    #         input_files:
    #             data_files:
    #                 - file:      amor2020n001930.hdf
    #                   timestamp: 2020-02-03T15:27:45


### repetition of short-version column description

optional

    # #         Qz             R              sR              sQz          lambda

### next data set

The following data set has to be of the same format (number, format and description of columns) as data set 0,
probably with a different number of rows.

```
1.0356329600000000e-02 3.8810006800000001e+00 4.3390906800000000e+00 5.1781647800000000e-05
1.0671729400000000e-02 1.1643051099999999e+01 8.8925271899999991e+00 5.3358647100000001e-05
...
```

---

## the end

There are no rules yet for a footer. Thus creating one might collide with future versions of the ORSO (.ort) format.
