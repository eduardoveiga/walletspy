import urllib, json, tabulate, requests
tab = []
fiat = 'USD'
confirmations='6'
etherscan_api_key=''

wallets = json.loads(open("wallet.json").read())

for wallet in wallets:
	if wallet['coin']=='bitcoin' or wallet['coin']=='btc':
		#url = "https://blockexplorer.com/api/addr/"+wallet['address']
		#url = "https://blockchain.info/q/addressbalance/"+wallet['address']+"?confirmations="+confirmations
		url = "https://blockchain.info/q/addressbalance/"+wallet['address']
		
		response = urllib.urlopen(url)
		balance =  float(response.read())/100000000.0
		coin = 'bitcoin'
	elif wallet['coin']=='ether' or wallet['coin']=='ethereum' or wallet['coin']=='eth':
		
		url='https://api.etherscan.io/api?module=account&action=balance&address='+wallet['address']+'&tag=latest&apikey='+etherscan_api_key
		response = urllib.urlopen(url)
		coin_data = json.loads(response.read())
		
		balance= float(coin_data['result'])/1000000000000000000.0
		coin='ethereum'
		
	elif wallet['coin']=='bitcoin-cash' or wallet['coin']=='bch' or wallet['coin']=='bcc':
		url = "https://api.blockchair.com/bitcoin-cash/dashboards/address/"+wallet['address']
		response = urllib.urlopen(url)
		coin_data = json.loads(response.read())
		balance =  float(coin_data['data'][0]['sum_value_unspent'])/100000000.0
		coin='bitcoin-cash'
		
	elif wallet['coin']=='litecoin' or wallet['coin']=='ltc':
		url = 'https://chain.so/api/v2/get_address_balance/ltc/'+wallet['address']
		response = requests.get(url)
		coin_data = response.json()
		print coin_data
		balance =  float(coin_data['data']['confirmed_balance'])
		coin = 'litecoin'
		
	elif wallet['coin']=='dogecoin' or wallet['coin']=='doge':
		url = 'https://chain.so/api/v2/get_address_balance/doge/'+wallet['address']
		response = requests.get(url)
		coin_data = response.json()
		balance =  float(coin_data['data']['confirmed_balance'])
		coin = 'dogecoin'
		
	elif wallet['coin']=='dash':
		url = 'https://chain.so/api/v2/get_address_balance/dash/'+wallet['address']
		response = requests.get(url)
		coin_data = response.json()
		balance =  float(coin_data['data']['confirmed_balance'])
		coin = 'dash'
		
	
		
	else:
		coin=None
	
	
	if(coin!=None):
	
		url = "https://api.coinmarketcap.com/v1/ticker/"+coin+"/?convert="+fiat
		response = urllib.urlopen(url)
		coin_data = json.loads(response.read())
		price =  coin_data[0]['price_'+fiat.lower()]
		balance_converted =  float(price)*float(balance)

		tab.append([coin,wallet['address'],balance,round(balance_converted,2)])
total=0
for i in tab:
	total=total+i[3]
tab.append(['','','',''])
tab.append(['','','TOTAL',total])
print tabulate.tabulate(tab,['coin','address','balance','balance in '+fiat], tablefmt='orgtbl')

