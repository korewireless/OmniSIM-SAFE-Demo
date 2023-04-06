# OmniSIM-SAFE-Middleware
OmniSIM SAFE - Middleware to enable Zero Touch Provisioning / Chip-2-Cloud with IoT SAFE 

## Hardware
This section provides recommended Hardware to build a IoT SAFE test device.  Other hardware can be used and recommend Linux based OS running on the device.

![image](https://user-images.githubusercontent.com/107300091/230322865-f5a76d2a-1012-4095-8725-de2e4d58ee43.png)

### RASPBERRY PI 4 MODEL B

-Recommend 4Gb+ of RAM just to provide a better experience if using VNC with the device.
- Raspberry Pi has more support for LTE HATs to provide SIM slot and connectivity.
- Raspberry Pi OS comes with VNC and SSH support which is good for 
 
### SIXFAB RASPBERRY PI 4G/LTE CELLULAR MODEM KIT

- Comes with everything to attach a modem to the Raspberry Pi,  they have choice of Modem depending on your region.
- Sixfab has great documentation to setup the modem with the Pi.

![image](https://user-images.githubusercontent.com/107300091/230323108-869a2504-2518-4949-bbb4-901e7fd53ef8.png)

https://sixfab.com/product/raspberry-pi-4g-lte-modem-kit

## Middleware setup

To allow the IoT client to use the IoT SAFE Zero-Touch Provisioning. KORE has a reference middleware that was developed with Kigen. As the IoT SAFE product is GSMA standard then then any middleware could be used with the SIM.

There are C based shared libraries that provide an API that can be used by the IoT Application to implement Zero-Touch Provisioning or Chip-2-Cloud secure communication.

### DEPLOY THE MIDDLEWARE TO A DEVICE

Easiest way to get the middleware onto a device is to type the following on the command line of the device.

```
git clone https://github.com/korewireless/OmniSIM-SAFE-Middleware.git kore
```


This creates a directory /kore and clones the OmniSIM SAFE middleware and demo applications to a safe directory 

Copy the shared libraries to the device /lib directory to enable code anywhere on the device to access IoT SAFE.

```
cd ~/kore/safe/Libs
sudo cp *.so /lib
```

## OMNISIM SAFE FILESYSTEM


| Directory	| File | Comments |
| ----------| ---- | -------- |
| ~/kore/safe	|	Directory | Application Directory for running the demos |
|	| ActivationURI.config | Text file with the url to the KORE activation portal.  This should not change |
| |	iotSafe_demo.py | Python script that calls the API in the shared libs, presents a menu to be able to demo IoT SAFE.  (Requires python 3) |
| ~/kore/safe/Data | Directory | Data directory that has AWS Root Cert and Operational Cert when downloaded |
| |	RootCA.crt | AWS Root Cert for the Operational Key if using the Standard option.  Do not delete |
|	| CN.config | Client Name Required for MQTT Connection. Remove to force ZTP |
| |	EndPoint.config | Text file with the url of the AWS IoT instance to send application data. Remove to force ZTP |
|	| operationalCertificate.pem | Operational Cert (Public) that is downloaded from AWS. Remove to force ZTP |
| ~/kore/safe/Dev | Directory | Contains header file for SAFE API and example C application |
| | Application_Executable | Binary exe of the example application, ZTO & sends a MQTT and HTTPs message to AWS |
| | Iot_Application.c	| C code for the example application |
| | iotSafe.h | Header file containing the IoT SAFE API to be included in C applications |
| ~/kore/safe/Libs |  Directory| Shared Libraries used by IoT SAFE, this is the middleware.  These 2 files should be copied to the /lib directory on the device.|
| | libiotSafe.so	IoT SAFE shared Library used for ZTP |
| | libmqtt_mutual_auth_iotsafe.so | Shared library for communicating with MQTT |


## RUNNING THE DEMO

SSH or use a Terminal window on the device.  Navigate to the safe directory where there is a iotSafe_demo python script.  This python script provides a number of options to demonstrate the functions of IoT SAFE.

```
cd ~/kore/safe

python iotSafe_demo.py
```
 

### 1. Initialize IoT SAFE

This will Zero-Touch Provision the OmniSIM SAFE if the card is not already provisioned.  You should see the following if the card requires provisioning. 

```
OmniSIM SAFE - Zero Touch Provisioning
Initialize Operational Certificate if required

 Activation point  is manufacturer-api.iotsafe.korewireless.com

 Operational Credentials Not Found

 Generating Key Pair And Csr From Sim New
GET /.well-known/est/csrattrs HTTP/1.1
User-Agent: SampleClient v1.2.1
Host: manufacturer-api.iotsafe.korewireless.com:443


HTTP/1.1 200 OK
x-amzn-RequestId: 3475dfa7-92e0-44da-b1a2-7d45bf5c6949
access-control-allow-origin: *
x-amz-apigw-id: C6mmoGV7oAMFyAA=
X-Amzn-Trace-Id: Root=1-642db7c3-0411df85df67c6d64c9323c1;Sampled=1;lineage=5e935c59:0|4f6a4953:0
content-type: application/json
content-length: 21
date: Wed, 05 Apr 2023 18:02:46 GMT

"CN=korewireless.com"
"CN=korewireless.com"
 Csr Attributes=|CN=korewireless.com|
 Key Pair Generated in SIM
 POST /.well-known/est/simpleenroll HTTP/1.1
User-Agent: SampleClient v1.2.1
Host: manufacturer-api.iotsafe.korewireless.com:443
Content-Length: 474


{"csr": "-----BEGIN CERTIFICATE REQUEST-----\nMIIBCTCBrgIBADAbMRkwFwYDVQQDDBBrb3Jld2lyZWxlc3MuY29tMFkwEwYHKoZI\nzj0CAQYIKoZIzj0DAQcDQgAEIEBSV9jwbzhJSvld5lvSC+1KkGRIvmZBlrXmAI5W\nTWLx+2Jbp1HFG/pt6CiMCuck3Uysibu7UikcuyQjYEuK/KAxMC8GCSqGSIb3DQEJ\nDjEiMCAwCwYDVR0PBAQDAgeAMBEGCWCGSAGG+EIBAQQEAwIHgDAMBggqhkjOPQQD\nAgUAA0gAMEUCIQCZ8RJL6hoLh4HdUXxZc94jYcg//0+xpVMYs8io8A/y3wIgAlx9\nGdv6cSBFJ/IhcpOQofyXxLWW5fljXEJI0QU8R+o=\n-----END CERTIFICATE REQUEST-----\n","deviceType":"IOT"}
HTTP/1.1 200 OK
x-amzn-RequestId: 2bef8ccf-c607-4456-a572-8a1858932588
access-control-allow-origin: *
x-amz-apigw-id: C6modGEhoAMFprg=
X-Amzn-Trace-Id: Root=1-642db7cf-dd5e2d3a8edc72a058ac317a;Sampled=1;lineage=5e935c59:0|4f6a4953:0
content-type: application/json
content-length: 1052
date: Wed, 05 Apr 2023 18:02:56 GMT

{"operationalCertificate":"-----BEGIN CERTIFICATE-----\nMIICjDCCAXSgAwIBAgIVAI4BIsMQzjc/MpJp2PnyGqT8ffXAMA0GCSqGSIb3DQEB\nCwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24▒▒▒<▒▒▒▒▒
▒

 Response length is 1054

 Formatted Operational Certificate is \nMIICjDCCAXSgAwIBAgIVAI4BIsMQzjc/MpJp2PnyGqT8ffXAMA0GCSqGSIb3DQEB\nCwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t\nIEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yMzA0MDUxODAw\nNTZaFw00OTEyMzEyMzU5NTlaMBsxGTAXBgNVBAMMEGtvcmV3aXJlbGVzcy5jb20w\nWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAAQgQFJX2PBvOElK+V3mW9IL7UqQZEi+\nZkGWteYAjlZNYvH7YlunUcUb+m3oKIwK5yTdTKyJu7tSKRy7JCNgS4r8o2AwXjAf\nBgNVHSMEGDAWgBRebzeJbWKg1TqXW7BbCKoMiJeNcjAdBgNVHQ4EFgQUWas7lofz\nQGRFTwm2zgaks5e32XQwDAYDVR0TAQH/BAIwADAOBgNVHQ8BAf8EBAMCB4AwDQYJ\nKoZIhvcNAQELBQADggEBAECRvOLJkAc+glIpRknf4bzxCxO/+69+hJgoPysK/39Y\nmDKMIcyjqMBNVTpEZt+ydHXn03AhgZsyqkWOQcM09xqQ1P9O+FQEqY7BTyOs90sb\nlkCfS6cqelmh1M8u+5s0zSqVA3NHkmREuvH7nlW6OoXuyAQfnso2+7ZMhTP0jKbU\nT0DBPo0ZinWCLxLQ0Uw81VT/dQtpDGSIMRUGbXBEz4lzhVtLUroYgr2xXymK1RNQ\nVbmBb79DTtDle9hT6x0Yk0Dpedq9x5CZlKEO08/Tco6UurzEpjpA9m0e/I56sDBb\nJAxUJdORjZ0PANv7QJz9IvHlW+7R2SabJe9vxk6jZC0=\n

 End Point is a25h2ej531ly5q-ats.iot.us-west-2.amazonaws.com

OmniSIM SAFE - Zero Touch Provisioning Complete
```

### 2 - Re- initialize IoT SAFE

Cleans up the device to remove any existing Operational Certificates and forces a Zero-Touch Provisioning as the initialize IoT SAFE option.

### 3 - Send Secure MQTT to IoT Core

Once the device has an Operational Certificate and End Point then this option will send the CPU temperature to a MQTT Topic called CPUTemp.

```
Send MQTT Message

 End is a25h2ej531ly5q-ats.iot.us-west-2.amazonaws.com[INFO] [LOG] [mqtt_mutual_auth_iotsafe.c:735] Establishing a TLS session to a25h2ej531ly5q-ats.iot.us-west-2.amazonaws.com:8883.
[INFO] [MQTT] [core_mqtt.c:886] Packet received. ReceivedBytes=2.
[INFO] [MQTT] [core_mqtt_serializer.c:970] CONNACK session present bit not set.
[INFO] [MQTT] [core_mqtt_serializer.c:912] Connection accepted.
[INFO] [MQTT] [core_mqtt.c:1565] Received MQTT CONNACK successfully from broker.
[INFO] [MQTT] [core_mqtt.c:1831] MQTT connection established with the broker.
[INFO] [LOG] [mqtt_mutual_auth_iotsafe.c:1255] MQTT connection successfully established with broker.

[INFO] [LOG] [mqtt_mutual_auth_iotsafe.c:1601] A clean MQTT connection is established. Cleaning up all the stored outgoing publishes.

{"CPUTemp (°C)": 48.199, "Method":"MQTT"}
[INFO] [LOG] [mqtt_mutual_auth_iotsafe.c:1417] PUBLISH sent for topic CPUTemp to broker with packet ID 1.

[INFO] [LOG] [mqtt_mutual_auth_iotsafe.c:1629] Publish To Topic Success
[INFO] [MQTT] [core_mqtt.c:2151] Disconnected from the broker.
[INFO] [LOG] [mqtt_mutual_auth_iotsafe.c:1647] Mqtt Disconnected
```

### 4 - Send HTTPs to IoT Core

Once the device has an Operational Certificate and End Point then this option will send the CPU temperature as a HTTPS message to a Topic called Temperature.

```
Send HTTPS Message

{"Temperature (°C)": 47.225, "Method":"HTTPS"}

 End is a25h2ej531ly5q-ats.iot.us-west-2.amazonaws.com
POST /topics/Temperature?qos=1 HTTP/1.1
User-Agent: SampleClient v1.2.1
Host: a25h2ej531ly5q-ats.iot.us-west-2.amazonaws.com:8443
Content-Length: 47

{"Temperature (°C)": 47.225, "Method":"HTTPS"}
HTTP/1.1 200 OK
content-type: application/json
content-length: 65
date: Wed, 05 Apr 2023 18:18:25 GMT
x-amzn-RequestId: ae8c1a66-c23e-80c1-0ba0-fc1951698f34
connection: keep-alive

{"message":"OK","traceId":"ae8c1a66-c23e-80c1-0ba0-fc1951698f34"}
```

### 5 - Demo - Initialize & send MQTT to IoT Cloud

This is shows how a real use case where an application will try and send MQTT/HTTPS data to an End Point, if the device does not have the Operational Certificate or End Point the device will Zero Touch Provision first.  The device will send new data every 10secs until ctrl+C.


### 6 - Clean IoT SAFE directory

Removes the Operational Certificate and other temporary files from the device so put it in an initial state.

### 7 – Exit

Quits the Demo script



