#include <Adafruit_MAX31855.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "Adafruit_MAX31855.h"
#include <PID_v1.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define SCREEN_ADDRESS 0x3C

#define GRAPH_WIDTH 64
float tempHistory[GRAPH_WIDTH];
int historyIndex = 0;

// Some pin definitions
const int CS_PIN = 10;
const int SPI_CLK = 13;
const int SPI_MISO = 12;
const int BOILER_PIN = 5;
const int MODE_BUTTON_PIN = 17;
const int TEMP_DOWN_BUTTON_PIN = 15;
const int TEMP_UP_BUTTON_PIN = 14;

// Values for boiler control/PID system
double BOILER_SETPOINT = 205;
bool BOILER_ON = false;
double CURRENT_TEMP;
double PID_OUTPUT;
double Kp = 38, Ki = 4, Kd = 180;
unsigned long previousTime = 0;
unsigned long cycleTime = 2000; // 2 second PID loop
unsigned long onTime = 0;
unsigned long offTime = 0;

// Actual PID controller object
PID mainPID(&CURRENT_TEMP, &PID_OUTPUT, &BOILER_SETPOINT, Kp, Ki, Kd, DIRECT);

// For debouncing and reading button presses
bool STEAM_ON = false;
bool lastModeButton = HIGH;

// For the 128x64 OLED display
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Adafruit_MAX31855 thermocouple(SPI_CLK, CS_PIN, SPI_MISO);

void setup() {
  Serial.begin(9600);

  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);   // deselect

  pinMode(BOILER_PIN, OUTPUT);  // SSR switching pin
  mainPID.SetMode(AUTOMATIC);
  mainPID.SetOutputLimits(0, cycleTime);  // Output is on-time in ms
  mainPID.SetSampleTime(1000);

  pinMode(MODE_BUTTON_PIN, INPUT_PULLUP);

  // Wait for display
  delay(500);

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  startupText();
  display.display();
  delay(500);
  display.clearDisplay();
}

void loop() {

  bool modeButton = digitalRead(MODE_BUTTON_PIN);

  if (lastModeButton == HIGH && modeButton == LOW) {
    STEAM_ON = !STEAM_ON;

    if (STEAM_ON) {
      BOILER_SETPOINT = 280;
    } else {
      BOILER_SETPOINT = 205;
    }

    // Reset PID state on mode change
    mainPID.SetMode(MANUAL);
    PID_OUTPUT = 0;
    mainPID.SetMode(AUTOMATIC);
  }

  lastModeButton = modeButton;

  CURRENT_TEMP = thermocouple.readFahrenheit() - 10;

  updateGraph(CURRENT_TEMP);
  drawGraph();

  // double error = BOILER_SETPOINT - CURRENT_TEMP;

  mainPID.Compute();

  unsigned long now = millis();

  // If the boiler should be on and cycle time is left
  if (!BOILER_ON && now - previousTime >= cycleTime)
  {
    previousTime = now;

    onTime = PID_OUTPUT;
    BOILER_ON = true;
    digitalWrite(BOILER_PIN, HIGH);
    offTime = now + onTime;

  }

  if(BOILER_ON && millis() >= offTime)
  {
    digitalWrite(BOILER_PIN, LOW);
    BOILER_ON = false;
  }

  //mainDisplay(CURRENT_TEMP, onTime, BOILER_SETPOINT);
}

void startupText()
{
  display.clearDisplay();

  display.setTextSize(2); // Draw 2X-scale text
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(50, 0);
  display.println(F("Good \n"));
  display.setCursor(20, 15);
  display.println(F("morning!"));
  display.display();
  delay(500);

}

void mainDisplay(double temp, unsigned long onTime, double setpoint)
{
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.setTextSize(1);
  display.printf("Mode: %s\n", STEAM_ON ? "STEAM" : "BREW");

  display.setTextSize(2); // Draw 2X-scale text

  display.printf("Boiler:\n%.1fF\n", temp);

  display.setTextSize(1);
  display.printf("OnTime: %lums\n", onTime);
  display.printf("Set Point:\n%.1fF\n", setpoint);

  display.display();
}

void updateGraph(float currentTemp) {
  tempHistory[historyIndex] = currentTemp;
  historyIndex = (historyIndex + 1) % GRAPH_WIDTH;
}

void drawGraph() {
  display.clearDisplay();
  
  // Graph dimensions - leave room for axes and labels
  int graphLeft = 20;
  int graphTop = 8;
  int graphWidth = 108;  // 128 - 20 for left margin
  int graphHeight = 48;  // Leave room at bottom for X axis label
  int graphBottom = graphTop + graphHeight;
  
  // Temperature range - full scale from room temp to steam
  float minTemp = 70;   // Room temperature
  float maxTemp = 280;  // Above steam temp
  
  // Draw axes
  display.drawLine(graphLeft, graphTop, graphLeft, graphBottom, SSD1306_WHITE);  // Y axis
  display.drawLine(graphLeft, graphBottom, graphLeft + graphWidth, graphBottom, SSD1306_WHITE);  // X axis
  
  // Y axis labels (every 50F)
  display.setTextSize(1);
  for (int temp = 75; temp <= 300; temp += 50) {
    int y = map(temp, minTemp, maxTemp, graphBottom, graphTop);
    display.drawPixel(graphLeft - 2, y, SSD1306_WHITE);  // Tick mark
    display.setCursor(0, y - 3);
    display.print(temp);
  }
  
  // Draw temperature history
  for (int x = 0; x < GRAPH_WIDTH - 1; x++) {
    int idx = (historyIndex + x) % GRAPH_WIDTH;
    int nextIdx = (historyIndex + x + 1) % GRAPH_WIDTH;
    
    // Skip if no data yet
    if (tempHistory[idx] < 1) continue;
    
    // Map temperature to Y coordinate (inverted - high temp at top)
    int y1 = map(constrain(tempHistory[idx], minTemp, maxTemp), minTemp, maxTemp, graphBottom, graphTop);
    int y2 = map(constrain(tempHistory[nextIdx], minTemp, maxTemp), minTemp, maxTemp, graphBottom, graphTop);
    
    // Scale X to fit in graph area
    int screenX1 = graphLeft + (x * graphWidth) / GRAPH_WIDTH;
    int screenX2 = graphLeft + ((x + 1) * graphWidth) / GRAPH_WIDTH;
    
    display.drawLine(screenX1, y1, screenX2, y2, SSD1306_WHITE);
  }
  
  // Draw setpoint line (dashed)
  int setpointY = map(205, minTemp, maxTemp, graphBottom, graphTop);  // Your brew setpoint
  for (int x = graphLeft; x < graphLeft + graphWidth; x += 3) {
    display.drawPixel(x, setpointY, SSD1306_WHITE);
  }
  
  // Current temp in corner
  display.setCursor(graphLeft + graphWidth - 30, 0);
  display.print(tempHistory[(historyIndex - 1 + GRAPH_WIDTH) % GRAPH_WIDTH], 1);
  
  display.display();
}