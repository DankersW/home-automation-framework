#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* wifi_ssid = "SaveOurWinters";
const char* wifi_pwd =  "prettyflyforawifi";
const char* mqtt_broker_address = "192.168.1.125";
const int mqtt_port = 1883;
const char* device_id = "001";

WiFiClient espClient;
PubSubClient client(espClient);

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
        if (client.connect(device_id))
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

void setup()
{
    Serial.begin(115200);

    if (connectToWifi())
    {
        Serial.println("Connected to the WiFi network");
    }

    if (connectToMqttBroker())
    {
        Serial.println("Connected to the MQTT broker")
    }

    client.publish("topic/data", "hello");
    client.subscribe("topic/data");
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
}

void loop()
{
    client.loop();
}