from amie.db import AccountDB

rtdb = AccountDB('testing', 'taqiu', 'password', 'public', True)
rtdb.create_project('GRANTNUM', '')
rtdb.create_project('GRANTNUM2', None)
rtdb.create_project('GRANTNUM1', 'TG-GRANTNUM1')
rtdb.create_project('GRANTNUM3', 'GRANTNUM3') # BAD example
rtdb.close()