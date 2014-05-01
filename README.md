AMIE-processing
===============

Recoding AMIE Project Create and Account Create scrips to be object oriented with some expanded functions.

## Prerequisites
* PostgreSQL
* psycopg2

## Installing instructions
1. Configure 'conf/amie-processing.cfg'

..* After installed, its dafault position is '/etc/amie-processing'

..* Modify 'data_files' in setup.py and 'config_path' in lib/amie/config.py to change configuration position

2. Run install script

```shell
./INSTALL
```

## Tools 
The Amie-processing package provides two command tools for request_account_create and request_project_create packet processing.
 
* Process request_account_create packet/packets

```shell
$ rac.py -h
usage: rac.py [-h] [--packet_rec_id PACKET_REC_ID] [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  --packet_rec_id PACKET_REC_ID
                        process single packet with the given receive id
  --verbose             print out the processing detail
```

* Process request_project_create packet/packets

```shell
$ rpc.py -h
usage: rac.py [-h] [--packet_rec_id PACKET_REC_ID] [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  --packet_rec_id PACKET_REC_ID
                        process single packet with the given receive id
  --verbose             print out the processing detail
```

## Main Modules 
* lib/amie/accounting.py
* lib/amie/db.py
* lib/amie/models.py
