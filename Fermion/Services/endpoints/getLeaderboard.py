import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
playersTable = dynamodb.Table('Players')
leaderboardsTable = dynamodb.Table("Leaderboards")

def lambda_handler(event, context):
    
    leaderboardId = event.get("pathParameters").get("proxy")
    
    response = leaderboardsTable.query(
        KeyConditionExpression=Key('leaderboard_id').eq(str(leaderboardId))
    )
    leaderboard = response.get("Items")[0]
    players = leaderboard.get("players")

    playersInfo = []
    
    for playerId in players:
        playerResponse = playersTable.query(
            KeyConditionExpression=Key('player_id').eq(str(playerId))
        )
        player = playerResponse.get("Items")[0]
        playersInfo.append({
            "player_id": player.get("player_id"),
            "player_name": player.get("player_name"),
            "score": int(player.get("score"))
        })
        
    playersInfo.sort(key=sortArray)
    leaderboard["players_info"] = playersInfo

    return {
        'statusCode': 200,
        'headers': {"Access-Control-Allow-Origin": '*'},
        'body': json.dumps(leaderboard, cls=DecimalEncoder)
    }
    {
}
class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)
    
def sortArray(e):
  return -int(e["score"])