AMIE-processing
===============

Recoding AMIE Project Create and Account Create scrips to be object oriented with some expanded functions.

## Prerequisites
* PostgreSQL
* psycopg2

## Installing instructions
1. Configure 'conf/amie-processing.cfg'
  * After installed, its dafault position is '/etc/amie-processing'
  * Modify 'data_files' in setup.py and 'config_path' in lib/amie/config.py to change configuration position
2. Run install script

```shell
./INSTALL
```

## Tools 
The Amie-processing libary provides two command tools for request_account_create and request_project_create packet processing.
 
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
### lib/amie/models.py
This module cantians the Packet class which is used to represent the Amie packets.

```python
# create a new packet
packet = Packet()

# set the attributes of packet
packet.trans_rec_id = 1
packet.packet_id = 4  
packet.type_id = 19
packet.version = '1.0'
packet.state_id = 6
packet.outgoing_flag = 0
packet.expected_reply_type = 7

# set the data of packet
packet.set_value('PiEmail', 'john.doe@example.com')
packet.set_value('PiFirstName', 'John')
packet.set_value('PiMiddleName', '')
packet.set_value('PiLastName', 'Doe')
packet.set_value('GrantNumber', '87WHATEVER')
packet.set_value('ResourceList', 'mason.iu.xsede')
packet.set_value('ProjectID', 'TG-87WHATEVER')

```
### lib/amie/db.py
This module is developed for amie and accounting database operation.
* amie databse

```python
tgdb = AmieDB('testing', 'taqiu', 'password', 'public', True)
tgdb.add_packet(packet) # packet is a models.Packet object
packets = tgdb.find_all_packets(limit=5)
# Found packet with type_id=19 state_id=6
packets = tgdb.find_all_packets(conditions=['type_id=19', 'state_id=6'])
# Found packet by packet_rec_id
packet = tgdb.find_packet(4)
tgdb.close()
```

* accouting database

```python
rtdb = AccountDB('testing', 'taqiu', 'password', 'public', True)
rtdb.add_new_user('tg-jdoe', 122333, 'johndoe@example.com', 'john', 'doe', 'f', 't')
rtdb.close()
```
### lib/amie/accounting.py
This module is developed basing on db.py, it is used to process rpc and rac packets.


