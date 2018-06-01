#!/bin/bash

# Asset 1 ================

#cp test-stuff/test_asset_1.json test_asset.json
# user 1 creates the asset
cp test-stuff/config1.json config.json
./DAWN_framework.py register test-stuff/test_asset_1.json
sleep 1
./DAWN_framework.py transfer dawn-user-1/this-is-asset-1 dawn-user-2
# change to user 2
cp test-stuff/config2.json config.json
# transfer to user 1
./DAWN_framework.py transfer dawn-user-1/this-is-asset-1 dawn-user-1
# change to user 1
cp test-stuff/config1.json config.json
# transfer to user 3
./DAWN_framework.py transfer dawn-user-1/this-is-asset-1 dawn-user-3
# change to user 3
cp test-stuff/config3.json config.json
# transfer to user 2
./DAWN_framework.py transfer dawn-user-1/this-is-asset-1 dawn-user-2


# Asset 2 ================

#cp test-stuff/test_asset_1.json test_asset.json
# user 2 creates the asset
cp test-stuff/config2.json config.json
./DAWN_framework.py register test-stuff/test_asset_2.json
sleep 1
./DAWN_framework.py transfer dawn-user-2/this-is-asset-2 dawn-user-1
# change to user 1
cp test-stuff/config1.json config.json
# transfer to user 1
./DAWN_framework.py transfer dawn-user-2/this-is-asset-2 dawn-user-3
# change to user 3
cp test-stuff/config3.json config.json
# transfer to user 2
./DAWN_framework.py transfer dawn-user-2/this-is-asset-2 dawn-user-2
# change to user 2
cp test-stuff/config2.json config.json
# transfer to user 3
./DAWN_framework.py transfer dawn-user-2/this-is-asset-2 dawn-user-3
# invalid transfer
./DAWN_framework.py transfer dawn-user-2/this-is-asset-2 dawn-user-1 



# Asset 3 ================

#cp test-stuff/test_asset_1.json test_asset.json
# user 2 tries to create the asset
cp test-stuff/config2.json config.json
./DAWN_framework.py register test-stuff/test_asset_3.json

# user 3 registers
cp test-stuff/config3.json config.json
./DAWN_framework.py register test-stuff/test_asset_3.json
sleep 1
./DAWN_framework.py transfer dawn-user-3/this-is-asset-3 dawn-user-1
# change to user 2
cp test-stuff/config2.json config.json
# try to transfer to user 3 (invalid)
./DAWN_framework.py transfer dawn-user-3/this-is-asset-3 dawn-user-3
