---
layout: page  
title: "ORSO - file formats - ToDo list"  
author: "Jochen Stahn"  
---

Some of the items mentioned below are discussed in more detail at

[www.reflectometry.org/file_format/specs_discussion](https://www.reflectometry.org/file_format/specs_discussion)

---

## use header syntax (and `orsopy`) for non-ort files

The `.ort` header is in many cases also suitable for other types of data.
Jochen thinks it would be nice if e.g. an omega scan has almost the same
header as an omega-2theta scan....

The differences would be:

- free choice of all columns (order and content)
- the first line can not be the one reserved for R(q)
- the ending can not be `.ort`

Consequences:

- adaption of `orsopy`

#### Votes:

- Do we want this?
- How much standardisation outside the `.ort` will we provide?

#### Responsible:

Jochen

#### Due date:

2022-12-31

---

## standardised optional column descriptions

There is a number of *optional* columns which will be used quite frequently - especially
when used for x-ray data. Brian suggested to give them standardised names so that the
analysis software can be simpler. Suggestions are:

- incident angle
- counting time per point
- attenuation factor
- wavelength
- absolute counts
- incoming beam divergence

#### Actions:

- prepare a list of physical properties
- suggestions for names or key words

#### Votes:

- Do we want this?
- If so: which physical properties with which names and probably symbols (short notation)?

#### Responsible:

tba.

#### Due date:

?

---

## column vs. header 

Brian asked for a clarification / definition in case information is given as a column:

- Does it overwrite the header content?
- Should there be a key in the header pointing to the column?

Artur's suggestion: the analysis software should check the column description and decide
what to use. Recommendation: 'column beats header', but no further rules. This approach
requires standardised column descriptions.
A link in the header to the column (name) helps to avoid ambiguities.
There should be a check in orsopy if the column exists when link is present.

#### Votes:

- Which approach: key, internal link or just a rule how to prioritise column and header?
- If so: definition of key / link / rule.

#### Responsible:

tba.

---

## documentation for `orsopy`

For non-experts it is quite difficult to figure out how to use orsopy. There
should be some guide on how to start and how to add header info.

#### Responsible:

Andrew MCC

---

## errors for physical quantities in the header 

Ability to have an error defined for a quantity in the header, either implemented
similar to how quantities are allowed to have a range, or similar to how columns
are allowed to be an error of another column.

#### Responsible:

?

---

## open issues on output of lab x-ray sources

The output of lab x-ray reflectometers is be both, a raw and (partially) reduced data file. Thus there must be
more information provided. An example is the cathod material, the chosen line(s)
with name, energy and relative intensity, probably the monochromator....

#### Responsible:

tba.

---

## contacts to lab x-ray reflectometer manufacturers

#### Tasks:

#### Responsible:

tba.

---

## next release of `orsopy`

In the meantime several corrections and additions have been made to orsopy. 

- When will the next version be released?
- Who is deciding this?

---
