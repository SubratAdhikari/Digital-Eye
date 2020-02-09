#define button 5  //button pin D5
boolean buttonState;

void setup()
{   // putting internal pullup for resistor
  pinMode(button,INPUT_PULLUP);
      // setting baudrate to 9600
  Serial.begin(9600);
  
}

void loop()
{    
  buttonState = digitalRead(button);
    // while button is clicked
  if (buttonState==0){
  Serial.println(buttonState);
    // wait until the the button is relished
  while (buttonState==0){buttonState = digitalRead(button);}
  }
  
}
