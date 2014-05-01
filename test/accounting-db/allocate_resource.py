from amie.db import AccountDB

rtdb = AccountDB('testing', 'taqiu', 'password', 'public', True)
rtdb.allocate_resource('TG-123445', 'taqiu', 'cluster name1')
rtdb.close()