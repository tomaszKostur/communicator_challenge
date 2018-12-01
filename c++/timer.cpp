/*
Simpliest application just for configure build system with boost
*/

#include <iostream>
#include <boost/asio.hpp>
#include <cstdio>

using namespace std;

int main() {
    cout << "Hello World!" << endl;
    boost::asio::io_context io;
    boost::asio::steady_timer t(io, boost::asio::chrono::seconds(1));
    t.wait();
    cout << "Timer passed!" << endl;
    return 0;
}
