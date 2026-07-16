package main

import (
	"fmt"
	"time"
)

// There is a way that we can wait for a goroutine to finish running.

func add(x int, y int,ch chan int) {
	time.Sleep(5 * time.Second) // will wait for 5 seconds to generate the output from main 
	// function 
	ch <- x + y
}

func main() {

	// when we want to get return values from go routines, is used something known as channel.
	// A channel is a special way that we can pass values between different go routines and 
	// we are allowed to send values on a channel and wait for values to be received. This 
	// allows us to implement something known as blocking code.
	
	ch := make(chan int) // creating the channel

	// Now, we need to do is we need to give this channel to our go routine.

	// we can not simply get a return value from a go routine. What we need to do instead 
	// is: pass that on something known as a channel. The channel allows us to synchronize 
	// and wait for different values to be returned.

	go add(5,10,ch) // passing the channel to the go routine
	x:= <- ch // this line known as blocking code
	fmt.Println(x)
}