using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LeaderboardController : MonoBehaviour
{
	public GameObject leaderboardRow;
	public GameObject leaderboardContainer;
	public List<GameObject> leaderboardRows;
	public Services services;
    // Start is called before the first frame update
    void Start()
    {
		services = ScriptableObject.CreateInstance<Services>();
		// Spawn the inital leaderboard values
		spawnLeaderboardRows();

		// Update the leaderboard every 3 seconds
		InvokeRepeating("UpdateLeaderboard", 2.0f, 2.0f);
    }

	public void spawnLeaderboardRows()
	{
		// First delete all existing rows
		for (int i = 0; i < leaderboardRows.Count; i++) {
			Destroy(leaderboardRows[i]);
		}

		// Then add the new ones
		PlayerModel[] players = StaticVar.leaderboardPlayers;

        for(int i = 0; i < players.Length; i++) {
			string playerName = players[i].player_name;
			string playerScore = players[i].score;
			int rank = i + 1;
			int yPos = -(rank * 25);

			GameObject newLeaderboardRow = Instantiate(leaderboardRow, new Vector3(0, yPos, 0), Quaternion.identity) as GameObject;
			newLeaderboardRow.transform.SetParent(leaderboardContainer.transform, false);
			leaderboardRows.Add(newLeaderboardRow);

			Text[] rowTexts = newLeaderboardRow.GetComponentsInChildren<Text> ();
			rowTexts[0].text = rank.ToString();
			rowTexts[1].text = playerName;
			rowTexts[2].text = playerScore;
		}
	}

	public void UpdateLeaderboard()
	{
		Services.GetLeaderboardCallback callback = getLeaderboardCallback;
		services.getLeaderboard(this, callback);
	}

	public void getLeaderboardCallback()
	{
		spawnLeaderboardRows();
	}
}
