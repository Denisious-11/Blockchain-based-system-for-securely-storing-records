import random
import sys
import base64
import json
import os
import pandas as pd
from web3 import Web3
from solcx import compile_standard
# from ipfs import upload as up1
import ipfshttpclient
import solcx
#solcx.install_solc()

compiled_sol = compile_standard({
     "language": "Solidity",
     "sources": {
         "phb.sol": {
             "content": '''
                 pragma solidity >=0.4.0 <0.8.16;
               

                contract PHB {

                    struct User
                    {       

                        int S_id;
                        string P_address;
                        string Username;
                        string Email;
                        string Password;
                        string Phone;
                    }

                    User []users;

                    function addUser(int S_id,string memory P_address,string memory Username,string memory Email,string memory Password,string memory Phone) public
                    {
                        User memory e
                            =User(S_id,
                                    P_address,
                                    Username,
                                    Email,
                                    Password,
                                    Phone);
                        users.push(e);
                    }

                    function getUser(int S_id) public view returns(
                            string memory,
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<users.length;i++)
                        {
                            User memory e
                                =users[i];
                            
                            if(e.S_id==S_id)
                            {
                                return(e.P_address,
                                    e.Username,
                                    e.Email,
                                    e.Password,
                                    e.Phone
                                   
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found"
                               );
                    }

                    function getUserCount() public view returns(uint256)
                    {
                        return(users.length);
                    }


                     struct Records
                    {
       
                        int record_id;
                        string record_name;
                        string access;
                        string date;
                        string time;
                        string hash_value;
                    }

                    Records []recs;

                    function addRecords(int record_id,string memory record_name,string memory access,string memory date,string memory time,string memory hash_value) public
                    {
                        Records memory e
                            =Records(record_id,
                                    record_name,
                                    access,
                                    date,
                                    time,
                                    hash_value);
                        recs.push(e);
                    }


                    function getRecords(int record_id) public view returns(
                            string memory,
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<recs.length;i++)
                        {
                            Records memory e
                                =recs[i];
                                 
                            
                            if(e.record_id==record_id)
                            {
                                return(e.record_name,
                                    e.access,
                                    e.date,
                                    e.time,
                                    e.hash_value
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found");
                    }

                    function getRecordsCount() public view returns(uint256)
                    {
                        return(recs.length);
                    }

                }

               '''
         }
     },
     "settings":
         {
             "outputSelection": {
                 "*": {
                     "*": [
                         "metadata", "evm.bytecode"
                         , "evm.bytecode.sourceMap"
                     ]
                 }
             }
         }
 })


# web3.py instance



def verify_key(adr1,key,amount):
    try:
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.enable_unaudited_features()
        nonce = web3.eth.getTransactionCount(adr1)

        tx = {
            'nonce': nonce,
            'to': adr1,
            'value': web3.toWei(1, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei(amount, 'gwei'),
        }
        signed_tx = web3.eth.account.signTransaction(tx,key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        #print(web3.toHex(tx_hash))
        return "Yes"
    except Exception as e:
        print(e)  
        return "No"  



def create_contract():
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    # get bytecode
    bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    pb = w3.eth.contract(abi=abi, bytecode=bytecode)

    # # Submit the transaction that deploys the contract
    tx_hash = pb.constructor().transact()

    # # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print("tx_receipt.contractAddress: ",tx_receipt.contractAddress)
    f=open('contract_address.txt','w')
    f.write(tx_receipt.contractAddress)
    f.close()


def add_user1(S_id,P_address,Username,Email,Password,Phone):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    tx_hash = p1.functions.addUser(S_id,P_address,Username,Email,Password,Phone).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    #print(tx_hash) 
    print(tx_receipt)

    

def get_user(id1):
    id1=int(id1)
    p1=get_contract()
    store = p1.functions.getUser(id1).call()
    print("store : ",store)
    return store

def get_users():
    c=get_user_count()
    c_names=['P_address','Username','Email','Password','Phone']
    dict1={}
    for i in range(1,c+1):
        d=get_user(i)
        dict2={}
        for j in range(len(c_names)):
            # print("j : ",j)
            # print(type(j))
            # if(j==4):
            #     print("entered")
            #     dict2[c_names[j]]=d[6]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1        

def get_user_count():
    p1=get_contract()
    store = p1.functions.getUserCount().call()
    print(store)
    return int(store)


def get_record(id1):
    id1=int(id1)
    p1=get_contract()
    print(id1,'============')
    store = p1.functions.getRecords(id1).call()
    print(store)
    return store

def get_records():
    c=get_records_count()
    c_names=['record_name','access','date','time','hash_value']
    dict1={}
    for i in range(1,c+1):
        d=get_record(i)
        dict2={}
        for j in range(len(c_names)):
            # if j==5:
            #     dict2[c_names[j]]=d[7]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1     


def get_records_count():
    p1=get_contract()
    store = p1.functions.getRecordsCount().call()
    print(store)
    return int(store)
    

def add_records(record_id,file_name,username,current_date,time,hash_value):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    tx_hash = p1.functions.addRecords(record_id,file_name,username,current_date,time,hash_value).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print(tx_hash)




def get_contract():
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]#'0x3529A6ee990639C32bEe5F841a9649cdd0c6e0FD'
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    return p1



def verify_adr(s):
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected(),"##########")
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    adrs = w3.eth.accounts
    print(adrs)

    if s in adrs:
        return True
    else:
        return False  



if __name__=="__main__":
    # pass

    create_contract()




