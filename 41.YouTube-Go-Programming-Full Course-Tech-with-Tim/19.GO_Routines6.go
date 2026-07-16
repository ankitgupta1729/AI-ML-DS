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
	x := <- ch
	go add(8,11,ch)
	x = <- ch
	go add(5,0,ch)
	x = <- ch
	go add(5,-5,ch)
	x = <- ch
	fmt.Println(x)
}

// Here we scheduled the go routines in order. 