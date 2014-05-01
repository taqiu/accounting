from amie.db import AccountDB

rtdb = AccountDB('testing', 'taqiu', 'password', 'public', True)
print rtdb.generate_new_username('John', '', 'Doe')
print rtdb.generate_new_username('John', None, 'Doe')
print rtdb.generate_new_username('John', 'Stefan', 'Doe')
rtdb.close()