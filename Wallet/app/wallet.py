# goals
# create a new wallet
# add item to existing wallet
# retrieve an item from an existing wallet
# this should work for different versions of the mobile game client (playing v1 and v2 of the game)

import json
import uuid
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, request, jsonify

client = MongoClient("mongodb://localhost:27017")
# database is called "wallets"
# will have tables: PlayerWallets and WalletItems
db = client.Wallets
playersDB = db["Players"]

app = Flask(__name__)

def getUserFromAuth(header):
	# retrieving user information from auth
	return {
		"player_id": 123456
	}

# {
#    "_id" : ObjectId("5c6d73090c3d5054b766a76e"),
#    "EmployeeName" : "Larry",
#    "EmployeeSalary" : 9000,
#    "EmployeeDetails" : [
#       {
#          "EmployeeDOB" : ISODate("1990-01-21T00:00:00Z"),
#          "EmployeeDepartment" : "ComputerScience",
#          "EmployeeProject" : [
#             {
#                "Technology" : "C",
#                "Duration" : 6
#             },
#             {
#                "Technology" : "Java",
#                "Duration" : 7
#             }
#          ]
#       }
#    ]
# }

# {
# 	"_id": "5c6d73090c3d5054b766a76e",
# 	"PlayerName": "Test",
# 	"Wallets": [
# 		{
# 			"WalletName": "test",
# 			"Items": [
# 				{
# 					"ItemName": "testItem",
# 					""
# 				}
# 			]
# 		}
# 	]
# }

@app.route('/wallet', methods=['POST'])
def createWallet():
	authHeader = request.headers.get("Authorization")
	userInfo = getUserFromAuth(authHeader)
	eventBody = json.loads(request.data)
	# Input body params
	walletName = eventBody.get("wallet_name")

	# Create id for new wallet
	walletId = str(uuid.uuid4())

	if not walletName:
		return {"Message": "Missing fields: wallet_name"}, 400

	playersDB.update(
		{ 
			"_id": userInfo.get("player_id")
		}, 
		{
			"$push": {
				"Wallets": {
					"_id": walletId,
					"WalletName": walletName, 
					"Items": [] 
				}
			}
		}
	);

	return {"Message": "Success"}, 200


@app.route('/wallet/item', methods=['POST'])
def addItemToWallet():
	authHeader = request.headers.get("Authorization")
	userInfo = getUserFromAuth(authHeader)

	eventBody = json.loads(request.data)
	# Input body params
	walletId = eventBody.get("wallet_id")
	itemName = eventBody.get("item_name")
	itemPrice = eventBody.get("item_price") or ""
	itemColor = eventBody.get("item_color") or ""

	if not walletId or not itemName:
		return {"Message": "Missing fields: wallet_id or item_name"}, 400

	try:
		# playersDB.update(
		# 	{ 
		# 		"_id": userInfo.get("account_id"),
		# 		"Wallets._id": walletId
		# 	}, 
		# 	{
		# 		"$push": {
		# 			"Wallets.$.Items": {
		# 				"ItemName": itemName, 
		# 				"ItemPrice": itemPrice,
		# 				"ItemColor": itemColor  
		# 			}
		# 		}
		# 	}
		# );

		# updateResponse = playersDB.update(
		# 	{ 
		# 		"_id": userInfo.get("account_id"), 
		# 		"Wallets._id": walletId
		# 	},
		# 	{ "$push": 
		# 		{"Wallets.$[].Items": 
		# 			{
		# 				"ItemName": itemName,
		# 				"ItemPrice": itemPrice,
		# 				"ItemColor": itemColor
		# 			}
		# 		}
		# 	}
		# )

		returnItem = playersDB.find(
			{
				"Wallets._id": walletId
			}
		)


		print("returnItem:", returnItem)

		return {"Message": "Success"}, 200
	except:
		return {"Message": "Error"}, 500

@app.route('/wallet/<walletId>/item/<itemId>', methods=['GET'])
def getItemFromWallet(walletId, itemId):
	authHeader = request.headers.get("Authorization")
	userInfo = getUserFromAuth(authHeader)

	print("walletId:", walletId)
	print("itemId:", itemId)

	if not walletId or not itemId:
		return {"Message": "Missing fields: wallet_id or item_id"}, 400


	cur = playersDB.find(
		{
			"_id": userInfo.get("player_id"),
			"Wallets._id": walletId,
			"Wallets.Items._id": itemId
		}
	)
	# cur = playersDB.find(
	# 	{
	# 		"Wallets._id": walletId
	# 	}
	# )
	returnItem = {}
	for doc in cur:
		print("doc:", doc)
		returnItem = doc.get("Wallets")[0].get("Items")[0]
	# if (len(cur)):
	# 	returnItem = cur[0]
	# else:
	# 	return {"Message": "Item not found", "Item": ""}, 201

	# query = {"wallet_id": walletId, "item_id": itemId}
	# returnItem = walletItemsDB.find_one(query)

	return {"Message": "Success", "Item": returnItem}, 200

app.run(debug=True)