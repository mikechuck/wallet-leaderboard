using UnityEngine;
using UnityEngine.SceneManagement;

public class Loading : MonoBehaviour
{
	public Services services;
    // Start is called before the first frame update
    public void Start()
    {
		services = ScriptableObject.CreateInstance<Services>();

		// Create the player
		Services.CreatePlayerCallback callback = createPlayerCallback;
		services.createPlayer(this, callback);
    }

	public void createPlayerCallback()
	{
		// Get resulting leaderboard information
		Services.GetLeaderboardCallback callback = getLeaderboardCallback;
		services.getLeaderboard(this, callback);		
	}

	public void getLeaderboardCallback()
	{
		// Load Game scene
		SceneManager.LoadScene("Game");
	}
}
