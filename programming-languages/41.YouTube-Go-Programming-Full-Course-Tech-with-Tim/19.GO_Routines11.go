package main

import (
	"fmt"
	"time"
)

// here we will learn about mutex and lock

// Here, I am doing is attempting to count to 100 using 100 different go routines. 

type Counter struct {
	value int
}

func count(counter *Counter) {
	counter.value++
	fmt.Println(counter.value)
}

func main() {
	counter := Counter{0}

	for i := 0; i < 100; i++ {
		go count(&counter) // we are creating 100 go routines that are going to allow us 
		// to count to 100
	}
	time.Sleep(time.Second * 2)
}

// here we are getting weird output may be of same value in different order of values 
// because we don't know the order in which these different threads are going to be executed.
// And what happens, they're all kind of accessing the "value" field of "counter" struct at the
// exact same time. This is a big issue in multi-threaded programs when you have multiple threads
// accessing the same memory address location at the same time. When that occurs, then threads 
// can be changing and modifying things and can result in some really weird behavior. When 
// thread one is changing the "value" to 1 then thread 2 immediately change it to zero.

// We fix it by using mutex or lock. 

// A lock is something that we can acquire and release on some resource or value. 

// mutex and lock are pretty much synonymous and we will implement it in next code file. 