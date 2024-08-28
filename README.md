    # ticLANtoe
    #### Video Demo:  <URL HERE>
    #### Description:
    Our project is basically a game of Tictactoe. Seems too simple right? Well that's because the game part is simple, the real complexity comes from the fact that we madeit a LAN connection based game. We wanted to do something to challenge ourselves, something that would force us to learn new skills. We knew from the beginning we wanted to do something related to connection, later we settled on making a simple game like tictactoe using this connection. It involved a lot of learning, especially in the usage of Python's socket library. Familiarising ourselves with the library's documentation was an arduous task and dealing with errors the kind we've never dealt with before was a whole other experience. Sometimes it wasn't clear what was going wrong, since the server was running properly but it's behavior with the client was not as expected, leading to a lot of re-evaluation of our code, for example sending messages and having them only be displayed on the client side once ANOTHER message was sent was a huge issue.
    
    Making tictactoe by itself was the original task but seemed too simple for a two-person project. this part of the code was made highly modular, which helped later on in transferring the functionality to a single file. Near the end we realised that the code would make much more sense if we had used Object-Oriented-Programming and implemented the board as an object with related functionality wrapped up nicely in a class but decided to dismiss it on the basis of "If it ain't broke, dont fix it".

    
    Initially we had 3 seperate files, tictactoe.py, server.py and client.py. We first decided to implement tictactoe on the server side since we've heard its irresponsible in game development to allow clients access to important code; This was not smooth sailing. Lots of errors, things not working as intended, endless amounts of blank lines being sent to the client, the game not continuing when both users agree to a rematch. After a while we got server.py and client.py working as expected!
    Then we had to somehow implement both server.py and client.py as one file as per the requirements of the Final Project. This wasn't that hard. We made sure that on the global scope there wasn't any variable name used twice for different purposes, besides that it worked perfectly.

    
    We have the credits and instructions on how to play display on each player's terminal. This was initially implemented from the server-side but, it being simpler with print statements, we decided on implementing this part on the client-side. We had this message show once a client successfully connected to the server. The message only ever needs to be displayed once so we believe this was a good approach to handle this issue.

    
    Furthermore, pytesting project.py was a new journey. Due to the fact that most of our functions for project.py involve some function that utilizes Python's "socket" library, we had to learn and use monkeypatch so that we could disable messages and prompts being sent to clients for display in "test_project.py" when testing these functions.

