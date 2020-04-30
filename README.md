This project has a database that holds data about messages. 
This 'API' was written in order to help the "client side" manage with  the data (delete, insert ,select).
The API lets the client:
 Add messages by sending a Json (and of course sending the matching url) 
 Delete messages by mentioning their application Id/session Id or delete signal messages by mentioning the message Id .
Get messages/message in the same way mentioned above.

The function in the 'app' file receives the clients request and is responsible to pass on the incoming data to the functions that manage the database (in the 'DB' file) and also return the the matching data to the client. 
(for delete/get single message there is a different function from delete/get messages)



The functions in the 'DB' file has 2 parts: 
The first one executes queries straight on the database (functions that names end with 'DB') 
The second one runs the first one and returns the data back abstractly.

The 'Message' file has a class that defines the 'Message' object, (Created in order to managing the data easily)


The 'test_api' file is a test plan for the 'API'


The database 'MessagesDB' is built in the following way:


TABLE "Messages":
messageId" TEXT NOT NULL PRIMARY KEY, "applicationId" TEXT NOT NULL, "sessionId" TEXT NOT NULL, "content" TEXT,


TABLE "participants":
"participantId" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "messageId" TEXT NOT NULL, articipantName" TEXT, " FOREIGN KEY("messageId") REFERENCES "Messages" )
