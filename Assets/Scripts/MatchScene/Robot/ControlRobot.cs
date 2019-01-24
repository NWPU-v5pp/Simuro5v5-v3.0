using UnityEngine;
using Simuro5v5;

public class ControlRobot : MonoBehaviour
{
    WheelCollider leftWheel;
    WheelCollider rightWheel;

    // 动力属性
    float velocityLeft;         // 左轮速，标量，因为方向和rotation一致
    float velocityRight;        // 右轮速，标量，因为方向和rotation一致

    Wheel wheel;
    Rigidbody rb;

    // 数据记录
    Vector3 pos0 = new Vector3(102.5f, 0.0f, 70.0f);       // 记录初始位置
    int PlayTime;

    bool IsBlue(int i)
    {
        return transform.name == ("Blue" + i);
    }

    void Start()
    {
        Time.fixedDeltaTime = Const.Zeit;

        rb = GetComponent<Rigidbody>();
        rb.maxAngularVelocity = (Const.Robot.maxAngularVelocity * Mathf.Deg2Rad);

        leftWheel = transform.Find("WheelL").GetComponent<WheelCollider>();
        rightWheel = transform.Find("WheelR").GetComponent<WheelCollider>();

        PlayTime = 0;
    }

    void FixedUpdate()
    {
        //if (IsBlue(0))
        {
            //PositionController();

            leftWheel.motorTorque = GetMotor(velocityLeft);
            rightWheel.motorTorque = GetMotor(velocityRight);

            leftWheel.brakeTorque = velocityLeft == 0 ? Const.Wheel.brakeTorque : 0;
            rightWheel.brakeTorque = velocityRight == 0 ? Const.Wheel.brakeTorque : 0;

            PlayTime++;
        }
    }

    float GetMotor(float power)
    {
        float motor = 0;
        float velocity = rb.velocity.magnitude;
        float k = 1.0f / 600.0f;
        float offset = 2.0f;

        motor = (power - velocity) / ((velocity + offset) * k);
        //Debug.Log("PlayTime=" + PlayTime + " power=" + power + " velocity=" + velocity + " motor=" + motor + " name=" + transform.name);

        return motor;
    }

    void PositionController()
    {
        if (IsBlue(0))
        {
            if (Input.GetKeyUp("q"))
            {
                rb.position = pos0;
            }
            if (rb.position.z <= -70)
            {
                rb.position = pos0;
            }
        }
    }

    public void SetWheelVelocity(Wheel ws)
    {
        velocityLeft = (float)ws.left;
        velocityRight = (float)ws.right;

        if (velocityLeft * velocityRight >= 0)
        {
            if (velocityLeft < velocityRight)
            {
                velocityLeft = InceraseVmin(velocityRight, velocityLeft);
            }
            else
            {
                velocityRight = InceraseVmin(velocityLeft, velocityRight);
            }
        }
    }

    float InceraseVmin(float Vmax, float Vmin)
    {
        //Vmin = Vmin + (Vmax - Vmin) * (Vmax - Vmin) * 0.004f;

        return Vmin;
    }

    public void SetPlacement(Robot robot)
    {
        // 设置刚体的坐标，会在下一拍才会显示到屏幕上，应该直接设置物体的
        Vector3 pos;
        Quaternion rot = new Quaternion();
        pos.x = robot.pos.x;
        pos.z = robot.pos.y;
        pos.y = robot.pos.z;
        transform.position = pos;
        //rb.position = pos;
        //rot.y = (float)robot.rotation;
        //rot.y.FormatOld().FormatUnity2Old();
        rot.eulerAngles = new Vector3
        {
            x = 0,
            y = ((float)robot.rotation).FormatOld().FormatOld2Unity(),
            z = 0,
        };
        //rot.eulerAngles.y.FormatOld().FormatOld2Unity();
        transform.rotation = rot;
        //rb.rotation = rot;
    }

    public void SetStill()
    {
        wheel.left = 0;
        wheel.right = 0;
        rb.Sleep();
        rb.WakeUp();
    }
}