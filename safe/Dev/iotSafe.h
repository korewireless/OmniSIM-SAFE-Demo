//Initializes Iot Safe And Connects to activation portal if no operational certificate found,Need to be called once atleast once at first.


int iotsafe_initialize(int,int,char *);
int fetch_eui(char *);
int export_lora();
char * cleanup1();
//Clean up Memory(For Internal Use)


int cleanup_iot();

//Send Http req
//Format:http_req(path,port,message,buffer,buffer_len)
//Eg:http_req("www.google.com","7778","{ \"test\":\"Hello1\" }","POST)
//Use "GET" for get request

int http_req(char *,int,char *,char *,int);

//Connects to mqtt endpoint
//params(port)

int iotsafe_getMQTTConnection(int);

//Publishes to topic
//Params(Message,Topic)

int iotsafe_publish(char * ,char * );

//Disconnects Iot Safe
int iotsafe_disconnect();
