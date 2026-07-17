package main

// Buffered channel

import (
	"fmt"
)

func main (){
	ch := make(chan bool)
	ch <- true // sending something to this channel
	<-ch // receiving something from this channel
	fmt.Println("Done")
}

// Here, we are getting the deadlock error. Whenever we have the send on a channel 
// i.e. ch <- true, this is actually a blocking operation that waits for the channel to  
// receive the value true. Every single send that we have is waiting for a value to be received.

// So, when I do send operation ch <- true above, we don't actually move on to the next line. 
// We don't continue in this go routine until we see the receive block <-ch in another go routine.

// So, this ch<-true is blocking until we receive and same with receive, it's blocking until
// a value is sent onto the channel. This happens in a unbuffered channel. Unbuffered channel is
// a channel that have one value on it at a time. We can avoid it using a buffered channel in the next code file.  