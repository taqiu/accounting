# this is a example for finding packet
from amie.db import AmieDB

tgdb = AmieDB('testing', 'taqiu', 'password', 'public', True)
print '=' * 40
print 'List 5 packets in the database' 
packets = tgdb.find_all_packets(limit=5)
print packets
print '=' * 40
print 'Found packet with type_id=19 state_id=6'
packets = tgdb.find_all_packets(conditions=['type_id=19', 'state_id=6'])
print packets
print '=' * 40
print 'Found packet by packet_rec_id'
packet = tgdb.find_packet(4)
print packet
tgdb.close()