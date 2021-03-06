import json
import uuid
from pymongo import MongoClient
from flask import request, Blueprint
from ..common import authenticateUser

client = MongoClient("mongodb://localhost:27017")
db = client.Wallets
playersCollection = db["Players"]
walletsCollection = db["Wallets"]

# Create blueprint for this api version
api = Blueprint('v1', __name__)

@api.route('/wallets', methods=['POST'])
def createWallet():
	# Validate authorization
	playerId = authenticateUser(request.headers).get("player_id")
	if (not playerId):
		return {"Message": "Missing authorization"}, 403

	# Input body params
	eventBody = json.loads(request.data)
	walletName = eventBody.get("wallet_name")
	walletId = str(uuid.uuid4())

	# Validate required input fields
	if not walletName:
		return {"Message": "Missing fields: wallet_name"}, 400

	try:
		# Add id to Players.Wallets
		playersCollection.update_one(
			{ "_id": playerId }, 
			{ "$push": {"Wallets": walletId} }
		);

		# Create new Wallet document in Wallets collection (with empty Items array)
		walletsCollection.insert_one(
			{
				"_id": walletId,
				"PlayerId": playerId,
				"WalletName": "New Wallet",
				"Items": []
			}
		)

		return walletId, 200
	except:
		return {"Message": "Internal Error"}, 500


@api.route('/wallets/items', methods=['POST'])
def addItemToWallet():
	# Validate authorizations
	playerId = authenticateUser(request.headers).get("player_id")
	if (not playerId):
		return {"Message": "Missing authorization"}, 403

	# Input body params
	eventBody = json.loads(request.data)
	walletId = eventBody.get("wallet_id")
	itemName = eventBody.get("item_name")
	itemPrice = eventBody.get("item_price") or ""
	itemColor = eventBody.get("item_color") or ""

	# Validate required input fields
	if not walletId or not itemName:
		return {"Message": "Missing fields: wallet_id or item_name"}, 400

	try:
		# Create id for new item
		itemId = str(uuid.uuid4())

		# Add new item to Wallet.Items array
		walletsCollection.update_one(
			{ 
				"_id": walletId,
				"PlayerId": playerId
			}, 
			{
				"$push": {
					"Items": {
						"_id": itemId,
						"ItemName": itemName, 
						"ItemPrice": itemPrice,
						"ItemColor": itemColor  
					}
				}
			}
		);

		return itemId, 200
	except:
		return {"Message": "Internal Error"}, 500


@api.route('/wallets/<walletId>/items/<itemId>', methods=['GET'])
def getItemFromWallet(walletId, itemId):
	# Validate authorization
	playerId = authenticateUser(request.headers).get("player_id")
	if (not playerId):
		return {"Message": "Missing authorization"}, 403

	# Validate input fields
	if not walletId or not itemId:
		return {"Message": "Missing fields: wallet_id or item_id"}, 400
	
	try:
		# Query for the itemId, and filter by matching on only that item
		cur = walletsCollection.find(
			{
				"PlayerId": playerId,
				"Items._id": itemId
			}, 
			{
				"Items": {
					"$elemMatch": {
						"_id": itemId
					}
				}
			}
		);

		# Get item from returned document
		returnItem = {}
		for doc in cur:
			returnItem = doc.get("Items")[0]

		return returnItem, 200
	except:
		return {"Message": "Internal Error"}, 500
