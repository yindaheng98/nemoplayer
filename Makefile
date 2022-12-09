all:
	cd build && make all
clean: player-clean
	cd build && make clean

INCS += -I.
INCS += -I./..
INCS += -I./../libvpx
INCS += -I./../libvpx/vp9
INCS += -I./../libvpx/third_party/libwebm
INCS += -I./../libvpx/third_party/libyuv/include

CXXFLAGS += -m64
CXXFLAGS += -g
CXXFLAGS += -O3
CXXFLAGS += -fPIC -U_FORTIFY_SOURCE
CXXFLAGS += -D_FORTIFY_SOURCE=0
CXXFLAGS += -D_LARGEFILE_SOURCE
CXXFLAGS += -D_FILE_OFFSET_BITS=64
CXXFLAGS += -Wall

common.c.o:
	cd build && gcc $(CXXFLAGS) $(INCS) -c -o ../$@ ../common.c
common-clean:
	rm common.c.o

player.c.o: all
	cd build && gcc $(CXXFLAGS) $(INCS) -c -o ../$@ ../player.c
player-clean: common-clean
	rm player.c.o
	rm player

LDFLAGS += -L. -lvpx -lm -lpthread
LDFLAGS += -m64 -g

LDFILES += ivfdec.c.o
LDFILES += tools_common.c.o
LDFILES += video_reader.c.o
LDFILES += y4minput.c.o

player: player.c.o common.c.o
	cd build && g++ -o ../$@  $(LDFILES) ../player.c.o ../common.c.o $(LDFLAGS)