from web3 import Web3
import json

#Connect to Ganache
def makeCar(price,_car_info="TestCar",_additional="change its oil"):
	w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
	#Get smart contract address
	file=open("smartcontract_address.txt", "r")
	cont_addr=file.read()
	file.close()

	abi=json.load(open("smartcontract_abi.json","r")) #get ABI

	contract = w3.eth.contract(address=cont_addr, abi=abi)

	account = w3.eth.accounts[0] 

	#function setCar(uint _carId, bytes32 _car_info, bytes32 _additional, uint _duration)
	_car_info=_car_info 
	_additional=  _additional

	tx_hash = contract.functions.setCar(1,_car_info, _additional,price ).transact({'from': account})
	w3.eth.wait_for_transaction_receipt(tx_hash)

	carinfo = contract.functions.getCarInfo().call({'from': account}) #Call is better for reading, transact for writing to the blockchain
	print(carinfo)

#makeCar("Some new car", "Change its oil dude")