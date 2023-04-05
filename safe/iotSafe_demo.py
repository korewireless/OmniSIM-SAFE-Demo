# OmniSIM SAFE Demo Client 1.1.1
from ctypes import *
from gpiozero import CPUTemperature
import time
import os

running = True
topic = "CPUTemp"
port = 8883
LoRa = '00:80:00:00:A0:00:8F:65'    

iot_safe_lib = "/lib/libiotSafe.so"
mqtt_lib = "/lib/libmqtt_mutual_auth_iotsafe.so"
iot_safe_api = CDLL(iot_safe_lib)
mqtt_api = CDLL(mqtt_lib)


mqtt_api.iotsafe_getMQTTConnection.argtypes = [c_int]
mqtt_api.iotsafe_publish.argtypes = (c_char_p,c_char_p)
iot_safe_api.iotsafe_initialize.argtypes = (c_int,c_int,c_char_p)
mqtt_api.http_req.argtypes = (c_char_p,c_int, c_char_p,c_char_p,c_int)


menu_options = {
    1: 'Initiaize IoT SAFE - will zero-touch provision if required',
    2: 'Re-initialize IoT SAFE - force cleanup and download new Operational Key',
    3: 'Send Secure MQTT to IoT Core',
    4: 'Send HTTPs to IoT Core',
    5: 'Demo - Initialize & send MQTT to IoT Cloud',
    6: 'Clean IoT SAFE directory',
    7: 'Exit',
}

def print_menu():
    print("\n------- OmniSIM SAFE Demo --------\n")
    for key in menu_options.keys():
        print (key, '-', menu_options[key] )
        
def option1():
    print("OmniSIM SAFE - Zero Touch Provisioning")
    print("Intialize Operational Certificate if required\n")
    if initialize_iotSafe(0) == 0:
        print("\nOmniSIM SAFE - Zero Touch Provisioning Complete\n")

def option2():
    print("OmniSIM SAFE - Zero Touch Provisioning")
    print("Resets Operational Certificate")
    print("Initializes IoT SAFE and Connects to activation portal")
    print("Request new Operational Certificate\n")
    if initialize_iotSafe(1) == 0:
        print("\nOmniSIM SAFE - Zero Touch Provisioning Complete\n")
    
def initialize_iotSafe(refresh):
    status = iot_safe_api.iotsafe_initialize(refresh,0,None)

    if status != 0:
        print("There was an error. Status code: " + str(status))
        iot_safe_api.cleanup_iot()
    return status

def demo():
    print("OmniSIM SAFE Demo")
    print("Checks if OmniSIM SAFE is Provisioned, if not will zero-touch provision")
    print("Then sends MQTT mesages until ctrl+C\n\n")

    try:
        if initialize_iotSafe(0) == 0:
            running = True
                
            while running:
                status=mqtt_api.iotsafe_getMQTTConnection(port)
                if status != 0:
                    print("There was an issue setting up iotsafe_getMQTTConnection. Status code: " + str(status))
                    running = False

                cpu = CPUTemperature()
                mqtt_msg = "{\"CPUTemp (°C)\": " + str(cpu.temperature) + ", \"Method\":\"MQTT\"}"
                print(mqtt_msg + "\n")
                        
                status = mqtt_api.iotsafe_publish(mqtt_msg.encode(),topic.encode())
                if status != 0:
                    print("There was an issue setting up iotsafe_publish. Status code: " + str(status))
                    running = False

                mqtt_api.iotsafe_disconnect()
                if status != 0:
                    print("There was an error. Status code: " + str(status))
                    iot_safe_api.cleanup_iot()
                    running = False
                
                time.sleep(10.0)

    except (KeyboardInterrupt):
        running = False
        mqtt_api.iotsafe_disconnect()
        if status != 0:
            print("There was an error. Status code: " + str(status))
            iot_safe_api.cleanup_iot()
        print ("\nDemo Stopped\n")

def send_MQTT():
    print("Send MQTT Message\n")
    status=mqtt_api.iotsafe_getMQTTConnection(port)
    if status != 0:
        print("There was an issue setting up iotsafe_getMQTTConnection. Status code: " + str(status))
    cpu = CPUTemperature()
    mqtt_msg = "{\"CPUTemp (°C)\": " + str(cpu.temperature) + ", \"Method\":\"MQTT\"}"
    print(mqtt_msg)
                   
    status = mqtt_api.iotsafe_publish(mqtt_msg.encode(),topic.encode())
    if status != 0:
        print("There was an issue setting up iotsafe_publish. Status code: " + str(status))
    
    mqtt_api.iotsafe_disconnect()
    if status != 0:
        print("There was an error. Status code: " + str(status))
        iot_safe_api.cleanup_iot()

def send_HTTPS():
    print("Send HTTPS Message\n\n")
    
    cpu = CPUTemperature()
    buffer = ""
    http_msg = "{\"Temperature (°C)\": " + str(cpu.temperature) + ", \"Method\":\"HTTPS\"}"
    http_path = "topics/Temperature?qos=1"
   
    print(http_msg)
                   
    status = mqtt_api.http_req(http_path.encode(),8443,http_msg.encode(),buffer.encode(), 512)
    if status != 0:
        print("There was an issue setting up http_req. Status code: " + str(status))

def deleteFile(file):
    cwd = os.getcwd()
    fileToDel = os.path.join(cwd, file)
    if os.path.exists(fileToDel):
        os.remove(fileToDel)
        print("Remove file: " + fileToDel)
    else:
        print("File does not exist: " + fileToDel)
    
    
    
def clean_iots():
    print("Cleans the Device working directory")
    iot_safe_api.cleanup_iot()
    deleteFile("Csr1.csr")
    deleteFile("Data/CN.config")
    deleteFile("Data/EndPoint.config")
    deleteFile("Data/operationalCertificate.pem")

if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            send_MQTT()
        elif option == 4:
            send_HTTPS()
        elif option == 5:
            demo()
        elif option == 6:
            clean_iots()
        elif option == 7:
            print('\nExit Secure SIM Demo')
            iot_safe_api.cleanup_iot()
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 8.')


