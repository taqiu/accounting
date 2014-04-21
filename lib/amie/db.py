import random
import psycopg2
import models
import time


class AccountDB():
    """
    This class provides operations for accounting database.
     
    Relations: 
        accounting.user (username, unixid, email, first_name, last_name, iu_user, teragrid_user)
        
        accounting.teragrid_project  (id, status)
        accounting.teragrid_allocation (username, cluster_name, project, status)
        accounting.teragrid_resource_to_cluster  (resource_name, cluster_name)
        
        accounting.cluster_account (username, cluster_name, status)
        accounting.cluster_account_group (username, cluster_name, group_name)
        accounting.cluster_account_primary_group (username, cluster_name, group_name)
    """
    
    def __init__(self, database, user, password, schema, verbose=False):
        self.schema = schema
        self.verbose = verbose
        if self.verbose: 
            print '[%s] Connect accounting database [%s] as user [%s]' % (time.asctime(), database, user)
        self.conn = psycopg2.connect(database=database, user=user, password=password)
        self.cursor = self.conn.cursor()


    def close(self):
        if not self.cursor.closed:
            self.cursor.close()
        if not self.conn.closed:
            self.conn.close()

        
    def __del__(self):
        self.close()        


    def is_existing_user(self, email, first_name, last_name):
        """
        check whether the user exists by email 
        """
        self.cursor.execute("SELECT username FROM %s.user WHERE email like '%s';" % (self.schema, email))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        
        # sometimes, user might change their email domain
        # check this with their firstname and last name
        email_id = email.stript().split('@')[0]
        self.cursor.execute("""SELECT username FROM %s.user 
                            WHERE email like '%s%%' 
                            AND first_name like '%s' 
                            AND last_name like '%s';""" % (self.schema, email_id, first_name, last_name))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        
        return None



    def add_new_user(self, username, unixid, email, first_name, last_name, iu_user, teragrid_user):
        """
        Add a new account record into user table
        """
        self.cursor.execute("INSERT INTO %s.user (username, unixid, email, first_name, last_name, iu_user, teragrid_user) VALUES ('%s',%i,'%s','%s','%s','%s','t');" 
                        % (self.schema, username, unixid, email, first_name, last_name,iu_user, teragrid_user))



    def find_cluster_by_resource_list(self, resource_list):
        """
        
        """
        self.cursor.execute("SELECT cluster_name FROM %s.teragrid_resource_to_cluster WHERE resource_name = '%s';" % (self.schema, resource_list))
        try:
            cluster_nm = self.cursor.fetchone()[0]
            print("cluster is '%s'"%(cluster_nm))
            return cluster_nm
        except IndexError:
            print "ERROR - Did NOT get valid <cluster_nm>"
        return None
        


    def create_cluster_account(self, username, cluster_nm, group_name):
        """
        create cluster account and group if user is not created
        return True if user is created otherwise False
        """
        is_new_account = False
        self.cursor.execute("""SELECT * FROM %s.cluster_account 
                        WHERE username = '%s' and cluster_name = '%s';"""
                         % (self.schema, username, cluster_nm))
        
        if self.cursor.fetchone() is None:
            print("Creating cluster_acct (and group) records now!")
            self.cursor.execute("BEGIN;")
            self.cursor.execute("""INSERT INTO %s.cluster_account 
                        (username, cluster_name, status) 
                        VALUES ('%s','%s','create');""" % (self.schema, username, cluster_nm))
            self.cursor.execute("""INSERT INTO %s.cluster_account_group 
                        (username, cluster_name, group_name) 
                        VALUES ('%s', '%s', '%s');""" % (self.schema, username, cluster_nm, group_name))
            self.cursor.execute("""INSERT INTO %s.cluster_account_primary_group
                        (username, cluster_name, group_name) 
                        VALUES ('%s', '%s', '%s');""" % (self.schema, username, cluster_nm, group_name))
            self.cursor.execute("COMMIT;")
            is_new_account = True
            
        return is_new_account
        

      
    def create_project(self, grant_number, project_id):
        """
        Create a project record in the accounting database.
        If the project exist, no new record will be created.
        The project ID must be 'TG-' + grant_number. Otherwise, an exception will be raised.
        If the project_id is None or empty string, the project id will 'TG-' + grant_number
        Return project_id if the operation succeed. 
        """
        # check project id
        check_proj = 'TG-'+grant_number
        if project_id and project_id != check_proj:
            raise Exception('bad project id')
        project_id = check_proj
        
        # create project if doesn't exist
        self.cursor.execute("""SELECT * FROM %s.teragrid_project 
                    WHERE id = '%s';""" % (self.schema, project_id))
        if self.cursor.fetchone() is None:
            self.cursor.execute("""INSERT INTO %s.teragrid_project (id, status) 
                                VALUES ('%s','enabled');""" % (self.schema, project_id))

        return project_id



    def is_existing_project(self, project_id, grant_number):
        """
        Check whether the project exist in the database
        """
        check_proj = 'TG-'+grant_number
        if project_id and project_id != check_proj:
            return False
        project_id = check_proj
        # create project if doesn't exist
        self.cursor.execute("""SELECT * FROM %s.teragrid_project 
                    WHERE id = '%s';""" % (self.schema, project_id))
        if self.cursor.fetchone() is None:
            return False
        return True
    
    
    
    def allocate_resource(self, project_id, username, cluster_nm):
        # allocate resource
        self.cursor.execute("""SELECT status from %s.teragrid_allocation  
                        WHERE cluster_name = '%s' AND project = '%s';""" 
                        % (self.schema, cluster_nm, project_id))
        alloc_status = self.cursor.fetchone()
        if alloc_status:
            print "allocation exists; '%s' on '%s' for '%s'; status is: '%s'"\
                    % (project_id, cluster_nm, username, alloc_status[0])
            if alloc_status[0] == 'disable':
                print 'enable resource'
                self.cursor.execute("""UPDATE %s.teragrid_allocation 
                                    SET status = 'enabled' 
                                    WHERE project = '%s' AND cluster_name = '%s';""" 
                                    % (self.schema, project_id, cluster_nm))
        else:
            print 'allocate resource for project %s' % project_id
            self.cursor.execute("""INSERT INTO %s.teragrid_allocation 
                            (username, cluster_name, project, status) 
                            VALUES ('%s', '%s', '%s', 'enabled');"""
                             % (self.schema, username, cluster_nm, project_id))
        

    
    def generate_teragrid_username(self, first_name, middle_name, last_name):
        """
        generate candidate user names and pick one from them 
        return None if no candidate user name is available
        """
        attempt_list=[]
        # initialize three parts
        part_one = first_name and first_name.lower() or ''
        part_two = last_name and last_name.lower() or ''
        part_three = middle_name and middle_name.lower() or ''
        
        # candidate user name 1
        attempt_list.append('tg-'+part_one[:1] + part_two[:6])
        # candidate user name 2
        attempt_list.append('tg-'+part_one[:2] + part_two[:5])
        # candidate user name 3
        attempt_list.append('tg-'+part_one[:2] + part_three[:1] + part_two[:4])
        # another five candidate user names with random number
        for _ in range(5):
            randy = str(random.randint(100,200))[1:]  # generate 2-digit random string
            attempt_list.append('tg-'+part_one[:1] + part_two[:5] + randy)
        
        # check availability
        for attempt_this in attempt_list:
            self.cursor.execute("SELECT 1 FROM %s.teragrid_user WHERE username = '%s';" % (self.schema, attempt_this))
            if len(self.cursor.fetchall()) == 0: 
                return attempt_this
            
        return None




class AmieDB():
    """
    This class provides basic database operations for AMIE packet database.  
    """
    
    def __init__(self, database, user, password, schema, verbose=False):
        self.schema = schema
        self.verbose = verbose
        if self.verbose: print '[%s] Connect amie database [%s] as user [%s]' % (time.asctime(), database, user)
        self.conn = psycopg2.connect(database=database, user=user, password=password)
        self.cursor = self.conn.cursor()

 
    def close(self):
        if not self.cursor.closed:
            self.cursor.close()
        if not self.conn.closed:
            self.conn.close()

       
    def __del__(self):
        self.close()
    
        
    def find_packet(self, packet_rec_id):
        """
        Return a Packet object with the given packet_rec_id
        """
        packets = self.find_all_packets(conditions=['packet_rec_id=%s' % packet_rec_id])
        return packets[0] if packets else None



    def find_all_packets(self, conditions=[], black_list=[], limit=25):
        """
        Return a bunch of Packets which satisfy the given conditions.
        The conditions should be SQL statement, for example 'state_id=12'
        Black list is a list of packet_rev_id
        """
        sql = """SELECT packet_rec_id, trans_rec_id, packet_id, 
            type_id, version, state_id, outgoing_flag, ts 
            FROM %s.packet_tbl
            WHERE packet_rec_id IN (
                SELECT packet_rec_id
                FROM %s.data_tbl
                WHERE VALUE LIKE 'mason.iu.xsede') """ % (self.schema, self.schema)
        if conditions:                   
            sql += ' AND ' + ' AND '.join(conditions)
        if black_list:
            sql += " AND packet_rec_id NOT IN ('%s')" % ','.join(black_list)
        sql += " LIMIT '%d'" % limit
        
        results = []
        self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            # get an AMIE packet from database
            packet = models.Packet()
            packet.packet_rec_id = row[0]
            packet.trans_rec_id = row[1]
            packet.packet_id = row[2]
            packet.type_id = row[3]
            packet.version = row[4]
            packet.state_id = row[5]
            packet.outgoing_flag = row[6]
            packet.ts = row[7]
            
            if self.verbose:
                print "[%s] Found packet (packet_rec_id: %s)" % (time.asctime(), packet.packet_rec_id)
            
            # fill packet data
            self._fill_packet_data(packet)
            
            # add to result list
            results.append(packet)
        return results

    
    def _fill_packet_data(self, packet): 
        sql = """SELECT tag, subtag, seq, value
                FROM %s.data_tbl
                WHERE packet_rec_id=%s
              """ % (self.schema, packet.packet_rec_id)
        self.cursor.execute(sql)
        for data_row in self.cursor.fetchall():
            tag, subtag, seq, value = data_row
            subtag = subtag or ""  # change to "" if None
            packet.set_item(tag, value, seq, subtag)


    def add_packet(self, packet): 
        """
        Create a new packet in database
        """
        self.cursor.execute("BEGIN;")
        self.cursor.execute("""INSERT INTO %s.packet_tbl 
                    (trans_rec_id, packet_id, type_id, version, state_id, outgoing_flag, ts)
                     VALUES ('%d', '%d', '%d', '%s', '%d', '%d', CURRENT_TIMESTAMP);""" 
                     % (self.schema, packet.trans_rec_id, packet.packet_id, packet.type_id, packet.version,
                        packet.state_id, packet.outgoing_flag))
        
        # set the packet_rec_id of new packet 
        self.cursor.execute("SELECT CURRVAL('%s.packet_tbl_packet_rec_id_seq'::text) AS id" % (self.schema))
        packet.packet_rec_id = self.cursor.fetchone()[0]
        
        self.cursor.execute("""INSERT INTO %s.expected_reply_tbl 
                        (packet_rec_id, type_id, timeout) VALUES ('%s', '%d', 36000)""" 
                        % (self.schema, packet.packet_rec_id, packet.expected_reply_type))
        
        # save the packet data
        for tag in packet.data.keys():
            for seq in packet.data[tag].keys():
                for subtag in packet.data[tag][seq].keys():
                    if packet.data[tag][seq][subtag] is not None:
                        self.cursor.execute("""INSERT INTO %s.data_tbl 
                            (packet_rec_id, tag, subtag, seq, value) 
                            VALUES ('%d', '%s', '%s', '%d', '%s') """
                            % (self.schema, packet.packet_rec_id, tag, subtag, seq, packet.data[tag][seq][subtag]))
        
        self.cursor.execute("COMMIT;")
            

            
