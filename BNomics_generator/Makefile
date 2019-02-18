#//=============================================================
#//(c) 2011 Distributed under MIT-style license. 
#//(see LICENSE.txt or visit http://opensource.org/licenses/MIT)
#//=============================================================

CC=g++
CFLAGS=-Wall -c -fPIC -std=c++11

all: ofext.so

ofext.so: ofext.o
	$(CC) -shared -o ofext.so ofext.o 

ofext.o: ofext.cpp
	$(CC) $(CFLAGS) ofext.cpp
