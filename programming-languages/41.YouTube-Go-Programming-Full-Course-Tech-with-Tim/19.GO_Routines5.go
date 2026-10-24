package main

import (
	"fmt"
)

func add(x int, y int,ch chan int) {
	fmt.Println(x + y)
	ch <- x + y
}

func main() {
	ch := make(chan int)
	go add(5,10,ch)
	go add(8,11,ch)
	go add(5,0,ch)
	go add(5,-5,ch)
	x := <- ch
	x = <- ch
	x = <- ch
	x = <- ch
	fmt.Println(x)
}

// the above 4 go routines are running at exact same time in separate threads. So, we need to 
// write x := <- ch 4 times to get the value from the channel and print all the resultant values.
// but values can be printed in any order because we don't know how our threads are going to 
// be scheduled on the CPU. To make it in order, check next code file.

