all:
	cd build && make V=1 all
clean:
	cd build && make clean

player.c.o: all
	cd build && gcc -I./../libvpx/third_party/libwebm -I./../libvpx/vp9 -I./../libvpx/vp9 -I./../libvpx/third_party/libyuv/include -m64 -g -O3 -fPIC -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -Wall -Wdeclaration-after-statement -Wdisabled-optimization -Wfloat-conversion -Wpointer-arith -Wtype-limits -Wcast-qual -Wvla -Wimplicit-function-declaration -Wuninitialized -Wunused -Wextra -Wundef -I. -I"./../libvpx" -M ./../libvpx/../player.c | sed -e 's;^\([a-zA-Z0-9_]*\)\.o;../player.c.o ../player.c.d;' > ../player.c.d
player: player.c.o
	cd build && g++ -L. -m64 -g -o ../player ivfdec.c.o tools_common.c.o video_reader.c.o ../player.c.o -lvpx -lm -lpthread