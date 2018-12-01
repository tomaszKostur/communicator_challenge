#include <iostream>
#include <boost/asio.hpp>
#include <boost/array.hpp>

#define PORT "5000"
#define HOST "localhost"

using boost::asio::ip::tcp;

int main() {
    boost::asio::io_context io_context;
    tcp::socket socket(io_context);
    tcp::resolver resolver(io_context);
    tcp::resolver::results_type endpoints = resolver.resolve(HOST, PORT);
    boost::asio::connect(socket, endpoints);

    boost::array<char, 128> buf;
    std::size_t msg_len = socket.read_some(boost::asio::buffer(buf));
    std::cout.write(buf.data(), msg_len);

    return 0;
}
