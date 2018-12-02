# DAWN - Digital Asset Worldwide Network

A protocol (and implementation) for tracking ownership of digital assets on the Steem blockchain.

## Roadmap

* QT Client 
The idea is to have fully integrated Qt-based desktop client that syncs with the blockchain and allows one to view the state of the sub-chain (see all assets, history, etc) as well as submit orders (transfers/ register assets). The advantage is that users can verify the state of the subchain independently (at least to the extent that the node they connect to is honest). 

* Javascript Client 
		This is to be used together with the dawn-server as to serve as a local(js)-only client that reads information from the dawn-server which is located elsewhere. I aim to build it using riotJS. The advantage is that it is easier to access (just a web page somewhere, should probably be able to be used locally even). The disadvantage is that it relies on a third-party service (that serves the DB) which could potentially be malicious.

* Use merkle proofs to prove inclusion of all and particular transactions.
* 

## The protocol

Two basic operations are allowed: the *registration* of a new asset and the *transfer* of ownership of this asset. These operations are implemented as messages broadcast on the STEEM blockchain, which are cryptographically verified to come from a specific user. This is critical for the trust in this system.

1. **Registration** will simply broadcast a new asset and will be only accepted in the registry if the sender of the message is the stated author of the asset. (this prevents forgeries).

1. **Transfer** of ownership will broadcast that the item with ID number will be transfered to a different user (this user may or may not exist, creating the possibility of "destroying" items). This message will only be accepted if the sender of the message is the current owner of the asset.

An asset description follows the schema:
```json
	{
		"permlink": <author_username>/<asset_title>,	
		"author": <author_username>,	
		"data": <arbitrary_data>
	}
```

Orders are submited as `custom_json` transfers with the `DAWN` id.
In order to *register* an asset the `json_body` should have the structure:

```python
["register_asset", {
	"permlink": identifier,
		"title": title,
		"author": author,
		"owner": author,
		"data": data}]
]
```

In order to *transfer* an asset the `json_body` should have the structure:

```python
["transfer_asset", {
	"permlink": identifier,
	"new_owner": new_owner}
]
```

### Verification
Verification is done only when replaying the full history of transactions as it requires knowledge of all previous transactions (just like any other blockchain).  These transactions are considered valid if:

`register_asset`: 
1. No asset with the same permkink should exist already.
1. sender of the transaction should be the author (as stated in the permlink).

`transfer_asset`: 
1. asset with the given permlink exists.
1. sender of the transaction is the current_owner of the asset


## Implementation

### ```DAWN_framework.py``` 

The file `DAWN_framework.py` contains 3 python classes:

* `DAWN` class 
The `DAWN` class is simply a wrapper for the `commit.custom_json` function in the Steem-Python library. It submits orders to the blockchain formatted to fit the protocol. 

* `DAWNBlockchainParser` 
The `DAWNBlockchainParser` class reads the Blockchain, looking for DAWN orders. It verifies their validity, as per the protocol, and stores the data in a database (see below).

* `DB` class
The `DB` class is an utiity class that wraps a SQLite3 database. It constains functions to update and to read from the database.

`DAWN_framework.py` also serves as a command-line interface to the framework. Invoke it without parameters to see the options.


### `dawn-server.py`
This file instantiates a web service (API) that allows querying the database for the parsed results.
So far, the endpoints are:

`/api/user/<username>`: returns JSON data containing all the assets owned by the user
`/api/user/<username>/<asset_title>`: returns JSON data containing the ownership history of the asset with permlink `<username>/<title>`

## Requirements

This implementation depends on:

* python 3.6 (because steem-python requires it)
* steem-python ( pip install steem )
* Flask is needed for the API (pip install flask)

## Why Steem?

Steem is a blockchain that uses Delegated Proof of Stake (DPOS) as its consensus mechanism and specialized in storing JSON documents. Initially, this blockchain was tailored towards social media applications for which mass adoption was a necessity. As such, it benefits from a number of features that makes it extremely easy to onboard new users. 
Most importantly, it features:

* No transaction fees
* fast block times
* human-readable account addresses
* advanced account management
