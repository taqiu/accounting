from amie.db import AccountDB

rtdb = AccountDB('testing', 'taqiu', 'password', 'public', True)
print rtdb.create_cluster_account('taqiu', 'mason', 'teragrid')
rtdb.close()