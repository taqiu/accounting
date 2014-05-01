from amie.db import AccountDB

rtdb = AccountDB('testing', 'taqiu', 'password', 'public', True)
print rtdb.is_existing_user('john.doe@example.com', 'john', 'doe')
rtdb.close()