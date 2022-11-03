---
layout: page  
title: "ORSO - file formats - ToDo list"  
author: "Jochen Stahn"  
---

Some of the items mentioned below are discussed in more detail at

> [www.reflectometry.org/file_format/specs_discussion](https://www.reflectometry.org/file_format/specs_discussion)

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

Votes:

- Do we want this?
- How much standardisation outside the `.ort` will we provide?

Responsible:

> Jochen

Due date:

> 2022-12-31
