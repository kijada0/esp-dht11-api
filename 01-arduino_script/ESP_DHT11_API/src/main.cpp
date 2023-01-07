#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <DHT.h>
 
 // -------------------------------------------------------------------------------- //

#define DHT_pin 16
DHT dht;

// -------------------------------------------------------------------------------- //

const char* ssid = "KrólestwoNauki";
const char* password = "53357007";
 
ESP8266WebServer server(80);

IPAddress local_IP(192, 168, 0, 125);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);

// -------------------------------------------------------------------------------- //

String status = "";
float temperature = 0;
float humidity = 0;

// -------------------------------------------------------------------------------- //

void update(){
  status = dht.getStatusString();
  humidity = dht.getHumidity();
  temperature = dht.getTemperature();
}

// -------------------------------------------------------------------------------- //

void getAll(){
  String message;

  update();

  message = "";
  message += "{\"temperature\" : ";
  message += String(temperature);
  message += ",\"humidity\" : ";
  message += String(humidity);
  message += ",\"status\" : \"";
  message += status;
  message += "\"}";

  server.send(200, "text/html", message);
}

void getTemperature(){
  String message;

  update();

  message = String(temperature);
  server.send(200, "text/html", message);
}

void getHumidity(){
  String message;

  update();

  message = String(humidity);
  server.send(200, "text/html", message);
}

void restServerRouting() {
    server.on("/", HTTP_GET, getAll);
    server.on("/temperature", HTTP_GET, getTemperature);
    server.on("/humidity", HTTP_GET, getHumidity);
}
 
// Manage not found URL
void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

// -------------------------------------------------------------------------------- //
 
void setup(void) {
  Serial.begin(115200);
  Serial.println("");

  dht.setup(DHT_pin);

  WiFi.mode(WIFI_STA);
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }

  WiFi.begin(ssid, password);
  Serial.println("");
  
  Serial.println("");
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  restServerRouting();
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");
}
 
// -------------------------------------------------------------------------------- //

void loop(void) {
  server.handleClient();
}