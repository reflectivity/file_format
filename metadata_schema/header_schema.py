"""
Generates the schema for an ORSO file.

Author: Brian Maranville (NIST)
"""
import datetime
import enum
from typing import Optional, Union, List, Literal, Dict, Any
from dataclasses import field

GENERATE_SCHEMA = True


def d(t):
    return field(metadata={"description": t})


if GENERATE_SCHEMA:
    from pydantic.dataclasses import dataclass as _dataclass

    class Config:
        @staticmethod
        def schema_extra(schema: Dict[str, Any]) -> None:
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)

    dataclass = _dataclass(config=Config)
else:
    from dataclasses import dataclass


@dataclass
class Creator:
    name: str
    affiliation: str
    time: datetime.datetime = d(
        "timestamp string, formatted as ISO 8601 datetime")
    computer: str


@dataclass
class owner:
    name: str
    affiliation: str
    contact: str


@dataclass
class Sample:
    name: str


@dataclass
class Experiment:
    instrument: str
    probe: Union[Literal['neutrons', 'x-rays']]
    facility: Optional[str] = None
    ID: Optional[str] = None
    date: Optional[datetime.datetime] = field(metadata={
                                              "description": "timestamp string, formatted as ISO 8601 datetime"}, default=None)
    title: Optional[str] = None


class Polarisation(str, enum.Enum):
    """ The first symbol indicates the magnetisation direction of the incident beam.
    An optional second symbol indicates the direction of the scattered beam, if a spin analyser is present."""
    p = '+'
    m = '-'
    mm = '--'
    mp = '-+'
    pm = '+-'
    pp = '++'


@dataclass
class data_file:
    file: str
    created: datetime.datetime


@dataclass
class Value:
    magnitude: Union[float, List[float]]
    unit: str = field(metadata={
        "description": "SI unit string"})


@dataclass
class ValueRange:
    min: float
    max: float
    unit: str = field(metadata={
        "description": "SI unit string"})
    steps: Optional[int] = None


@dataclass
class instrument_settings:
    incident_angle: Union[Value, ValueRange]
    wavelength: Union[Value, ValueRange]
    polarisation: Optional[Polarisation] = None


@dataclass
class Measurement:
    scheme: Union[Literal["angle- and energy-dispersive",
                          "angle-dispersive",
                          "energy-dispersive"]]
    instrument_settings: instrument_settings
    data_files: List[data_file]


@dataclass
class Reduction:
    software: str
    call: str


@dataclass
class DataSource:
    owner: owner
    experiment: Experiment
    sample: Sample
    measurement: Measurement


@dataclass
class column:
    """
    Information on a data column.
    """

    name: str = d("The name of the column")
    dimension: str
    unit: Optional[Literal["1/angstrom","1/nm"]] = field(default=None, metadata={
                                "description": "SI unit string"})
    #description: Optional[str] = field(
    #    default=None, metadata={"description": "A description of the column"})


@dataclass
class ORSOHeader:
    creator: Creator
    data_source: DataSource
    columns: List[column]
    reduction: Optional[Reduction] = None


if GENERATE_SCHEMA:
    schema = ORSOHeader.__pydantic_model__.schema()
    print(schema)
    import json
    open("refl_header.schema.json", 'wt').write(json.dumps(schema, indent=2))

    import yaml
    open("refl_header.schema.yaml", 'w').write(yaml.dump(schema))
