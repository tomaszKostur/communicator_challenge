all: timer message_server message_client

timer: timer.cpp
	g++ -std=c++17 -Wall -Wextra -g $^ -o $@ -lboost_system

message_server: message_server.cpp
	g++ -std=c++17 -Wall -Wextra -g $^ -o $@ -lboost_system

message_client: message_client.cpp
	g++ -std=c++17 -Wall -Wextra -g $^ -o $@ -lboost_system
