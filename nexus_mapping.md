# Proposed mapping of ORSO format to NeXus-compatible HDF5

## Summary
The information to be encoded in the NeXus format `.orb` file will (at least at the beginning)
be the same as the information encoded in the text-format `.ort` file.  The primary difference
will be that an additional `plottable_data` folder in the structure will be created, which 
will follow the standard schema for the NeXus `NXdata` class, to support automatic plotting of
the data.

No additional ORSO [application definition](https://manual.nexusformat.org/classes/applications/index.html)
is specified at this time.  The addition of an application definition for the terms in the header (e.g. `ORSO_class`)
can be discussed in the future, and presents no conflict with this initial proposal for a minimal 
NeXus-compliant file.

## Mapping: orsopy to HDF5
The mapping of the hierarchical metadata structure represented by the orsopy Header subclasses
is fairly straightforward, with special handling required only for python `list`-like attributes.
Note that this definition refers both to python class `attributes` and HDF5 object `attributes`.  The 
latter will always be identified with the `@` symbol to avoid confusion.  In the mapping proposed, 
python class attributes will be mapped to HDF5 `Group` and `Dataset` objects, with HDF5 attributes on those
objects used to provide structural hints and to satisfy the NeXus metadata requirements.

### Header to HDF5
Every instance of a `fileio.Header` subclass is converted to an HDF5 `Group`, so that the hierarchical
structure of the classes is mapped onto the `Group` tree of the HDF5 file.

Python attributes of the `Header` class are converted with these rules:
* if the attribute is a subclass of `Header`, e.g. `Orso.data_source: DataSource`, it is added as a subgroup, with an added HDF5 attribute `@ORSO_class=<class name>`, e.g. `@ORSO_class='DataSource'`, with its own attributes handled according to these rules (recursive)
* if the attribute has type `list` or `tuple`, a new HDF5 subgroup is added with the attribute name, and with the 
HDF5 attribute `@sequence=1`.  All the items in the list are converted according to these rules, and the resulting
HDF5 object (`Dataset` or `Group`) is annotated with a positional index attribute e.g. `@sequence_index=2`
(indexing begins at zero)
  * Naming of the items:  if the items in the list have a python attribute called `name`, that name is used for the 
  created HDF5 attributes in the sequence (Note that this rule will apply to `Column` instances, which have a `name` attribute).  Otherwise they are named according to their position in the list e.g. `"0"`, `"1"`
* if the attribute has type `str`, `float`, `int`, `bool`, or `np.ndarray`, an HDF5 `Dataset` object is created
from the value of the attribute, using automatic HDF5 `dtype` assignment based on the type of the attribute value.
* if the attribute has value `None`, an empty HDF5 dataset is created (with `shape=None`)
* if the attribute has type `datetime.datetime`, it is converted to an ISO 8601 string representation and then added
according to the rules above
* if the attribute has type `Enum`, it is converted to the value of the enum (usually `str` or `int`) and then added
according to the rules above


### Datasets to HDF5
For each `fileio.OrsoDataset` dataset, an HDF5 group is created with the 
HDF5 attributes `@NX_class='NXentry'` and `@ORSO_class='OrsoDataset'`.

Its header (`OrsoDataset.info`) is converted to an HDF5 `Group` called `info` according to
the rules in the previous section.  The data (`OrsoDataset.data`) consists of a list of columns (or an `np.ndarray` where the first
index corresponds to the column number) and is converted by writing an HDF5 `Dataset` for each column, named to match the names
in the `info.columns` section of the header.  For example:

```
/ : (HDF5 Group)
|
└── dataset : (HDF5 Group, ORSO_class='OrsoDataset')
    ├── info : (HDF5 Group, @ORSO_class='Orso')
    │   ├── data_source : (HDF5 Group, @ORSO_class='DataSource')
    |   | ...
    └── data : (HDF5 Group, @sequence=1)
        ├── Qz : (HDF5 Dataset, @sequence_index=0)
        ├── R : (HDF5 Dataset, @sequence_index=1)
        ├── sR : (HDF5 Dataset, @sequence_index=2)
        └── sQz : (HDF5 Dataset, @sequence_index=3)
```

_(note that using the column number as the first index facilitates adding multidimensional 'column' data in the future, and is 
a change from the current alignment used in orsopy where the column number is the second index)_

### Adding the NXdata group
After the columns are written to the `data` group, an additional group `plottable_data`
is created.  It is given the following additional HDF5 attributes:
* `@NX_class = NXdata`
* `@axes = ['Qz']`
* `@signal = 'R'`
* `@Qz_indices = [0]`

Within that group, the following links are created to the columns in the
`data` group, where `fileio.Column` classes retain their names but `fileio.ErrorColumn` classes are named according to their `error_of` attribute, followed by the string '_errors', according to the NeXus convention, as here:
* `plottable_data/Qz` -> `data/Qz`
* `plottable_data/R` -> `data/R`
* `plottable_data/R_errors` -> `data/sR` _(for `ErrorColumn.error_of = 'R'`)_
* `plottable_data/Qz_errors` -> `data/sQz` _(for `ErrorColumn.error_of = 'Qz'`)_
* ...

Resulting structure is like this:
```
/ : (HDF5 Group, @NX_class='NXroot', @default='dataset')
|
└── dataset : (HDF5 Group, @NX_class='NXentry', @default='plottable_data', @ORSO_class='OrsoDataset')
    ├── info : (HDF5 Group, @ORSO_class='Orso')
    │   ├── data_source : (HDF5 Group, @ORSO_class='DataSource')
    |   | ...
    ├── data : (HDF5 Group, @sequence=1)
    |   ├── Qz : (HDF5 Dataset, @sequence_index=0)
    |   ├── R : (HDF5 Dataset, @sequence_index=1)
    |   ├── sR : (HDF5 Dataset, @sequence_index=2)
    |   └── sQz : (HDF5 Dataset, @sequence_index=3)
    └── plottable_data (HDF5 Group, @NX_class='NXdata', @signal='R'...)
        ├── Qz : link to ../data/Qz
        ├── R : link to ../data/R
        ├── R_errors : link to ../data/sR
        └── Qz_errors : link to ../data/sQz
```

An additional HDF5 attribute `@default='plottable_data'` is added to the 
dataset group in accordance with the NeXus standard for finding plottable data.

Two HDF5 attributes are added to the root HDF5 `File` object:
* `@NX_class='NXroot'`
* `@default=<name of first dataset group>`

## Reading back: HDF5 to orsopy
The conversion rules above are applied in reverse upon reading an HDF5-encoded ORSO file.

* HDF5 groups that contains an attribute `@ORSO_class` are loaded into the orsopy class of that name, and the members of the HDF5 group are converted to python attributes of that class.  The `NXdata` group (`plottable_data`) is dropped on reloading, as it represents an additional NeXus-specific mapping that was created entirely to facilitate plotting of the data, and does not exist in the original data structures.

* Any group with the HDF5 attribute `@sequence=1` is loaded into a python `list`, with members ordered according to the `@sequence_index` attributes of the subgroups in the HDF5 group.
* ...etc
