#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import steembase
# from steembase.account import PasswordKey
import steem
from steem.utils import derive_permlink, resolve_identifier, fmt_time_string, keep_in_dict

import sys
import sqlite3


# testnet
steembase.chains.known_chains['STEEM'] = { 'chain_id': '79276aea5d4877d9a25892eaa01b0adf019d3e5cb12a97478df3298ccdd01673', 'prefix': 'STX', 'steem_symbol': 'STEEM', 'sbd_symbol': 'SBD', 'vests_symbol': 'VESTS' }

class DAWN:
    # client = steem.Steem(['https://testnet.steem.vc'],keys=['5J8UmwoWoySnkjfdrR9BDLjPVAmsDfof6ovqXVZXCfM3ZYZxVSA'])

    def __init__(self,posting_keys):
        self.posting_key = posting_keys
        self.client = steem.Steem(['https://testnet.steem.vc'],keys=self.posting_key)
    
    #these classes 
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

    def closeDB():
        self.db.close()
    
    def resetDB(self):
        cursor = self.db.cursor();
        cursor.execute('''drop table if exists assets;''');
        cursor.execute('''drop table if exists transfers;''');
        cursor.execute('''drop table if exists users;''');
        cursor.execute('''create table assets(
                asset_id integer primary key autoincrement,
                permlink text not null unique,
                genesis_block integer not null,
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

        self.db.commit();
        pass

    def addAsset(self,permlink,block,author):
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
            cursor.execute('''insert into assets(permlink,genesis_block,author_id,owner_id,last_transfer_id) 
                    values(?,?,?,?,null)
                    ''', (permlink,block,author_id,author_id) );
            self.db.commit() 
        except sqlite3.IntegrityError:
            print('Record already exists')
        pass

    def transferAsset(self,assetPermlink,block,new_owner):
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
            cursor.execute('''insert into transfers(block_number,previous_transfer,asset_id,previous_owner_id,new_owner_id) values(?,?,?,?,?);''',(block,last_transfer_id,asset_id,previous_owner_id,new_owner_id,))
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

    def getUsername(self,userid):
        cursor = self.db.cursor();
        cursor.execute('''select username from users where user_id = ?''',(userid,));
        user = cursor.fetchone();
        if user is None:
            return None
        else:
            return user[0]
        pass

    def listAssets(self,username):
        user_id = self.getUserID(username);
        if user_id is None:
            return "user not on the database";

        cursor = self.db.cursor();
        cursor.execute('''select * from assets where owner_id = ?''',(user_id,));
        for row in cursor:
            print(row['permlink'])
        pass

    def getAssetID(self,permlink):
        cursor = self.db.cursor();
        cursor.execute('''select asset_id from assets where permlink = ?''',(permlink,));
        assetID = cursor.fetchone();
        return assetID[0]

    def listAssetHistory(self,asset_permlink):
        asset_id = self.getAssetID(asset_permlink);
        if asset_id is None:
            return "asset not found"
        else:
            #get asset
            cursor1 = self.db.cursor();
            cursor1.execute('''select * from assets where asset_id = ?''',(asset_id,));
            asset = cursor1.fetchone();

            cursor = self.db.cursor()
            cursor.execute('''select * from transfers where asset_id = ?;''',(asset_id,))

            # print("asset # {2}".format(asset_id,self.getUsername(asset['author_id']),self.getUsername(asset['genesis_block'])))
            # print("genesis block # {0}".format(asset['genesis_block']))
            print("Asset # {0} created by {1} in block # {2}".format(asset_id,self.getUsername(asset['author_id']),asset['genesis_block']))
            for transfer in cursor:
                print("{0} transfered to {1} in block# {2}".format(self.getUsername(transfer['previous_owner_id']),self.getUsername(transfer['new_owner_id']),transfer['block_number']))
        # pass

class DAWNBlockchainParser:

    def __init__(self, dbname):
        self.client = steem.Steem(['https://testnet.steem.vc'])
        self.dbname = dbname


    def getDawnTransactions(self,block):
        pass

    def verifyTransfer(self):
        pass


# dawn = DAWN(['5J8UmwoWoySnkjfdrR9BDLjPVAmsDfof6ovqXVZXCfM3ZYZxVSA']);

# out = dawn.registerAsset('tiagotest','the title of my first asset','this is the data')
# print(out)
# out = dawn.transferAsset('tiagotest/the title of my first asset','tiagotest','tiagouser')
# print(out)



# if len(sys.argv) > 1 :
    # startup_behavior = sys.argv[1]
# else :
    # startup_behavior = 'normal'

db = DB('test.db')
db.resetDB();
db.addAsset('tiago/asset1',1,"tiago");
db.addAsset('tiago/asset2',2,"tiago");
db.addAsset('mariana/asset_2',2,"mariana");
db.transferAsset('tiago/asset1',3,'mariana')
db.transferAsset('tiago/asset1',5,'tiago')


db.listAssets('tiago')

db.listAssetHistory('tiago/asset1')


