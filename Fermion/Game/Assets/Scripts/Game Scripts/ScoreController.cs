
using UnityEngine;
using UnityEngine.UI;

public class ScoreController : MonoBehaviour
{
	public Text textObject;
    // Update is called once per frame
    void Update()
    {
        textObject.text = StaticVar.playerScore.ToString();
    }
}
