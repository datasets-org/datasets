# Datasets
This project is part of **Datasets** toolkit.

Running server (https://github.com/tivvit/datasets_server) is needed for this
 project to be useful.

## Install 
```sh
pip install git+https://github.com/tivvit/datasets
```

## CLI
`datasets` command is provided after the installation 
### Usage
It is recommended to configure the server address first. You may always 
provide it with `-s`.

#### config
```sh
datasets config
Server address (example.com): localhost
Port: 8000
```
The configuration will be saved to `~/.datasets` and will be used also by the
 python library.

#### new
Generate new UID for the data set and creates file `dataset.yaml` with 
prefilled structure. 

#### scan
Rescan the data sets.

#### info, usages, chagelog
`info` shows all the information about the data set. The data set is 
recognized based on `dataset.yaml` which is searched bottom-up. 

`usages` shows only usages and `changelog` only the changelog respectively

## Lib
Python library for interacting with the **Datasets**.

### Init
```python
from datasets import Datasets

ds = Datasets()
# Without args the address in ~/.datasets will be used or {"addres": 
"http:localhost:5000"} may be used
```

### Info
Returns information about the data set identified by the UID. Second param - 
[usage](#usage-log)
```python
ds.info("8b88a424-dbd8-4032-8be7-a930a415b9a5", {"user": "tivvit"})
```
### Paths
Returns list of paths where the data set may be found. Second param - 
[usage](#usage-log)
```python
ds.paths("8b88a424-dbd8-4032-8be7-a930a415b9a5", {"user": "tivvit"})
# ["/data/a", "/data/b"]
```

### Create
Creates data set in the database. Useful for pragmatical data set creation.

- `data` - dict with the data set attributes
- `path` - path where should the `dataset.yaml` should be created (optional).

Returns data set UID. 
```python
ds.create(data={"name": "Best DS", ...}, path="")
# "8b88a424-dbd8-4032-8be7-a930a415b9a5"
```

## Usage log
Actions are 
logged to the usage log, the second parameter is optional and will be stored 
in the usage log.

## Development

Feel free to contribute.

## Copyright and License
&copy; 2016 [Vít Listík](http://tivvit.cz)

Released under [MIT license](https://github.com/tivvit/datasets/blob/master/LICENSE)
