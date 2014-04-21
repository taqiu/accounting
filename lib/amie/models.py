
class Packet():
    """
    This class is used to represent an AMIE packet
    The attributes of packet can be accessed like packet.packet_rec_id
    The data of packet should use set and get methods to access.
       For example,
           packet.get_value('UserEmail', 'john.deo@example.com')
           packet.set_value('UserEmail')
    """
    def __init__(self):
        self.packet_rec_id = None
        self.trans_rec_id = None
        self.packet_id = None
        self.type_id = None
        self.version = None
        self.state_id = None
        self.outgoing_flag = None
        self.ts = None
        self.expected_reply_type = None
        self.data = {}

    ############## get/set data functions #####################
    def set_value(self, tag, value, subtage=""):
        self.set_item(tag, value, 0, subtage)


    def set_list(self, tag, values):
        for i, val in enumerate(values):
            self.set_item(tag, val, i)

    
    def set_item(self, tag, value, seq, subtage=""):
        if tag not in self.data:
            self.data[tag] = {}
        if seq not in self.data[tag]:
            self.data[tag][seq] = {}
        self.data[tag][seq][subtage] = value


    def get_value(self, tag, subtage=""):
        self.get_item(tag, 0, subtage)
        
    
    def get_list(self, tag):
        if self.get_count(tag) == 0:
            return []
        
        size = max(self.data[tag].keys()) + 1
        values = [None]*size
        for seq in self.data[tag].keys():
            values[seq] = self.get_item(tag, seq)
        return values

   
    def get_item(self, tag, seq, subtage=""):
        if tag not in self.data\
         or seq not in self.data[tag]\
         or subtage not in self.data[tag][seq]:
            return None
        
        return self.data[tag][seq][subtage]
    
    
    def get_count(self, tag):
        if tag in self.data:
            return len(self.data[tag])
        else:
            return 0

    
    def __repr__(self):
        return "<Packet(packet_rec_id: %s, trans_rec_id: %s, packet_id: %s, data: %s)>" %\
            (self.packet_rec_id, self.trans_rec_id, self.packet_id, self.data)
    

