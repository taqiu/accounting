# this is an example of creating packet
from amie.db import AmieDB
from amie.models import Packet


# Create a transaction for testing
"""
insert into public.transaction_tbl 
(originating_site_name, transaction_id, local_site_name, remote_site_name, state_id) 
values ('org_site_name', 123, 'local', 'remote', 2);
select * from public.transaction_tbl;
"""

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

# save the packet into database
tgdb = AmieDB('testing', 'taqiu', 'password', 'public', True)
tgdb.add_packet(packet)
tgdb.close()
