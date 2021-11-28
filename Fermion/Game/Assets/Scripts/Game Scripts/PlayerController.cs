using UnityEngine;

public class PlayerController : MonoBehaviour
{
	float horizontal;
	float vertical;
	public int flySpeed = 10;
	int playerScore;
	public Services services;
	public GameManager gameManager;

    // Start is called before the first frame update
    void Start()
    {
		services = ScriptableObject.CreateInstance<Services>();
		playerScore = 0;
    }

    // Update is called once per frame
    void Update()
    {	
		//Only allow movement after game has started
		if (!StaticVar.gameOver) {
			float horizontalInput = Input.GetAxisRaw("Horizontal");
			float verticalInput = Input.GetAxisRaw("Vertical");
			float xPos = transform.position.x;
			float yPos =  transform.position.y;

			Vector2 screenBounds = Camera.main.ScreenToWorldPoint(new Vector2(Screen.width, Screen.height));
			Vector2 screenOrigo = Camera.main.ScreenToWorldPoint(Vector2.zero);

			// Check all the boundaries
			// Horizontal check
			bool leftCheck = horizontalInput == -1 && xPos > -screenBounds.x + 0.5f;
			bool rightCheck = horizontalInput == 1 && xPos < screenBounds.x - 0.5f;
			if (leftCheck || rightCheck) {
				transform.position = transform.position + new Vector3(horizontalInput * flySpeed * Time.deltaTime, 0, 0);
			}

			// Vertical check
			bool topCheck = verticalInput == -1 && yPos > -screenBounds.y + 0.5f;
			bool bottomCheck = verticalInput == 1 && yPos < screenBounds.y - 0.5f;
			if (topCheck || bottomCheck) {
				transform.position = transform.position + new Vector3(0, verticalInput * flySpeed * Time.deltaTime, 0);
			}
		}
    }

	void OnCollisionEnter2D(Collision2D col)
	{
		GameObject coinGameObject = col.gameObject;
		string tag = coinGameObject.tag;
		
		if (tag == "Green" || tag == "Red") {
			// Send to graveyard to play sound, then destroy
			coinGameObject.transform.localScale = new Vector3(-100, -100, 0);
			AudioSource destroySound = coinGameObject.GetComponent<AudioSource>();
			destroySound.Play();
			Destroy(coinGameObject, 1f);

			// Change score based on coin type
			if (tag == "Green") {
				playerScore++;
			} else if (tag == "Red") {
				if (StaticVar.playerScore > 0) {
					playerScore--;
				}
			}
			// Update Score
			StaticVar.playerScore = playerScore;
			services.updatePlayerScore(this);
			gameManager.spawnCoin(tag);
		}
	}
}
