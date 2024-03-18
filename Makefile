.PHONY: main
main:
	echo "#!/usr/bin/env python3" > VMTranslator;
	cat VMTranslator.py >> VMTranslator;
	chmod +x ./VMTranslator;

.PHONY: zip
zip:
	zip project7.zip \
		Makefile \
		lang.txt \
		VMTranslator.py \
		CodeWriter.py \
		Parser.py

.PHONY: clean
clean:
	rm -f VMTranslator;

.PHONY: test
test:
	./VMTranslator StackArithmetic/SimpleAdd/SimpleAdd.vm
	./VMTranslator StackArithmetic/StackTest/StackTest.vm
	./VMTranslator MemoryAccess/PointerTest/PointerTest.vm
	./VMTranslator MemoryAccess/BasicTest/BasicTest.vm
	./VMTranslator MemoryAccess/StaticTest/StaticTest.vm
	./VMTranslator ProgramFlow/BasicLoop/BasicLoop.vm
	./VMTranslator ProgramFlow/FibonacciSeries/FibonacciSeries.vm
	./VMTranslator FunctionCalls/SimpleFunction/SimpleFunction.vm
	./VMTranslator FunctionCalls/StaticsTest
