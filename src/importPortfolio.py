import json

def get_portfolio(pf_name):
    with open('portfolios.json') as json_data:
        d = json.load(json_data)
        json_data.close()

    return d.get(pf_name, [])

print(get_portfolio("test1"))

