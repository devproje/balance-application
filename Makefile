GC = go
TARGET = balance-application
SRCS = *.go **/*.go

$(TARGET): $(SRCS)
	go build -o $(TARGET) github.com/devproje/balance-application

clean: $(TARGET)
	rm -f $(TARGET)
