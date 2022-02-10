import datetime
import json
import hashlib
import time
from random import randint

global difficulty 
difficulty = 5 # To Control the puzzle hardness and intialize by 5

class Block_chain:
    def __init__(self):
        self.chain_of_blocks=[]
        self.creat_new_block(proof=1, previous_hash='0')
    
    def creat_new_block(self,proof,previous_hash):
        block = {'index':len(self.chain_of_blocks) + 1,'timestamp': str(datetime.datetime.now()),'proof': proof,
                'previous_hash': previous_hash,'transaction':'Alice pays Bob : ' + str(randint(1,500)) + ' LD'}
        self.chain_of_blocks.append(block)
        return block
    
    def previous_block(self):
        return self.chain_of_blocks[-1] # get the last block
    
    def proof_of_work(self,previous_nonce):
        nonce = 1 # the number that is being incremented inorder to generate the hash that suits our needs
        is_valid_proof = False

        while is_valid_proof is False:
            hash = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash[:difficulty] == difficulty*'0':
                is_valid_proof = True
            else:
                nonce += 1
        
        return nonce
    
    def calculate_hash_block(self,block):
        block_string_encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string_encoded).hexdigest()

blockchain = Block_chain()

def mining(): # add new block
    previous_block = blockchain.previous_block()
    previous_proof = previous_block['proof']
    new_proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.calculate_hash_block(previous_block)
    new_block = blockchain.creat_new_block(new_proof,previous_hash)

    data = {'type': 'user',
            'message':'A block is mined',
            'index': new_block['index'],
            'timestamp':new_block['timestamp'],
            'proof':new_block['proof'],
            'previous_hash':new_block['previous_hash'],
            'transaction':new_block['transaction']}
    
    print(data)

def attack(cpu_power): 
    #51% attack
    previous_block = blockchain.previous_block()
    previous_proof = previous_block['proof']
    user_new_proof = 1
    attacker_new_proof = 1

    while(1):
        user_iteration = 0
        attacker_iteration = 0
        
        #user
        while user_iteration < (100-cpu_power):
            hash = hashlib.sha256(str(user_new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash[:difficulty] == difficulty*'0':
                previous_hash = blockchain.calculate_hash_block(previous_block)
                block = blockchain.creat_new_block(user_new_proof,previous_hash)
                
                data = {'type': 'user',
                        'message':'A block is mined',
                        'index': block['index'],
                        'timestamp':block['timestamp'],
                        'proof':block['proof'],
                        'previous_hash':block['previous_hash'],
                        'transaction':block['transaction']}
                print(data)
                return
            else:
                user_new_proof += 1 
            
            user_iteration += 1
        
        #attacker
        while (attacker_iteration < cpu_power):
            hash = hashlib.sha256(str(attacker_new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash[:difficulty] == difficulty*'0':
                previous_hash = blockchain.calculate_hash_block(previous_block)
                block = blockchain.creat_new_block(attacker_new_proof,previous_hash)

                data = {'type': 'attacker',
                        'message':'A block is mined',
                        'index': block['index'],
                        'timestamp':block['timestamp'],
                        'proof':block['proof'],
                        'previous_hash':block['previous_hash'],
                        'transaction':block['transaction']}
                print(data)
                return 
            else:
                attacker_new_proof += 1
            
            attacker_iteration += 1

global time_of_mining_fn
time_of_mining_fn = 0
global total_time
total_time = 0
while(1):
    user_choice = input('''
        Please Enter the operation that you want: (M/A/D/V/E)
        M = Mining    A = making Attack    D = Display the block chain    E = Exit 
        ''')

    if(user_choice =='m' or user_choice == 'M'):
        t1 = time.time()
        mining()
        t2 = time.time()
        time_of_mining_fn = t2 - t1
        if(time_of_mining_fn > 1):
            #difficulty must not to be equal zero 
            if(difficulty != 1):
                difficulty -= 1
        else: 
            difficulty += 1
        print("Time of mining function = " , time_of_mining_fn)
        print("Difficulty = " , difficulty)
    
    elif(user_choice =='a' or user_choice == 'A'):
        attack_speed = int(input("Please Enter CPU Power(Attack speed): "))
        attack(attack_speed)
    
    elif(user_choice == 'd' or user_choice == 'D'):
        data = {'Block Chain': blockchain.chain_of_blocks,'Length of the chain':len(blockchain.chain_of_blocks)}
        print(data)

    else: 
        break

