package main

import (
	"fmt"
	"time"
)

// deadlock situation

// deadlock occurs when no threads are under execution
// here deadlock occurs because we are waiting for some value to be passed on the channel 
// in this go routine in x:= <- ch below.

// Here, we are blocking,waiting or stalling here and nothing gets returned. So, as soon as 
// we have no go routine in our program that are executing, nothing is happening in any of them,
// we get a deadlock which means we are deadlocked between different threads. One thread is 
// waiting for another thread and that thread is waiting for the same thread and we can't do
// anything. In this situation, we have one thread that's waiting for one thread to return 
// something it never has. So, be careful while writing these kind of programs. 

func add(x int, y int,ch chan int) {
	time.Sleep(5 * time.Second) 
	// ch <- x + y
}

func main() {
	ch := make(chan int)
	go add(5,10,ch) 
	x:= <- ch 
	fmt.Println(x)
}