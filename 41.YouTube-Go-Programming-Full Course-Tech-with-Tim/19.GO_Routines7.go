package main

import (
	"fmt"
)

func add(x int, y int,ch chan int) {
	ch <- x + y
}

func main() {
	ch := make(chan int)
	ch2 := make(chan int)
	go add(5,10,ch)
	go add(20,15,ch2)
	x := <- ch
	y := <- ch2
	fmt.Println(x)
	fmt.Println(y)
}

// Here, go routines can be executed in any order, so 2nd go routine can be executed before 
// 1st go routine.