#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import steembase
# from steembase.account import PasswordKey
import steem
from steem.utils import derive_permlink, resolve_identifier, fmt_time_string, keep_in_dict
from steem.utils import construct_identifier

import sys
import sqlite3
import json
import time
from datetime import datetime,timedelta

# from pathlib import Path # for isfile()
import os.path



class DAWN:
    # client = steem.Steem(['https://testnet.steem.vc'],keys=['5J8UmwoWoySnkjfdrR9BDLjPVAmsDfof6ovqXVZXCfM3ZYZxVSA'])

    def __init__(self,steemd_nodes,posting_keys):
        self.posting_key = posting_keys
        # testnet
        if steemd_nodes == ['https://testnet.steem.vc']:
            steembase.chains.known_chains['STEEM'] = { 'chain_id': '79276aea5d4877d9a25892eaa01b0adf019d3e5cb12a97478df3298ccdd01673', 'prefix': 'STX', 'steem_symbol': 'STEEM', 'sbd_symbol': 'SBD', 'vests_symbol': 'VESTS' }
            self.client = steem.Steem(steemd_nodes,keys=[self.posting_key])
        else: # use standard nodes
            self.client = steem.Steem(keys = [self.posting_key])

    
    def registerAsset(self, author,title,data):
        # author, permlink = resolve_identifier(identifier)
        identifier = author + '/' + title;
        json_body = ["register_asset", {
                "permlink": identifier,
                "title": title,
                "author": author,
                "owner": author,
                "data": data}]

        return self.client.commit.custom_json(
            id="DAWN",
            json=json_body,
            required_posting_auths=[author]
        )
        pass

    def transferAsset(self, identifier,old_owner,new_owner):
        json_body = ["transfer_asset", {
                "permlink": identifier,
                "new_owner": new_owner}]
                
        return self.client.commit.custom_json(
            id="DAWN",
            json=json_body,
            required_posting_auths=[old_owner]
        )
        pass

#5309277 my genesis block
class DB:
    def __init__(self,filename):
        self.dbfilename = filename
        self.db = sqlite3.connect(self.dbfilename);
        self.db.row_factory = sqlite3.Row

    def closeDB(self):
        self.db.commit();
        self.db.close()
    
    def resetDB(self):
        cursor = self.db.cursor();
        cursor.execute('''drop table if exists assets;''');
        cursor.execute('''drop table if exists transfers;''');
        cursor.execute('''drop table if exists users;''');
        cursor.execute('''drop table if exists params;''');
        cursor.execute('''create table assets(
                asset_id integer primary key autoincrement,
                permlink text not null unique,
                genesis_block integer not null,
                tx_id text not null,
                author_id integer,
                owner_id integer,
                last_transfer_id integer,
                foreign key (last_transfer_id) references transfers(transfer_id),
                foreign key (author_id) references users(user_id),
                foreign key (owner_id) references users(user_id)
                );
                ''');
        cursor.execute('''create table transfers(
                transfer_id integer primary key autoincrement,
                block_number int not null,
                tx_id text not null,
                previous_transfer int,
                asset_id integer,
                previous_owner_id integer,
                new_owner_id integer,
                foreign key (asset_id) references assets(asset_id),
                foreign key (previous_owner_id) references users(user_id),
                foreign key (new_owner_id) references users(user_id)
                );
                ''');
        cursor.execute('''create table users(
                user_id integer primary key autoincrement,
                username text not null unique);
                ''');
        cursor.execute('''create table if not exists params(
                key text not null unique primary key,
                value text not null unique);
                ''');
        cursor.execute('''insert into params(key,value) values(?,?)''',('last_parsed_block','0'))

        self.db.commit();
        pass

    def updateLastParsedBlock(self,last_block):
        cursor = self.db.cursor();
        cursor.execute('''update params set value = ? where key = 'last_parsed_block' ''',(last_block,))
        self.db.commit();

    def getLastParsedBlock(self):
        cursor = self.db.cursor();
        cursor.execute('''select value from params where key = last_parsed_block''')
        last_parsed_block = cursor.fetchone();
        return last_parsed_block;


    def addAsset(self,permlink,block,tx_id,author):
        cursor = self.db.cursor();
        #check if the author already exists
        # cursor.execute('''select user_id from users where username = ?''',(author,));
        # user = cursor.fetchone()
        user = self.getUserID(author)
        if user is None:
            # user does not exist (yet)
            cursor.execute('''insert into users(username) values(?)''',(author,))
            author_id = cursor.lastrowid
        else:
            #user exists
            author_id = user
            
        #add the asset
        try:
            cursor.execute('''insert into assets(permlink,genesis_block,tx_id,author_id,owner_id,last_transfer_id) 
                    values(?,?,?,?,null)
                    ''', (permlink,block,tx_id,author_id,author_id) );
            self.db.commit() 
        except sqlite3.IntegrityError:
            print('Record already exists')
        pass

    def transferAsset(self,assetPermlink,block,tx_id,new_owner):
        cursor = self.db.cursor();
        
        # Check that new_owner exists or add it
        userID = self.getUserID(new_owner)
        if userID is None:
            # user does not exist (yet)
            cursor.execute('''insert into users(username) values(?)''',(new_owner,))
            new_owner_id = cursor.lastrowid
        else:
            #user exists
            new_owner_id = userID

        #update asset table

        ### get asset (previous_owner_id)
        asset_id = self.getAssetID(assetPermlink)
        if asset_id is None:
            return "Asset not found"
        else: # get previous owner
            cursor.execute('''select * from assets where asset_id = ?''',(asset_id,))
            asset = cursor.fetchone();
            previous_owner_id = asset['owner_id']
            last_transfer_id = asset['last_transfer_id']

            #add transfer to transfers table
            cursor.execute('''insert into transfers(block_number,tx_id,previous_transfer,asset_id,previous_owner_id,new_owner_id) values(?,?,?,?,?);''',(block,tx_id,last_transfer_id,asset_id,previous_owner_id,new_owner_id,))
            transfer_id=cursor.lastrowid

            # update asset
            cursor.execute('''update assets set owner_id = ?, last_transfer_id = ? where asset_id = ?;''',(new_owner_id,transfer_id,asset_id))
            self.db.commit()
        pass
    
    def getUserID(self,username):
        cursor = self.db.cursor();
        cursor.execute('''select user_id from users where username = ?''',(username,));
        userID = cursor.fetchone();
        if userID is None:
            return None
        else:
            return userID[0]
        pass


    def listAssets(self,username):
        user_id = self.getUserID(username);
        if user_id is None:
            return '{ "error": "user not on database" }';

        cursor = self.db.cursor();
        cursor.execute('''select * from assets where owner_id = ?''',(user_id,));
        # if json_output:
        return json.dumps( [dict(ix) for ix in cursor.fetchall()] ) 
        # else:
            # for row in cursor:
                # # print("no json")
                # return row['permlink']
            # pass

    def listUserOwned(self,username):
        user_id = self.getUserID(username);
        if user_id is None:
            return '{ "error": "user not on database" }';

        cursor = self.db.cursor();

        cursor.execute('''select asset_id,permlink,genesis_block,username from assets join users on users.user_id=assets.author_id where assets.owner_id=?''',(user_id,));
        # if json_output:
        return json.dumps( [dict(ix) for ix in cursor.fetchall()] ) 

    def listUserCreated(self,username):
        user_id = self.getUserID(username);
        if user_id is None:
            return '{ "error": "user not on database" }';

        cursor = self.db.cursor();

        cursor.execute('''select asset_id,permlink,genesis_block,username from assets join users on users.user_id=assets.author_id where assets.author=?''',(user_id,));
        # if json_output:
        return json.dumps( [dict(ix) for ix in cursor.fetchall()] ) 

    def getUsername(self,userid):
        print(userid)
        cursor = self.db.cursor();
        cursor.execute('''select username from users where user_id = ?''',(userid,));
        user = cursor.fetchone();
        if user is None:
            return None
        else:
            return user['username']
        pass

    def getAssetID(self,permlink):
        cursor = self.db.cursor();
        cursor.execute('''select asset_id from assets where permlink = ?''',(permlink,));
        assetID = cursor.fetchone();
        if assetID is None:
            return None
        else:
            return assetID[0]

    def getAssetOwner(self,permlink):
        cursor = self.db.cursor();
        cursor.execute('''select owner_id from assets where permlink = ?''',(permlink,));
        owner_id = cursor.fetchone();
        if owner_id is None:
            return None
        owner_name = self.getUsername(owner_id[0])
        return owner_name

    def listAssetHistory(self,asset_permlink):
        asset_id = self.getAssetID(asset_permlink);
        if asset_id is None:
            return '{"error": "asset not found on DB"}'
        else:
            #get asset
            cursor1 = self.db.cursor();
            cursor1.execute('''select * from assets where asset_id = ?''',(asset_id,));
            asset = cursor1.fetchone();

            cursor = self.db.cursor()
            cursor.execute('''select * from transfers where asset_id = ?;''',(asset_id,))

            # TODO: SHOULD OUTPUT JSON
            # print("Asset # {0} created by {1} in block # {2}".format(asset_id,self.getUsername(asset['author_id']),asset['genesis_block']))
            # for transfer in cursor:
                # print("{0} transfered to {1} in block# {2}".format(self.getUsername(transfer['previous_owner_id']),self.getUsername(transfer['new_owner_id']),transfer['block_number']))

            asset_dict = {'author': self.getUsername(asset['author_id']), 'genesis_block': asset['genesis_block'] }
            # asset_dict['author'] = self.getUsername(asset['author_id']) 
            # asset_dict['genesis_block']=asset['genesis_block']

            transfers = []
            for transfer in cursor:
                transfer_dict={'previous_owner': self.getUsername(transfer['previous_owner_id']), 
                        'next_owner': self.getUsername(transfer['new_owner_id'])
                        }
                transfers.append(transfer_dict)
            return json.dumps((asset_dict,transfers))

        # pass

    def deleteFromBlock(self,block_number):
        cursor = self.db.cursor();
        cursor.execute('''delete from transfers where block_number >= ? ''',(block_number,))
        cursor.execute('''delete from assets where genesis_block >= ? ''',(block_number,))
        self.db.commit();
        self.updateLastParsedBlock(block_number-1)
        return block_number -1
        pass

class DAWNBlockchainParser:

    def __init__(self, steemd_nodes,dbname):
        self.steem_client = steem.Steem(steemd_nodes) #only need read-access
        # self.dbname = dbname
        self.db = DB(dbname)

    # returns None if it is not aDAWN op
    # else returns the op dict
    def get_DAWN_op(self,op):
        if op[0] != 'custom_json':
            print('no custom_json')
            return None
        # if json_obj[0] not in  ['register_asset','transfer_asset']:
        if op[1]['id'] != 'DAWN':
            print('no DAWN ops')
            return None
        else:
            # json_obj = json.loads(op[1]['json']);
            return op[1]
        pass

# {'required_auths': [], 'required_posting_auths': ['tiagotest'], 'id': 'DAWN', 'json': '["register_asset", {"permlink": "tiagotest/the-title-of-my-first-asset", "title": "the-title-of-my-first-asset", "author": "tiagotest", "owner": "tiagotest", "data": "this is the data"}]'}
    
    # should return either true or false
    def verify_op(self,op_dict):
        json_obj = json.loads(op_dict['json'])
        # print(json.dumps(json_obj))
        # print(op_dict)
        print('verifying')
        if json_obj[0] == 'register_asset':
            print('verifying register')
            return self.verify_register_op(op_dict,json_obj)
        elif json_obj[0] == 'transfer_asset':
            print('verifying transfer')
            return self.verify_transfer_op(op_dict,json_obj)
        else: #no DAWN op that we know
            return False

    # should return either true or false
    def verify_transfer_op(self,op_dict,json_obj):
        # json_obj = json.loads[op_dict['json']);
        # if json_obj[0] == 'transfer_asset': #re verify?
        #is the sender the current owner?
        sender = op_dict['required_posting_auths'][0]
        asset_owner = self.db.getAssetOwner(json_obj[1]['permlink']);
        if sender == asset_owner:
            return True
        else:
            print('sender not owner')
            return False
    pass
    
    # should return either true or false
    def verify_register_op(self,op_dict,json_obj):
        # json_obj = json.loads(op_dict['json']);
        # is the permlink OK (owner/title)?
        sender = op_dict['required_posting_auths'][0]
        # print(json_obj['permlink'])
        author,title = resolve_identifier(json_obj[1]['permlink'])
        if sender != author:
            print('sender not author')
            return False
        #does an asset with the same permlink already exist?
        asset_id = self.db.getAssetID(json_obj[1]['permlink'])
        if asset_id is None:
            return True
        return False
    pass

    def execute_op(self,op_dict, reference):
        json_obj = json.loads(op_dict['json'])

        if json_obj[0] == 'register_asset':
            print('Found new asset')
            return self.register_asset(json_obj[1],reference);
        elif json_obj[0] == 'transfer_asset':
            print('Found new transfer')
            return self.transfer_asset(json_obj[1],reference);
        else: #no DAWN op that we know
            return False
        pass

    def register_asset(self,json_op,reference):
        #add obj to DB
        permlink = json_op['permlink']
        block_number = reference[0]
        tx_id = reference[1]
        # need to include trxid
        author,title = resolve_identifier(permlink);
        self.db.addAsset(permlink,block_number,tx_id,author);
        print('Adding '.format(permlink))
        return True

    def transfer_asset(self,json_op,reference):
        #add transfer_order to DB
        permlink = json_op['permlink']
        new_owner = json_op['new_owner']
        block_number = reference[0]
        tx_id = reference[1]
        self.db.transferAsset(permlink,block_number,tx_id,new_owner);
        print('tranfering asset'.format(permlink))
        return True

    def replay(self,block_number=0):

        if block_number == 0:
            # replay normally (from the last parsed block
            last_parsed_block = self.db.getLastParsedBlock()
        else: # replay from some previous block
            last_parsed_block = self.db.deleteFromBlock(block_number) # this updates the last_parsed_block in the database

        print("last parsed block: {0}".format(last_parsed_block))
        
        # while True:
            # last block in the blockchain
            # try:
        last_irr_block = self.steem_client.last_irreversible_block_num
        print("last irr block: {0}".format(last_irr_block))
            # except TypeError:
                # pass
            # else: 
                # break
        # MAIN LOOP 
        while True:
            if last_parsed_block + 1 < last_irr_block:
                # Get a block
                print("Getting block #{0}".format(last_parsed_block+1))
                block = self.steem_client.get_block(last_parsed_block+1);
                
                trxs = block['transactions'];
                trx_ids  = block['transaction_ids']
                if len(trxs) == 0:
                    print("block #{0}:empty".format(last_parsed_block +1))
                    time.sleep(1)
                    last_parsed_block = last_parsed_block +1;
                    continue

                this_block = last_parsed_block +1;

                for trx,trx_id in zip(trxs,trx_ids):
                    for op in trx['operations']:
                        op_dict = self.get_DAWN_op(op)

                        # not DAWN op 
                        if op_dict is None: 
                            print('DAWN dict empty')
                            continue
                        #DAWN_op
                        # op_dict['block'] = this_block;
                        # op_dict['transaction_id']= trx_id;
                        # ref = str(this_block)+"/"+str(trx_id)
                        ref = [this_block,trx_id]

                        if self.verify_op(op_dict):
                            # execute  op
                            # print(ref)
                            self.execute_op(op_dict,ref)
                    pass

                last_parsed_block = this_block;
                pass
            else: # reached the last block; get a new one
                try:
                    last_irr_block = self.steem_client.last_irreversible_block_num
                except TypeError:
                    print('Problem getting a new block')
                    pass
            pass



# CLI functions

def register(asset_fname):
    # load asset file
    asset_file= open(asset_fname);
    asset = json.load(asset_file)
    print(asset)
    if 'author' in asset and 'title' in asset and 'data' in asset:
        author = asset['author']
        title = asset['title'].replace(" ","-")
        data = asset['data']
    else:
        print("Required field in asset not found")
        return False
    # send it to the blockchain
    dawn = DAWN(config['steem_node'],config['postingKey'])
    last_block = dawn.client.last_irreversible_block_num
    print("Last block is: {0}".format(last_block))
    out = dawn.registerAsset(author,title,data);
    print(out)
    pass

def transfer(asset_permlink,new_owner):
    # get 
    old_owner = config['username']
    dawn = DAWN(config['steem_node'],config['postingKey'])
    last_block = dawn.client.last_irreversible_block_num
    print("Last block is: {0}".format(last_block))
    out = dawn.transferAsset(asset_permlink,old_owner,new_owner)
    print(out)
    pass

def list_user_assets(user):
    db = DB(config['db_name']);
    print(db.listAssets(user))
    pass

def list_asset_history(asset_permlink):
    db = DB(config['db_name']);
    # print(db.listAssets(user))
    print(db.listAssetHistory(asset_permlink))
    pass

def printHelp(executable_name):
    print("Usage: {0} command options. Check config.json for your credentials.\n Available options:".format(executable_name))
    # REGISTER
    print("register: registers a new asset in the blockchain")
    print("args: \n ASSET_FILE: JSON file describing the asset. Fields: author, title, data")
    # TRANSFER
    print("transfer: transfers one of your assets to a new owner. ")
    print("args: \n asset_permlink: owner/title, new_owner")
    # LIST USER
    print("list-user: list all assets of a particular user. ")
    print("args: \n username: self-explanatory.")
    # LIST ASSET
    print("list-asset: list ownership history of an asset. ")
    print("args: \n asset: asset_permlink.")
    # RESET
    print("reset: resets the DB")
    # REBUILD-DB    
    print("rebuild-db: Rebuilds the database from a particular block")
    print("args: \n block_number: the block number to rebuild from. Default value is 0. This will run until interrupted.")
    pass

if __name__ == '__main__':
    # db = DB('test.db')
    # db.resetDB();
    # db.addAsset('tiago/asset1',1,"tiago");
    # db.addAsset('tiago/asset2',2,"tiago");
    # db.addAsset('mariana/asset_2',2,"mariana");
    # db.transferAsset('tiago/asset1',3,'mariana')
    # db.transferAsset('tiago/asset1',5,'tiago')
    # db.transferAsset('tiago/asset1',7,'mariana')

    # print(db.listAssets('tiago'))

    # db.listAssetHistory('tiago/asset1')

    #['https://testnet.steem.vc']
    # dawn = DAWN(['https://testnet.steem.vc'], ['5J8UmwoWoySnkjfdrR9BDLjPVAmsDfof6ovqXVZXCfM3ZYZxVSA']);

    # out = dawn.registerAsset('tiagotest','the title of my first asset','this is the data')
    # print(out)
    # out = dawn.transferAsset('tiagotest/the title of my first asset','tiagotest','tiagouser')
    # print(out)


    # if len(sys.argv) > 1 :
        # startup_behavior = sys.argv[1]
    # else :
        # startup_behavior = 'normal'
    
    # dawn = DAWN(['https://testnet.steem.vc'], ['5J8UmwoWoySnkjfdrR9BDLjPVAmsDfof6ovqXVZXCfM3ZYZxVSA']);

    # print("current block is: {0}".format(dawn.client.last_irreversible_block_num))

    # out = dawn.registerAsset('tiagotest','the-title-of-my-first-asset','this is the data')
    # print(out)
    # out = dawn.transferAsset('tiagotest/the-title-of-my-first-asset','tiagotest','tiagouser')
    # print(out)

    global config

    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        config = {'username': '','postingKey': '', 'db_name': '', 'steem_node': '','first_block': ''}
        with open('config.json','w') as config_file:
            json.dump(config,config_file)
        raise FileNotFoundError("Could not read config.json. Please populate it with relevant details." )
        

    try:
        username = config['username']
        postingKey = config['postingKey']
        db_name = config['db_name']
        steem_node = config['steem_node']
        first_block = config['first_block']
    except KeyError as er:
        raise KeyError('Could not read required key from config.json.')

    if len(sys.argv) > 1:
        if sys.argv[1] == 'register':#args: asset_file
            # asset_file = Path(argv[2])
            # if asset_file.is_file():
            if os.path.isfile(sys.argv[2]):
                register(sys.argv[2])
            else:
                print("Asset file {0} not found".format(sys.argv[2]))
            pass
        elif sys.argv[1] == 'transfer': #args: asset, new_owner
            asset_permlink = sys.argv[2];
            new_owner = sys.argv[3];
            #sanity check (poor - need to do better inside)
            if asset_permlink == '' or new_owner == '':
                printHelp(sys.argv[0]);
            else:
                transfer(asset_permlink,new_owner)
            pass
        elif sys.argv[1] == 'list-user':#args: username
            list_user_assets(sys.argv[2])
            pass
        elif sys.argv[1] == 'list-asset':#args: username
            list_asset_history(sys.argv[2])
            pass
        elif sys.argv[1] == 'reset':
            db = DB(db_name)
            db.resetDB()
        elif sys.argv[1] == 'rebuild-db':#args: from_block
            if len(sys.argv) > 2:
                from_block = int(sys.argv[2])
            else:
                from_block = int(first_block)
            parser = DAWNBlockchainParser(steem_node,db_name)
            # parser.db.deleteFromBlock(from_block)
            parser.replay(from_block)
            
        else:
            print('command {0} not known'.format(sys.argv[1]))
            printHelp(sys.argv[0])
    else:
        # print('command {0} not known'.format(sys.argv[1]))
        printHelp(sys.argv[0])



