from amie.db import AccountDB

rtdb = AccountDB('testing', 'taqiu', 'password', 'public', True)
rtdb.is_existing_project('GRANTNUM', '')
rtdb.is_existing_project('GRANTNUM2', None)
rtdb.is_existing_project('GRANTNUM1', 'TG-GRANTNUM1')
rtdb.is_existing_project('GRANTNUM3', 'GRANTNUM3') # BAD example
rtdb.close()