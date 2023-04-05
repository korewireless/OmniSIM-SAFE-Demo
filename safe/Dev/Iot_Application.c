#include "iotSafe.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


int main()
{	char *awsend;
	
	printf("Intialize Operational Certificate Module \n");
	int status=0;
	char buffer[512];
    status=iotsafe_initialize(0,0,NULL);
	printf("Status is %d",status);

	if(status==0)
{	
	
	printf("Starting Mqtt Connection \n");
	int port=8883;
	
 	
	
status=iotsafe_getMQTTConnection(8883);
printf("\n status %d \n",status);
if(status==0)
{
  for(int i=0;i<1;i++) 
{
	status=iotsafe_publish("{\"Temperature\":97,\"Method\":\"MQTT\"}","Temperature");
	
}
}
printf("\n status %d \n",status);
    iotsafe_disconnect();

status=http_req("topics/Temperature?qos=1",8443,"{\"Temperature\":95,\"Method\":\"HTTPS\"}",buffer,512);
printf("\n status %d \n",status);


}


cleanup_iot();
return 0;
}
