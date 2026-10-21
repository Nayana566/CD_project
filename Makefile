CC      = gcc
CFLAGS  = -Wall -g
TARGET  = ifcompiler

all: $(TARGET)

parser.tab.c parser.tab.h: parser.y
	bison -d parser.y

lex.yy.c: lexer.l parser.tab.h
	flex lexer.l

$(TARGET): parser.tab.c lex.yy.c ast.c ast.h
	$(CC) $(CFLAGS) -o $(TARGET) parser.tab.c lex.yy.c ast.c

run: $(TARGET)
	./$(TARGET) tests/valid/if_else.txt

test: $(TARGET)
	sh tests/run_tests.sh

clean:
	rm -f $(TARGET) $(TARGET).exe parser.tab.c parser.tab.h lex.yy.c

.PHONY: all run test clean
