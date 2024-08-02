# real time chat application using django and django channels
> ## into
> This is a simple real time chat application built using python django web application framework.<br>
> and django <a href='https://channels.readthedocs.io/'>channels</a> Channels is a project that takes Django and extends its abilities beyond HTTP - to handle WebSockets, chat protocols, IoT protocols, and more. It’s built on a Python specification called ASGI.
>Channels builds upon the native ASGI support in Django. Whilst Django still handles traditional HTTP, Channels gives you the choice to handle other connections in either a synchronous or asynchronous style.
> i have utilised the asynchronous computing with websockets to serve multiple client at same time.(real time message excahnge or chatting)
> this project also utilises out of the box user authentication , orm and session management utilities of django framework to manage authentication and storing messages to database.
## description
> This project utilises websockets to send data and an <strong>Dephne</strong> an asgi protocol server to server those websockets in real time .
> This project utilises django auth to authenticate user and it is this flexibility of django which is why it was paired with dajngo channels . <br>
> but there are some issues how django handels querying database . Django database calls are synchronous in nature an d are thus blocking which can be easily fixed using "asgiref".
> I have used sqlite as my data base .
## Working of project
>user is first required to register them and log them in using credentials
>then they can make rooms of any name . A person making room is its admin and all the people joining are members. An admin choose to make the room public or private by adding private key to private key field.
>if the said field is left blank then the room is public any body can join it using room name<br>
> The app has very basic flow and few pages which includes signup page , loginpage , home page and chat room page some additional pages are also registered in path for testing and will certainly be removed in production<br>
>An admin can <br>1.delete rooms he/she created and doing so will also delete all the message and members associated with it.<br>2. ban a user from entering the room . one cath here is that i added this functionality for only the users that are members of thet room
>All messages sent are saved in data base in data base and can be once the user enter the room
## some considerations
>### UI
>pardon me for average UI as its was my first full stack Asgi project so I focuesd on learning backend more. Such as django orm and client auth (i am in love with django 😊).
>### security
>django secrete: the django secrete here is insecure and should be changed in production.<br>
>data:all the data in database is for testing only and that 'all data url' is just for testing will surely be removed in production . Also django admin url and password should be changed.<br>
>database: it is highly recomemded to use redis backend layers with asgi apps but for development purposes used django backend layers which will surely be change later. other wise it will result in data loss.<br>
>post calls: i have made a bunch of "unsafe" post calls using jquery ajax calls which might not be in accordance with rfc standard
## deployment
> sadly i have not deployed my project but if you want to experience it/test it (thanks 😊).if you are using vscode You can follow these steps
> <ol>
  <li>clone this repo i have also included .venv(although no recommended) which will suffice all dependencies</li>
  <li>set python interpreter to specific to vitual envirenment you can do so by clicking iterpreter at the bottom of screen vscode will automaticaly detect the interpreter and recommend use using the select that
  
  </li>

  <li></li>
  <li></li>
  <li></li>
</ol>
