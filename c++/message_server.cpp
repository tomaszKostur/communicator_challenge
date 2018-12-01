#include <iostream>
#include <boost/asio.hpp>

#define PORT 5000

using boost::asio::ip::tcp;

int main() {
    boost::asio::io_context io_context;
    tcp::acceptor acceptor(io_context, tcp::endpoint(tcp::v4(), PORT));
    for (;;) {
        tcp::socket socket(io_context);

        // acceptor.acept waits until connection;
        acceptor.accept(socket);
        boost::asio::write(socket, boost::asio::buffer("huehue from server\n"));
    }
    return 0;
}
