using UnityEngine;

// Models
public class PlayerModel
{
	public string player_id;
	public string player_name;
	public string score;
	public string rank;
}
public class CreateUserInput
{
	public string player_name;
}
public class CreateUserResponse
{
	public string player_id;
	public string leaderboard_id;
}
public class GetLeaderboardResponse
{
	public string leaderboard_id;
	public string player_count;
	public string[] players;
	public PlayerModel[] players_info;
}
public class UpdateScoreInput
{
	public string player_id;
	public string score;
}
public class UpdateScoreResponse
{
	public string player_id;
	public string success;
}

// Global variables
public class StaticVar : MonoBehaviour
{
	public static bool gameStart = false;
	public static bool gameOver = false;
	public static int gameTimer;
	public static string playerName;
	public static string playerId;
	public static string leaderboardId;
	public static int playerScore = 0;
	public static PlayerModel[] leaderboardPlayers;
	public static string apiUrl = "https://hdpw9n3dz9.execute-api.us-east-2.amazonaws.com/v1";

	public static void resetGame()
	{
		gameStart = false;
		gameOver = false;
		playerScore = 0;
	}
}