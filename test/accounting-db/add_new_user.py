from amie.db import AccountDB

rtdb = AccountDB('testing', 'taqiu', 'password', 'public', True)
rtdb.add_new_user('tg-jdoe', 122333, 'johndoe@example.com', 'john', 'doe', 'f', 't')
rtdb.close()