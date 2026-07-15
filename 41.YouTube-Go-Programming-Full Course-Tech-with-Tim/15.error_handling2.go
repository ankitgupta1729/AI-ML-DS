package main

import "fmt"

func divide(x, y int) int {
	return x / y
}

// Now, let's see how to recover from the panic.

func defferedFunc(){
	fmt.Println("defer")
	r := recover() // this function can only be used inside a function that is deferred. It will catch any error that occurs
	// and save error message inside the "r" variable. 
	// What this actually do is allow us to not actually crash our program.
	fmt.Println(r)

	// Now, rest of the function that was executing will not continue to execute. 
}

func main() {
	defer defferedFunc()
	panic("this caused a crash") // if panic occurs then it goes to the deferred function and its body is executed and 
	// due to recover() function, program will be able to continue to be executed. 
	// instead of panic() statement, try divide(1,0) which is a runtime error(panic)
	fmt.Println("run")
}