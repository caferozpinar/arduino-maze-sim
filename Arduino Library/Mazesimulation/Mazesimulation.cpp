#include "Arduino.h"
#include "Mazesimulation.h"

int GetMazeSize(char maze[20])
{
  int size_x;
  int size_y;
  byte empty = 0;
  if (maze == "size_x" || maze == "x_size" || maze == "x")
  {
    while (!Serial.available());
    empty = Serial.readString().toInt();
    Serial.print("size_x");
    while (!Serial.available());
    size_x = Serial.readString().toInt();
    Serial.print("size_x_done");
    return size_x;
  }
  if (maze == "size_y" || maze == "y_size" || maze == "y")
  {
    while (!Serial.available());
    empty = Serial.readString().toInt();
    Serial.print("size_y");
    while (!Serial.available());
    size_y = Serial.readString().toInt();
    Serial.print("size_y_done");
    return size_y;
  }
}

void SetSimulationPrint(int baudrate)
{
  Serial.begin(baudrate);
  Serial.setTimeout(1);
}

void SimulationCalibrate()
{
  byte empty = 0;
  while (!Serial.available());
  empty = Serial.readString().toInt();
  Serial.print("turnRight");
  while (!Serial.available());
  empty = Serial.readString().toInt();
  Serial.print("turnRight");
  while (!Serial.available());
  empty = Serial.readString().toInt();
  Serial.print("turnRight");
  while (!Serial.available());
  empty = Serial.readString().toInt();
  Serial.print("turnRight");
  while (!Serial.available());
  empty = Serial.readString().toInt();
  Serial.print("setRotationRight");
}

void Printf(char request[255])
{
  byte empty = 0;
  while (!Serial.available());
  empty = Serial.readString().toInt();
  Serial.print(request);
}
void MoveSimulation(char rotation_axis_maze[20])
{
  byte empty = 0;
  if (rotation_axis_maze == "right" || rotation_axis_maze == "RIGHT" || rotation_axis_maze == "Right")
  {
    while (!Serial.available());
    empty = Serial.readString().toInt();
    Serial.print("turnRight");
  }
  if (rotation_axis_maze == "left" || rotation_axis_maze == "LEFT" || rotation_axis_maze == "Left")
  {
    while (!Serial.available());
    empty = Serial.readString().toInt();
    Serial.print("turnLeft");
  }
  if (rotation_axis_maze == "back" || rotation_axis_maze == "BACK" || rotation_axis_maze == "Back")
  {
    while (!Serial.available());
    empty = Serial.readString().toInt();
    Serial.print("turnBack");
  }
  if (rotation_axis_maze == "go" || rotation_axis_maze == "GO" || rotation_axis_maze == "Go")
  {
    while (!Serial.available());
    empty = Serial.readString().toInt();
    Serial.print("go");
  }

}

int SensorValue(char rotation_axis_maze[20])
{
  byte empty = 0;
  int right;
  int left;
  int forward;
  while (!Serial.available());
  empty = Serial.readString().toInt();
  Serial.print("getVal");
  while (!Serial.available());
  int val = Serial.readString().toInt();
  if (val != 35 && val != 25)
  {
    left = val % 2;
    val = (val / 2);
    forward = val % 2;
    val = (val / 2);
    right = val % 2;
  }

  if (rotation_axis_maze == "right" || rotation_axis_maze == "RIGHT" || rotation_axis_maze == "Right" || rotation_axis_maze == "r" || rotation_axis_maze == "R")
  {
    return right;
  }
  if (rotation_axis_maze == "forward" || rotation_axis_maze == "FORWARD" || rotation_axis_maze == "Forward" || rotation_axis_maze == "f" || rotation_axis_maze == "F")
  {
    return forward;
  }
  if (rotation_axis_maze == "left" || rotation_axis_maze == "LEFT" || rotation_axis_maze == "Left" || rotation_axis_maze == "l" || rotation_axis_maze == "L")
  {
    return left;
  }
}
