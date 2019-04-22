from Client import Client
user = input("User: ")
passw = input("Pass: ")
method = input("Method: ")

cli = Client(method, user, passw)
print(cli.c)