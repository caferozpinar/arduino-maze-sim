#ifndef Mazesimulation_h
#define Mazesimulation_h
#include "Arduino.h"

int GetMazeSize(char maze[20]);
void SetSimulationPrint(int baudrate);
void SimulationCalibrate();
void Printf(char request[255]);
void MoveSimulation(char rotation[20]);
int SensorValue(char rotation[20]);

#endif
