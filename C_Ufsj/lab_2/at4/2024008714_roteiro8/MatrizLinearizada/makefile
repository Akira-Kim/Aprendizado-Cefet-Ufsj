EXECUTAVEL = main
SRCS = main.c MatrizLinearizada.c
OBJS = $(SRCS:.c=.o)
CFLAGS = 

all: $(EXECUTAVEL)

$(EXECUTAVEL): $(OBJS)
	$(CC) $(OBJS) -o $(EXECUTAVEL)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(EXECUTAVEL)
	rm -f *~
