package main

import "fmt"

// When we use a buffered channel, we will wait for a certain numbers of values to be 
// added on to the channel before we start having a blocking operation. So, we can make
// the channel to have a certain size.

func main() {
	ch := make(chan bool, 2) // creating a buffered channel
	ch <- true // sending something to this channel
	<-ch // receiving something from this channel
	fmt.Println("Done")
} 