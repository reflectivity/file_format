# Data representation

Follow-up on meeting of 30sep20 - Joachim Wuttke.

## Common subset of YAML and HDF5, no attributes

To keep things simple, our data model should only use
components that are supported by YAML *and* HDF5. These
are arrays (=lists), dictionaries (=maps=hashes) and
scalars (numbers or strings). This precludes the use
of HDF5 attributes.

In standard ascii representation of HDF5, attributes
are denoted by the prefix "@". In NeXuS, they are used
most prominently to specifiy physical units. This is
a sensible choice within HDF5, but not important enough
to justify the complications it would cause for us.

## Values and ranges with units

This brings us to the question how to represent physical
units. In the YAML community there seems to be consensus
that this is best done by sticking with the hierarchical
nature of the data format,
```
  wavelength: {value: 7.2, unit: angstrom}
```

Also specify that we want flow style here, not block style:
```
  wavelength:
    value: 7.2
    unit: angstrom
```

A related question: how to represent a range. Proposal:
```
  wavelength: {min:4, max:12, unit: angstrom}
```
keeps the specification effort (and the implementation effort
for a possible machine reader) to a minimum; not even the word
"range" is needed.

## Avoid NeXuS folklore

No need for a "root" element. The "group" element of NeXuS
has not been well defined, and is used in different ways,
inconsistent with each other. Avoid all this.

Avoid the "NX" prefix. Avoid data type declarations like "NX_CHAR".

From all of NeXuS, just copy&paste metadata names, stripped
of "NX", and definitions, and adapt them as appropriate for
our field.

## Wrapped YAML

We will not use plain YAML, because often our users just want
the I(q) table; metadata are only tolerated when confined
to comment lines starting with "#". Also, there is no good
way to include columns verbatim in YAML.

Therefore, the ASCII data representation
[proposed by Jochen Stahn](https://www.reflectometry.org/working_groups/file_formats/examples)
is "wrapped YAML": a YAML block with each line prefixed
by "# ", followed by a plain rectangular table.

## Columns definition

To keep the Ascii document self-explaining, the table needs
to be preceded by an explanation of the columns.

As a minor change to Jochen's proposal, the explanation stance
should not be labelled "data", because data is what the entire
file is about. What about "columns":
```
  columns:
  - {column: 1, variable: Qz, unit: angstrom^-1}
  - {column: 2, variable: ReflectedIntensity}
  - {column: 3, variable: sigma(ReflectedIntensity)}
```
