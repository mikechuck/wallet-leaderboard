using UnityEngine;
using UnityEngine.Networking;
using System;
using System.Collections;
using Newtonsoft.Json;

public class Services: ScriptableObject
{
	static string dataString;
	static object data;
	// Declare callbacks for each service:
	public delegate void CreatePlayerCallback();
	public delegate void GetLeaderboardCallback();
	public delegate void UpdateScoreCallback();

	// Service methods:
    public void createPlayer(MonoBehaviour mono, CreatePlayerCallback callback)
	{
		mono.StartCoroutine(createPlayerService((UnityWebRequest req) =>
		{
			CreateUserResponse userResponse = JsonConvert.DeserializeObject<CreateUserResponse>(req.downloadHandler.text);
			StaticVar.playerId = userResponse.player_id;
			StaticVar.leaderboardId = userResponse.leaderboard_id;
			callback();
		}));
	}
	public void getLeaderboard(MonoBehaviour mono, GetLeaderboardCallback callback)
	{
		mono.StartCoroutine(getLeaderboardService((UnityWebRequest req) =>
		{
			GetLeaderboardResponse leaderboardResponse = JsonConvert.DeserializeObject<GetLeaderboardResponse>(req.downloadHandler.text);
			StaticVar.leaderboardPlayers = leaderboardResponse.players_info;
			callback();
		}));
	}
	public void updatePlayerScore(MonoBehaviour mono)
	{
		mono.StartCoroutine(updateScoreService());
	}


	// Helper services:
	static IEnumerator createPlayerService(Action<UnityWebRequest> callback)
	{
		CreateUserInput playerInfo = new CreateUserInput();
		playerInfo.player_name = StaticVar.playerName;
		string json = JsonConvert.SerializeObject(playerInfo, Formatting.Indented);

		var uwr = new UnityWebRequest(StaticVar.apiUrl + "/users", "POST");
		byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
		uwr.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
		uwr.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
		uwr.SetRequestHeader("Content-Type", "application/json");
		yield return uwr.SendWebRequest();
		callback(uwr);
	}
	static IEnumerator getLeaderboardService(Action<UnityWebRequest> callback)
	{
		var uwr = new UnityWebRequest(StaticVar.apiUrl + "/leaderboards/" + StaticVar.leaderboardId, "GET");
		uwr.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
		yield return uwr.SendWebRequest();
		callback(uwr);
	}
	static IEnumerator updateScoreService()
	{
		UpdateScoreInput updateInfo = new UpdateScoreInput();
		updateInfo.player_id = StaticVar.playerId;
		updateInfo.score = StaticVar.playerScore.ToString();
		string json = JsonConvert.SerializeObject(updateInfo, Formatting.Indented);

		var uwr = new UnityWebRequest(StaticVar.apiUrl + "/users/score", "POST");
		byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);
		uwr.uploadHandler = (UploadHandler)new UploadHandlerRaw(jsonToSend);
		uwr.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
		uwr.SetRequestHeader("Content-Type", "application/json");
		yield return uwr.SendWebRequest();
	}
}
