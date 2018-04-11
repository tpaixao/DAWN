#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import steembase
# from steembase.account import PasswordKey
import steem
from steem.utils import derive_permlink, resolve_identifier, fmt_time_string, keep_in_dict


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


dawn = DAWN(['5J8UmwoWoySnkjfdrR9BDLjPVAmsDfof6ovqXVZXCfM3ZYZxVSA']);

out = dawn.registerAsset('tiagotest','the title of my first asset','this is the data')
print(out)
out = dawn.transferAsset('tiagotest/the title of my first asset','tiagotest','tiagouser')
print(out)
