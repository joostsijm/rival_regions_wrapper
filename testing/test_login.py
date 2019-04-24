from Client import Client

user = input("User: ")
passw = input("Pass: ")
method = input("Method: ")

cli = Client(method, user, passw, show_window=False)
print(cli.c)
# print(cli.market_info('oil'))
market_info = cli.get_all_market_info()
for i in market_info:
    print("")
    print(i.upper())
    print("#"*len(i))
    for j in market_info[i]:
        print(j.upper() + ':' + market_info[i][j])

# cli.create_article("Test","Whoops")