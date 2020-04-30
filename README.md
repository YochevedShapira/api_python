# api_python
The project has database that holds data about messages and in order that the "client side" 
will be able to manage with the data (delete, insert ,select) this 'API' is written.
The API  let the client:

Add message by sending a Json (and of course sending the match url).

Delete messages by mention their application id/session id or delete signal message by mention message id.

Get messages/message as mentioned above(like delet).


 
The function in 'app' file get the client request and responsible to pass the data they got to the functions
that manage with the database (in 'DB' file) and also return the client the matching data.
For delete/get single message there is a different function from delete/get messages))
(that file runs the project)


The functions in 'DB' file has 2 parts:
The first one executes queries straight on the database(functions that their name ends with 'db').
The second one runs the first one and returns and back data abstractly.


The 'Message' file has a class that defines the 'Message' object ,(I have created him for managing with the data easily)


The 'test_api' file is a test plan for the 'api'




The database 'MessagesDB' is build this way:


TABLE "Messages":

 messageId" TEXT NOT NULL PRIMARY KEY,
 "applicationId" TEXT NOT NULL,
 "sessionId" TEXT NOT NULL,
 "content" TEXT,
 
TABLE "participants":



  "participantId" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
"messageId" TEXT NOT NULL,
articipantName" TEXT,
 " FOREIGN KEY("messageId") REFERENCES "Messages" )

