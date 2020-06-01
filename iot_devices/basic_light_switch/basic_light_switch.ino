#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define RELAY_OUTPUT_PORT D1
#define SWITCH_INPUT_PORT D2
#define ONBOARD_LED 2

const char* wifi_ssid = "SaveOurWinters";
const char* wifi_pwd =  "prettyflyforawifi";
const char* mqtt_broker_address = "192.168.1.125";
const int mqtt_port = 1883;
String device_id = "light_switch_001";
String mqtt_control_topic = "iot/" + device_id + "/control";
String mqtt_state_topic = "iot/" + device_id + "/state";
String mqtt_attach_topic = "iot/" + device_id + "/attach";
bool mqtt_state = 0;
bool light_state = 0;
bool light_state_prev = 0;
bool switch_state_prev = 0;
bool mqtt_state_set = 0;
 
WiFiClient espClient;
PubSubClient client(espClient);

void setupIo();
bool connectToWifi();
bool connectToMqttBroker();


void setup()
{
    Serial.begin(115200);

    setupIo();

    if (connectToWifi())
    {
        Serial.println("Connected to the WiFi network");
    }
    if (connectToMqttBroker())
    {
        Serial.println("Connected to the MQTT broker");
    }
    
    client.subscribe(mqtt_control_topic.c_str());
    digitalWrite(ONBOARD_LED, HIGH); // Active low
    client.publish(mqtt_attach_topic.c_str(), "");
}

void loop()
{
    bool switch_state = digitalRead(SWITCH_INPUT_PORT);

    if (switch_state != switch_state_prev)
    {
        light_state = switch_state;
    }
    if (mqtt_state_set)
    {
        light_state = mqtt_state;
    }

    Serial.print("Switch state: ");
    Serial.print(switch_state, DEC);
    Serial.print(" - prev: ");
    Serial.print(switch_state_prev, DEC);
    Serial.print("\t mqtt state: ");
    Serial.print(mqtt_state, DEC);
    Serial.print(" - set: ");
    Serial.print(mqtt_state_set, DEC);
    Serial.print("\t light state: ");
    Serial.println(light_state, DEC);

    digitalWrite(RELAY_OUTPUT_PORT, light_state);
    if (light_state != light_state_prev)
    {
        const char* mqtt_data = light_state ? "1" : "0";
        client.publish(mqtt_state_topic.c_str(), mqtt_data);
    }

    switch_state_prev = switch_state;
    mqtt_state_set = false;
    light_state_prev = light_state;
    
    client.loop();
    delay(100);
}

void setupIo()
{
     pinMode(ONBOARD_LED, OUTPUT);
     pinMode(RELAY_OUTPUT_PORT, OUTPUT);
     pinMode(SWITCH_INPUT_PORT, INPUT);
     digitalWrite(ONBOARD_LED, LOW); // Active low
     digitalWrite(RELAY_OUTPUT_PORT, LOW); 
}

bool connectToWifi()
{
    WiFi.begin(wifi_ssid, wifi_pwd);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }
    return true;
}

bool connectToMqttBroker()
{
    client.setServer(mqtt_broker_address, mqtt_port);
    client.setCallback(callback);
    while (!client.connected())
    {
        Serial.println("Connecting to MQTT...");
        if (client.connect(device_id.c_str()))
        {
            Serial.println("connected");
        }
        else
        {
            Serial.print("failed with state ");
            Serial.print(client.state());
            delay(2000);
        }
    }
    return true;
}

void callback(char* topic, byte* payload, unsigned int length)
{
    Serial.print("Message arrived in topic: ");
    Serial.print(topic);
    Serial.print("\t Message: \"");
    for (int i = 0; i < length; i++)
    {
        Serial.print((char)payload[i]);
    }
    Serial.println("\"");
    
    if (strcmp(topic, mqtt_control_topic.c_str()) == 0)
    {
        if (length == sizeof(bool))
        {
            mqtt_state = (char)payload[0] != '0';
            mqtt_state_set = true;
        }
    }
}
