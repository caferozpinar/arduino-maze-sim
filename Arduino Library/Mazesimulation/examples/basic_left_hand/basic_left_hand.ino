#include <Mazesimulation.h>
int swc;
int rotation = 'r';
int sim_car_x = 0;
int sim_car_y = 0;
byte map_array[60][60];

void pathFind()
{
  if(SensorValue("left") == 0)
  {
    MoveSimulation("left");
    MoveSimulation("go");
  }
  else if(SensorValue("forward") == 0)
  {
    MoveSimulation("go");
  }
  else if(SensorValue("right") == 0)
  {
    MoveSimulation("right");
    MoveSimulation("go");
  }
  else
  {
    MoveSimulation("back");
  }
  
}

void setMapArraySize()
{

  int size_x = 0;
  int size_y = 0;

  size_x = GetMazeSize("x");
  size_y = GetMazeSize("y");

  //we dont now start point
  int x = (size_x * 2);
  int y = (size_y * 2);

  for (int k = 0; k < y; k++)
  {
    for (int j = 0; j < x; j++)
    {
      if (k == (y / 2) && j == (x / 2) )
      {
        map_array[j][k] = 25;
        sim_car_x = j;
        sim_car_y = k;
        continue;
      }
      else
      {
        map_array[j][k] = 0;
      }
    }

  }
}

void setup() 
{
  Serial.begin(115200);
  Serial.setTimeout(1);
  randomSeed(analogRead(A0));
  swc = 1;
}
void loop() 
{

  switch (swc)
  {
    case 1:
      setMapArraySize();
      SimulationCalibrate();
      swc = 2;
      break;
    case 2:
      pathFind();
      break;

  }
}
