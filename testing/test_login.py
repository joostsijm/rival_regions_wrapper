from Client import Client

user = input("User: ")
passw = input("Pass: ")
method = input("Method: ")

cli = Client(method, user, passw, show_window=False)
print(cli.c)

# cli.create_article("Test","Whoops")