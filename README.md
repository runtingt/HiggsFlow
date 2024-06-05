# HiggsFlow

## Description

Uses the `law` framework to orchestrate the Higgs combination at CMS.

## Setup

To set up the environment for this project, run the `setup.sh` script.

## Class structure

To produce the `*_tasks.pdf` files, use `pyreverse` from `pylint` to run

```sh
pyreverse -o pdf -p tasks tasks/
```

## Changes made to Combine
<!-- TODO just fork combine -->
MultiDimFit.cc: change `ceil` to `floor` in `doGrid()`
