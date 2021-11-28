using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    // Start is called before the first frame update
	public bool gameStarted = false;
	public int totalTime;
	public int numGoodCoins;
	public int numBadCoins;
	public GameObject goodCoin;
	public GameObject badCoin;
	public GameObject player;
	public GameObject startMenu;
	public GameObject gameOverMenu;
	public Text timeDisplay;
    void Start()
    {
        StaticVar.gameTimer = totalTime;
		// Invoke a repeater to count the time
		InvokeRepeating("UpdateTimeDisplay", 0f, 1.0f);

		// Set menu statuses
		startMenu.SetActive(true);
		gameOverMenu.SetActive(false);
    }
	void Update()
	{
		if (StaticVar.gameStart && !gameStarted)
		{
			gameStarted = true;
			// Spawn player
			Instantiate(player, new Vector3(0, 0, 0), Quaternion.identity);
			for (int i = 0; i < numGoodCoins; i++) {
				spawnCoin("Green");
			}

			for (int i = 0; i < numBadCoins; i++) {
				spawnCoin("Red");
			}
		}

		// If time is up, Stop clock and despawn any particles as well as player
		if (StaticVar.gameTimer == 0) {
			GameOver();
		}

		// Check for game quit key
		if (Input.GetKeyDown(KeyCode.Escape))
        {
			// On quit, reset global values for next play
			StaticVar.resetGame();
            SceneManager.LoadScene("Menu");
        }
	}

	public void spawnCoin(string coinType)
	{
		// Spawn coins
		Vector2 screenBounds = Camera.main.ScreenToWorldPoint(new Vector2(Screen.width, Screen.height));
		float xMin = (-screenBounds.x + 0.5f);
		float xMax = (screenBounds.x - 0.5f);
		float yMin = (-screenBounds.y + 0.5f);
		float yMax = (screenBounds.y - 0.5f);
		// Generate good coin
		float xrand = Random.Range(xMin, xMax);
		float yrand = Random.Range(yMin, yMax);
		if (coinType == "Green") {
			Instantiate(goodCoin, new Vector3(xrand,yrand, 0), Quaternion.identity);
		} else if (coinType == "Red") {
			Instantiate(badCoin, new Vector3(xrand,yrand, 0), Quaternion.identity);
		}
	}

	public void UpdateTimeDisplay()
	{
		timeDisplay.text = StaticVar.gameTimer.ToString(); 
		if (StaticVar.gameStart && StaticVar.gameTimer > 0) {
			StaticVar.gameTimer--;
		}
	}

	public void StartGame()
	{
		StaticVar.gameStart = true;
		startMenu.SetActive(false);
	}

	public void GameOver()
	{
		StaticVar.gameOver = true;
		gameOverMenu.SetActive(true);
	}
}
