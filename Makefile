libvpx.a:
	cd build && make libvpx.a

DEPFILES += ivfdec.c.o
DEPFILES += tools_common.c.o
DEPFILES += video_reader.c.o
DEPFILES += y4minput.c.o

vpx-deps: libvpx.a
	cd build && make $(DEPFILES)

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
player.c.o:
	cd build && gcc $(CXXFLAGS) $(INCS) -c -o ../$@ ../player.c
deps: common.c.o player.c.o vpx-deps

LDFLAGS += -L. -lvpx -lm -lpthread
LDFLAGS += -m64 -g

LDFILES += $(DEPFILES)
LDFILES += ../common.c.o

player: deps
	cd build && g++ -o ../$@  $(LDFILES) ../player.c.o $(LDFLAGS)

common-clean:
	rm common.c.o
player-clean: common-clean
	rm player.c.o
	rm player
clean: player-clean
	cd build && make clean