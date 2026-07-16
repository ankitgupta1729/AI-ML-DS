package main

// Go routines are the implementation of the concurrency in go.
// They make it very simple to actually create new lightweight threads in go that can 
// be ran independently of other sections of the code, allowing us to implement
// parallel processing and concurrency and multi-threading inside of our go programs.

import (
	"fmt"
	"time"
)

func run() {
	time.Sleep(2 * time.Second)
	fmt.Println("run")
}

func run2() {
	time.Sleep(4 * time.Second)
	fmt.Println("run2")
}

func run3() {
	time.Sleep(6 * time.Second)
	fmt.Println("run3")
}

func main() { // there is one go routine that runs this main function and so it will not 
// see other functions like run(), run2() and run3() running concurrently and it prints "Done"
// and main function will end. so write below time.sleep(7 * time.Second) before printing "Done"

	// run above function run(), run2() and run3() concurrently
	go run() // this function will be run in a new thread
	go run2() // this function will be run in a new thread
	go run3() // this function will be run in a new thread

	time.Sleep(7 * time.Second)
	fmt.Println("Done")
}
