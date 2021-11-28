import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
playersTable = dynamodb.Table('Players')

def lambda_handler(event, context):
    playerId = event.get("player_id")
    playerScore = event.get("score")
    
    playersTable.update_item(
        Key={
            'player_id': playerId
        },
        UpdateExpression="set score=:score",
        ExpressionAttributeValues={
            ':score': playerScore,
        }
    )
    
    return {
        'player_id': playerId,
        'success': True
    }
