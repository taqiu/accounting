from amie.db import AccountDB

rtdb = AccountDB('testing', 'taqiu', 'password', 'public', True)
print rtdb.find_cluster_by_resource_list('mason.iu.xsede')
rtdb.close()