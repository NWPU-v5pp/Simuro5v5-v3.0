/************************************************************************
 * GUI_Replay
 * 1.比赛界面，包括esc进入菜单
 * 2.比赛菜单，包括回到比赛、进入回放、退出
************************************************************************/

using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using Simuro5v5;
using Event = Simuro5v5.EventSystem.Event;

public class GUI_Play : MonoBehaviour {
    
    bool menu_open = false;
    bool GUI_on_Camera = true;

    // 以下对象设为静态，防止之后注册事件函数后，闭包造成重载场景后的空引用
    static Popup Popup { get; set; }

    static MatchMain matchMain { get; set; }
    static MatchInfo matchInfo { get { return MatchMain.GlobalMatchInfo; } }

    static GameObject SceneObj { get; set; }

    static GameObject CanvasObj { get; set; }
    static GameObject MenuObj { get; set; }
    static GameObject StartObj { get; set; }
    static GameObject ResumeObj { get; set; }
    static GameObject ReplayObj { get; set; }
    static GameObject ExitObj { get; set; }
    static GameObject MenuBack { get; set; }

    static GameObject BlueScoreObj { get; set; }
    static GameObject YellowScoreObj { get; set; }
    static GameObject TimeObj { get; set; }
    static Text BlueScoreText { get; set; }
    static Text YellowScoreText { get; set; }
    static Text TimeText { get; set; }
    static Text RefereeLogText { get; set; }

    void Start()
    {
        InitObjects();

        SetBlueScoreText(matchInfo.Score.BlueScore);
        SetYellowScoreText(matchInfo.Score.BlueScore);

        OpenMenu();

        StartObj.GetComponent<Button>().onClick.AddListener(delegate ()
        {
            matchMain.LoadStrategy();
            matchMain.StartMatch();
            matchMain.StartRound();
        });
        ResumeObj.GetComponent<Button>().onClick.AddListener(delegate
        {
            CloseMenu();
            matchMain.ResumeRound();
        });
        ReplayObj.GetComponent<Button>().onClick.AddListener(delegate
        {
            // 总拍数作为回放结束拍数
            PlayerPrefs.SetInt("step_end", matchInfo.PlayTime);
            SceneManager.LoadScene("GameScene_Replay");
        });

        ReplayObj.GetComponent<Button>().enabled = false;
        ExitObj.GetComponent<Button>().onClick.AddListener(delegate
        {
            SceneManager.LoadScene("MainScene");
        });

        Event.Register(Event.EventType0.RoundStart, delegate ()
        {
            Popup.Show("Round", "Round start", 1500);
        });
        Event.Register(Event.EventType0.RoundResume, delegate ()
        {
            Popup.Show("Round", "Round resume", 1500);
        });
        Event.Register(Event.EventType0.RoundPause, delegate ()
        {
            Popup.Show("Round", "Round pause", 1500);
        });
        Event.Register(Event.EventType0.RoundStop, delegate ()
        {
            Popup.Show("Round", "Round stop", 1500);
        });
        Event.Register(Event.EventType1.LogUpdate, SetRefereeInfo);
    }

    void InitObjects()
    {
        matchMain = GetComponent<MatchMain>();
        Popup = GameObject.Find("/Canvas/Popup").GetComponent<Popup>();

        SceneObj = GameObject.Find("MatchScene");

        CanvasObj = GameObject.Find("Canvas");
        MenuObj = GameObject.Find("/Canvas/Menu");
        StartObj = GameObject.Find("/Canvas/Menu/Btn/Start");
        ResumeObj = GameObject.Find("/Canvas/Menu/Btn/Resume");
        ReplayObj = GameObject.Find("/Canvas/Menu/Btn/Replay");
        ExitObj = GameObject.Find("/Canvas/Menu/Btn/Exit");
        MenuBack = GameObject.Find("/Canvas/Menu/Background");

        BlueScoreObj = GameObject.Find("/Canvas/Score/Blue");
        YellowScoreObj = GameObject.Find("/Canvas/Score/Yellow");
        BlueScoreText = BlueScoreObj.GetComponent<Text>();
        YellowScoreText = YellowScoreObj.GetComponent<Text>();

        TimeObj = GameObject.Find("/Canvas/Time");
        TimeText = TimeObj.GetComponent<Text>();
        RefereeLogText = GameObject.Find("/Canvas/Log/Referee").GetComponent<Text>();
    }

    void Update()
    {
        var cameras = GameObject.Find("MainCamera");
        if (cameras.GetComponent<Camera>().enabled == true && GUI_on_Camera == false)
        {
            Open_GUI_Camera();
            GUI_on_Camera = true;
        }
        if (cameras.GetComponent<Camera>().enabled == false && GUI_on_Camera == true)
        {
            Close_GUI_Camera();
            GUI_on_Camera = false;
        }
        if (cameras.GetComponent<Camera>().enabled == true)
        {
        }

        if (Input.GetMouseButtonDown(1))
        {
            // right clicked, pause and toggle menu
            if (menu_open)
            {
                CloseMenu();
            }
            else
            {
                matchMain.PauseRound();
                OpenMenu();
            }
        }
        if (Input.GetMouseButtonDown(0))
        {
            // left clicked, pause
            if (!menu_open)
            {
                if (matchMain.StartedMatch && matchMain.InRound)
                {
                    if (matchMain.PausedRound)
                    {
                        matchMain.ResumeRound();
                    }
                    else
                    {
                        matchMain.PauseRound();
                    }
                }
            }
        }

        UpdateTimeText();
        UpdateScoreText();
    }

    void OpenMenu()
    {
        StartObj.SetActive(true);
        ResumeObj.SetActive(true);
        ReplayObj.SetActive(true);
        ExitObj.SetActive(true);
        MenuBack.SetActive(true);
        menu_open = true;
    }

    void CloseMenu()
    {
        StartObj.SetActive(false);
        ResumeObj.SetActive(false);
        ReplayObj.SetActive(false);
        ExitObj.SetActive(false);
        MenuBack.SetActive(false);
        menu_open = false;
    }

    void SetBlueScoreText(int i)
    {
        BlueScoreText.text = i.ToString();
    }

    void SetYellowScoreText(int i)
    {
        YellowScoreText.text = i.ToString();
    }

    void SetTimeText(int i)
    {
        TimeText.text = i.ToString();
    }

    void UpdateTimeText()
    {
        SetTimeText(matchInfo.PlayTime);
    }

    void UpdateScoreText()
    {
        BlueScoreText.text = matchInfo.Score.BlueScore.ToString();
        BlueScoreText.text = matchInfo.Score.YellowScore.ToString();
    }

    void SetRefereeInfo(object obj)
    {
        var info = obj as string;
        RefereeLogText.text = info;
    }

    void Open_GUI_Camera()
    {
        GameObject obj0 = GameObject.Find("Canvas");
        if (obj0 == null)
        {
            Debug.Log("No Canvas Object.");
        }
        else
        {
            Debug.Log("Canvas Object.");
        }

        GameObject obj1 = obj0.transform.Find("ys").gameObject;
        if (obj1 == null)
        {
            Debug.Log("No ys Object.");
        }
        else
        {
            Debug.Log("ys Object.");
        }
        obj1.SetActive(true);

        GameObject obj2 = obj0.transform.Find("bs").gameObject;
        if (obj2 == null)
        {
            Debug.Log("No bs Object.");
        }
        else
        {
            Debug.Log("bs Object.");
        }
        obj2.SetActive(true);

        GameObject obj3 = obj0.transform.Find("referee").gameObject;
        if (obj3 == null)
        {
            Debug.Log("No referee Object.");
        }
        else
        {
            Debug.Log("referee Object.");
        }
        obj3.SetActive(true);

        GameObject obj4 = obj0.transform.Find("time").gameObject;
        if (obj4 == null)
        {
            Debug.Log("No time Object.");
        }
        else
        {
            Debug.Log("time Object.");
        }
        obj4.SetActive(true);

        GameObject obj5 = obj0.transform.Find("esc").gameObject;
        if (obj5 == null)
        {
            Debug.Log("No esc Object.");
        }
        else
        {
            Debug.Log("esc Object.");
        }
        obj5.SetActive(true);
    }

    void Close_GUI_Camera()
    {
        GameObject obj1 = GameObject.Find("ys");
        if (obj1 == null)
        {
            Debug.Log("No ys Object.");
        }
        else
        {
            Debug.Log("ys Object.");
        }
        obj1.SetActive(false);

        GameObject obj2 = GameObject.Find("bs");
        if (obj2 == null)
        {
            Debug.Log("No bs Object.");
        }
        else
        {
            Debug.Log("bs Object.");
        }
        obj2.SetActive(false);

        GameObject obj3 = GameObject.Find("referee");
        if (obj3 == null)
        {
            Debug.Log("No referee Object.");
        }
        else
        {
            Debug.Log("referee Object.");
        }
        obj3.SetActive(false);

        GameObject obj4 = GameObject.Find("time");
        if (obj4 == null)
        {
            Debug.Log("No time Object.");
        }
        else
        {
            Debug.Log("time Object.");
        }
        obj4.SetActive(false);

        GameObject obj5 = GameObject.Find("esc");
        if (obj5 == null)
        {
            Debug.Log("No esc Object.");
        }
        else
        {
            Debug.Log("esc Object.");
        }
        obj5.SetActive(false);
    }
}
