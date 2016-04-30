/*
Program: actuate_hand.ino
Created By: Josh Chan, Justin Fuerth, Matthew Snell
Last Modified: April 2nd, 2014
Description: Program to actuate a DC motor connected to a prosthetic hand.
Receives actuation commnad from a Python script.
*/

// uses pins 3 and 5 for PWM
int motorPin1 = 3;
int motorPin2 = 5;

//iterator
int i = 0;

//state of the hand
//0 = open
//1 = closed
int state = 0;

void setup(){
	// Open serial connection.
	Serial.begin(9600);

	//set pins as outputs
	pinMode(motorPin1,OUTPUT);
	pinMode(motorPin2,OUTPUT);

	//write two messages to Python. The first is to connect to the serial port,
	//the second is to let Python know that the hand is ready to be actuated.
	Serial.write('1');
	Serial.write('1');
}

void loop(){

	//poll the serial port to see if a message has been written to the buffer from Python
	//this also removes the message from the buffer, letting Python know that the Arduino
	//is now in the busy state. Python will not send any messages during this time.
	if(Serial.available() > 0 && Serial.read()=='1'){

		//when a message is sent, check the state of the hand
		if (state == 0)
		{

			//if the hand is open, close it and change the state to open
			close_hand(motorPin1,motorPin2);
			state = 1;

			//let Python know it is in the ready state again
			Serial.write('1');
		}
		else
		{
			//open the hand and change the state to open
			open_hand(motorPin1,motorPin2);
			state = 0;

			//let Python know it is in the ready state again
			Serial.write('1');
		}
	}
}


/*
This function rotates the DC motor for a set amount of time
that was determined iteratively. When the rotation stops,
the prosthetic hand will be in the fully closed position.
*/
void close_hand(int motorPin1, int motorPin2)
{
	digitalWrite(motorPin1,LOW);

	for (i = 0; i<3000; i++)
	{
		digitalWrite(motorPin2, HIGH);
		delayMicroseconds(1000);
	}

	digitalWrite(motorPin2,LOW);
}


/*
This function reverses the effects on the prosthetic hand
caused by the close_hand function. It reverses the polarity of
the DC motor, causing it to rotate in the opposite direction.
*/
void open_hand(int motorPin1, int motorPin2)
{
	digitalWrite(motorPin2,LOW);

	for (i = 0; i<700; i++)
	{
		digitalWrite(motorPin1, HIGH);
		delayMicroseconds(1000);
	}
	delay(800);
	
	digitalWrite(motorPin1,LOW);
}