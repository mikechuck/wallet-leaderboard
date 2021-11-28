import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
playersTable = dynamodb.Table('Players')
leaderboardsTable = dynamodb.Table("Leaderboards")

def lambda_handler(event, context):
    playerName = event.get("player_name")
    playerId = str(uuid.uuid4())
    leaderboardId = ''
    
    scanKwargs = {
        'FilterExpression': Key('player_count').between(0, 19)
    }
    leaderboardsResponse = leaderboardsTable.scan(**scanKwargs)
    
    if (leaderboardsResponse.get("Count") == 0):
        leaderboardId = str(uuid.uuid4())
        leaderboardsTable.put_item(
            Item={
                'leaderboard_id': leaderboardId,
                'player_count': 1,
                'players': [playerId]
            }
        )
    else:
        # Current Values
        leaderboard = leaderboardsResponse.get("Items")[0]
        leaderboardId = leaderboard.get("leaderboard_id")
        leaderboardPlayerCount = leaderboard.get("player_count")
        leaderboardPlayers = leaderboard.get("players")
        
        # New Values
        newPlayerCount = leaderboardPlayerCount + 1
        leaderboardPlayers.append(playerId)
        
        leaderboardsTable.update_item(
            Key={
                'leaderboard_id': leaderboardId
            },
            UpdateExpression="set player_count=:playerCount, players=:players",
            ExpressionAttributeValues={
                ':playerCount': newPlayerCount,
                ':players': leaderboardPlayers
            }
        )

    playersTable.put_item(
        Item={
            'player_id': playerId,
            'player_name': playerName,
            'leaderboard_id': leaderboardId,
            'score': 0
        }
    )
    
    return {
        "player_id": playerId,
        "leaderboard_id": leaderboardId
    }
