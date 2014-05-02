import db
import time
from config import get_config
from models import Packet
import sys

#from SOAPpy import SOAPProxy

############################### Read configuration file #######################################
cfg = get_config()
black_list = map(int, cfg.get('common', 'black-list').split(','))
tg_database = cfg.get('amie', 'database')
tg_user = cfg.get('amie', 'user')
tg_password = cfg.get('amie', 'password')
tg_schema = cfg.get('amie', 'schema')

rt_database = cfg.get('accounting', 'database')
rt_user = cfg.get('accounting', 'user')
rt_password = cfg.get('accounting', 'password')
rt_schema = cfg.get('accounting', 'schema')



def get_unix_id(username):
    url = 'https://itaccounts.iu.edu/soap/tg.cgi'
    proxy = 'https://itaccounts.iu.edu/TG'
    SOAPaction = "https://itaccounts.iu.edu/TG#get_unix_id"

    #server = SOAPProxy(url, proxy, soapaction=SOAPaction)

    #return int(server.get_unix_id(
    #  username,'603362a5264513d758b2f883abab55d0'))
    return 3456666



def is_iu_user(email):
    """
    check whether the e-mail is an IU user email
    return the username if true else None
    """
    email = email.lower()
    if '@iu.edu' in email or '@iupui.edu' in email\
         or '@indiana.edu' in email:
        return email.strip().split('@')[0]
    return None


def check_point(turn_on=False):
    if turn_on:
        checkpt = 'n'
        while True:
            checkpt = raw_input("Good data or not.. continue (y/n): ")
            if checkpt == 'n':
                print "FAILED at CHECKPOINT -----------------------------FAIL"
                sys.exit(1)
            elif checkpt == 'y':
                break
            else:
                print 'Unknown options!'

###################################  Process rac ###############################################

def process_rac(packet_rec_id=None, verbose=False, checkpt=False):
    """
    process request account create packet
    """
    tgdb = db.AmieDB(tg_database, tg_user, tg_password, tg_schema, verbose)
    rtdb = db.AccountDB(rt_database, rt_user, rt_password, rt_schema, verbose)
    
    if packet_rec_id is None:
        packets = tgdb.find_all_packets(['type_id=16', 'state_id=6'], black_list)
        for packet in packets:
            _process_single_rac(tgdb, rtdb, packet, verbose, checkpt)
    else:
        packet = tgdb.find_packets(packet_rec_id)
        _process_single_rac(tgdb, rtdb, packet, verbose, checkpt)

    tgdb.close()
    rtdb.close()
    

def _process_single_rac(tgdb, rtdb, in_packet, verbose=False, checkpt=False):
    """
    process a single request account create packet
    """
    if verbose:
        print '[%s] process rac packet [%s]' % (time.asctime(), in_packet.packet_rec_id)
    
    email = in_packet.get_value('UserEmail')
    first_name = in_packet.get_value('UserFirstName')
    middle_name = in_packet.get_value('UserMiddleName')
    last_name = in_packet.get_value('UserLastName')
    
    # create new account
    username = rtdb.is_existing_user(email, first_name, last_name)
    if username is None:
        # check whether it is a user by email
        iu_user = is_iu_user(email)
        if iu_user is not None:
            if verbose:
                print '[%s] user [%s] is a iu user' % (time.asctime(), iu_user)
            iu_user_status = 't'
            username = iu_user
        else:
            iu_user_status = 'f'
            username = rtdb.generate_new_username(first_name, middle_name, last_name)
            if verbose:
                print '[%s] new user name is [%s]' % (time.asctime(), username)
        
        unixid = get_unix_id(username)
        # create new user account in db
        rtdb.add_new_user(username, unixid, email, first_name, last_name, iu_user_status, 't')
    
    check_point(checkpt)

    grant_number = in_packet.get_value('GrantNumber')
    resource_list = in_packet.get_value('ResourceList')
    project_id = in_packet.get_value('ProjectID')

    cluster_nm = rtdb.find_cluster_by_resource_list(resource_list)
    group_name='teragrid'
    
    if not rtdb.is_existing_project(grant_number, project_id):
        raise Exception('Project does not exist')
    rtdb.create_cluster_account(username, cluster_nm, group_name)
    rtdb.allocate_resource(project_id, username, cluster_nm)
    
    check_point(checkpt)
    
    # create outgoing packet
    out_packet = Packet()
    out_packet.trans_rec_id = in_packet.trans_rec_id
    out_packet.packet_id = 1  
    out_packet.type_id = 6
    out_packet.version = '1.0'
    out_packet.state_id = 2
    out_packet.outgoing_flag = 1
    out_packet.expected_reply_type = 1
    
    # copy data to the outgoing packet
    for tag in ('NsfStatusCode', 'UserCountry', 'UserDepartment', 'UserCitizenship', 'UserCity',
                'UserEmail', 'UserFirstName', 'UserGlobalID', 'UserLastName', 'UserOrgCode',
                'UserOrganization', 'UserState', 'UserTitle', ):
        out_packet.set_value(tag, in_packet.get_value(tag))
    
    # copy list
    # 'UserDnList', 'UserRequestedLoginList', 'ResourceList'
    for tag in ('UserDnList', 'UserRequestedLoginList', 'ResourceList'):
        if tag in in_packet.data:
            out_packet.data[tag] = in_packet.data[tag]
    
    out_packet.set_value('ProjectID', project_id)
    out_packet.set_value('UserRemoteSiteLogin', username)
    out_packet.set_value('UserPersonID', username)
    
    # add outgoing packet to database
    tgdb.add_packet(out_packet)
    

   
        
###################################  Process RPC ###############################################    
def process_rpc(packet_rec_id=None, verbose=False, checkpt=False):
    """
    The request_project_create packet contains information to be used by a 
    local site to create a project and an account for the PI on the project. 
    The result of this request should be the creation of a local site project 
    (with a local project ID) as well as an account for the PI 
    """
    tgdb = db.AmieDB(tg_database, tg_user, tg_password, tg_schema, verbose)
    rtdb = db.AccountDB(rt_database, rt_user, rt_password, rt_schema, verbose)
    
    if packet_rec_id is None:
        packets = tgdb.find_all_packets(['type_id=19', 'state_id=6'], black_list)
        for packet in packets:
            _process_single_rpc(tgdb, rtdb, packet, verbose, checkpt)
    else:
        packet = tgdb.find_packets(packet_rec_id)
        _process_single_rpc(tgdb, rtdb, packet, verbose, checkpt)

    tgdb.close()
    rtdb.close()


def _process_single_rpc(tgdb, rtdb, in_packet, verbose=False, checkpt=False):
    """
    process a single request project create packet
    """
    if verbose:
        print '[%s] process rpc packet [%s]' % (time.asctime(), in_packet.packet_rec_id)
    
    email = in_packet.get_value('PiEmail')
    first_name = in_packet.get_value('PiFirstName')
    middle_name = in_packet.get_value('PiMiddleName')
    last_name = in_packet.get_value('PiLastName')   
    
    # create new account
    username = rtdb.is_existing_user(email,first_name, last_name)
    if username is None:
        # check whether it is a user by email
        iu_user = is_iu_user(email)
        if iu_user is not None:
            if verbose:
                print '[%s] user [%s] is a iu user' % (time.asctime(), iu_user)
            iu_user_status = 't'
            username = iu_user
        else:
            iu_user_status = 'f'
            # generate a user name according to user's name
            username = rtdb.generate_new_username(first_name, middle_name, last_name)
            if verbose:
                print '[%s] new user name is [%s]' % (time.asctime(), username)
        
        unixid = get_unix_id(username)
        # create new user account in db
        rtdb.add_new_user(username, unixid, email, first_name, last_name, iu_user_status, 't')
            
    check_point(checkpt)
        
    # allocation resource for the project
    grant_number = in_packet.get_value('GrantNumber')
    resource_list = in_packet.get_value('ResourceList')
    project_id = in_packet.get_value('ProjectID')
    
    cluster_nm = rtdb.find_cluster_by_resource_list(resource_list)
    group_name='teragrid'
    
    # if project id is none, a project id will be returned
    project_id = rtdb.create_project(grant_number, project_id)
    rtdb.create_cluster_account(username, cluster_nm, group_name)
    rtdb.allocate_resource(project_id, username, cluster_nm)
    
    check_point(checkpt)
    
    # create outgoing packet
    out_packet = Packet()
    out_packet.trans_rec_id = in_packet.trans_rec_id
    out_packet.packet_id = 1  # the packet ID that AMIE specifies, we set it to '1' because it is a new packet
    out_packet.type_id = 7
    out_packet.version = '1.0'
    out_packet.state_id = 2
    out_packet.outgoing_flag = 1
    out_packet.expected_reply_type = 2
    
    # copy data to the outgoing packet
    for tag in ('AllocatedResource', 'ResourceList', 'AllocationType', 'Comment', 
                'EndDate', 'GrantNumber', 'NsfStatusCode', 'PfosNumber', 'PiCitizenship', 
                'PiCity', 'PiCountry', 'PiDepartment', 'PiEmail', 'PiFirstName', 'PiGlobalID',
                'PiLastName', 'PiOrgCode', 'PiOrganization', 'StartDate', 'ServiceUnitsAllocated',
                'ProjectTitle'):
        out_packet.set_value(tag, in_packet.get_value(tag))
    
    # copy list
    # 'PiRequestedLoginList',  'Sfos', 'PiDnList'
    for tag in ('PiRequestedLoginList', 'Sfos', 'PiDnList'):
        if tag in in_packet.data:
            out_packet.data[tag] = in_packet.data[tag]

    
    # 'ProjectID',  username ('PiRemoteSiteLogin', 'PiPersonID')
    out_packet.set_value('ProjectID', project_id)
    out_packet.set_value('PiRemoteSiteLogin', username)
    out_packet.set_value('PiPersonID', username)
    
    # add outgoing packet to database
    tgdb.add_packet(out_packet)
    