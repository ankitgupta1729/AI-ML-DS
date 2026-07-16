package main

// Using mutex, we are forcing the threads to wait for the other threads to execute or work 
// on this resource or field before they are able to do that.

import (
	"fmt"
	"sync"
)

type Counter struct {
	lock sync.Mutex
	value int
}

func count(counter *Counter, ch chan<- bool) {
	counter.lock.Lock()
	defer counter.lock.Unlock() // error handling strategy
	counter.value++
	fmt.Println(counter.value)
	ch <- true
}

func main() {
	counter := Counter{}
	ch := make(chan bool)
	for i := 0; i < 100; i++ {
		go count(&counter, ch) // we are creating 100 go routines that are going to allow us
		// to count to 100
	}
	for i := 0; i < 100; i++ {
		<-ch
	}
	}