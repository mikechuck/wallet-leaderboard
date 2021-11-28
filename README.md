# wallet-leaderboard

## Contents

- Leaderboard
- Wallet
- Fermion

## Leaderboard

The Leaderboard folder contains system designs and diagrams for implementing a leaderboard system for a mobile game.

## Wallet

The Wallet folder contains services for a item-collection system for a mobile game.  
This project uses Python and Flask to run the services, with MongoDB as the database layer.

Command to start the services:
```bash
python run.py
```
After the services are running, you will need to start a local MongoDB database with collections ```Player``` and ```Wallets```.  

Then, insert the default Player document manually:

```Python
{
    "PlayerId": "123456",
    "PlayerName": "Test User",
    "Wallets": []
}
```

After the services are running locally, you can test them by uploading the collection in the Wallet/postman folder into Postman.

## Fermion

Merging the Leaderboard and Wallet designs together, I created a game in Unity called Fermion that you can play [here](https://play.unity.com/mg/other/v1-f7qzzt).
The Fermion folder contains a folder for the Game itself, and a folder for the services.

The services for Fermion are hosted on AWS, and utlize API Gateway, Lambda, and DynamoDB.  
Note: the backend for this game was not built with scalability and security in mind!  

**Game rules**:
- You have 30 seconds to collide with as many particles as you can
- Colliding with green particles will increase your score
- Colliding with red particles will decrease your score
- Try to finish at the top of the leaderboard!



