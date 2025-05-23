#pip install web3 py-solc-x
#NOTE: IN THE PROJECT THIS CODE MUST BE EXECUTED ONLY ONCE, DO NOT DEPLOY MULTIPLE CONTRACTS

from web3 import Web3
from solcx import compile_source, install_solc
import json

def deploy_contract():
	install_solc('0.8.0')

	file=open("smartcontract.sol", "r")
	source = file.read()

	comp = compile_source(source, solc_version="0.8.0")
	contract_id, contract_interface = comp.popitem()

	abi = contract_interface['abi']
	bytecode = contract_interface['bin']

	#Create ABI of contract
	file=open("smartcontract_abi.json", "w")
	json.dump(abi, file)
	file.close()

	#Create bytecode of contract
	file=open("smartcontract_bytecode.txt", "w")
	file.write(bytecode)
	file.close()

	print("Contract complied")

	#Start deployment 

	ganache_url = "http://127.0.0.1:7545" #connect to ganache 
	w3 = Web3(Web3.HTTPProvider(ganache_url))

	abi=json.load(open("smartcontract_abi.json","r")) #get ABI
	bytecode= open("smartcontract_bytecode.txt", "r").read()

	account = w3.eth.accounts[0] #using first ganache account
	smartcontract= w3.eth.contract(abi=abi, bytecode=bytecode)

	transaction_hash=smartcontract.constructor().transact({'from': account})
	receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

	file=open("smartcontract_address.txt", "w")
	file.write(receipt.contractAddress)
	file.close()

	print ("Contract deployed at:" + receipt.contractAddress)