all:
	cd build && make V=1 all
clean:
	cd build && make clean

INCS += -I.
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

player-clean:
	rm player.c.o
	rm player

player.c.o: all
	cd build && gcc $(CXXFLAGS) $(INCS) -c -o ../$@ ../player.c


LDFLAGS += -L. -lvpx -lm -lpthread
LDFLAGS += -m64 -g

player: player.c.o
	cd build && g++ -o ../$@  ivfdec.c.o tools_common.c.o video_reader.c.o ../$< $(LDFLAGS)