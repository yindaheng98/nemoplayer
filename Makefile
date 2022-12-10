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
	cd build && gcc $(CXXFLAGS) $(INCS) -c -o $@ ../common.c
player.c.o:
	cd build && gcc $(CXXFLAGS) $(INCS) -c -o $@ ../player.c
deps: common.c.o player.c.o vpx-deps

LDFLAGS += -L. -lvpx -lm -lpthread
LDFLAGS += -m64 -g

LDFILES += $(DEPFILES)
LDFILES += common.c.o

player: deps
	cd build && g++ -o ../$@  $(LDFILES) player.c.o $(LDFLAGS)

player.a: deps
	cd build && ar -crsv player.a $(LDFILES)

SOFLAGS += -m64
SOFLAGS += -g
SOFLAGS += -Wl,--no-undefined
SOFLAGS += -Wl,-soname,player.so.5
SOFLAGS += -Wl,--version-script,../player.ver
player.so: deps
	cd build && g++ -shared $(SOFLAGS) -o player.so $(LDFILES) -lpthread -lm -lvpx

install: player.a player.so
	cp -p build/player.a /usr/local/lib/libnemoplayer.a
	cp -p player.pc /usr/local/lib/pkgconfig/player.pc
	cd build && make install

player-clean:
	rm -f common.c.o
	rm -f player.c.o
	rm -f player
	rm -f build/nemoplayer.so
	rm -f build/libnemoplayer.a
clean: player-clean
	cd build && make clean