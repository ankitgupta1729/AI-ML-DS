package main

import "fmt"

// In go, most of the errors are caught at compile time, meaning we can't run our code unless we fix a majority of these issues.
// However there is still runtime errors. Now, a runtime error will occur when something happens during the execution of our code
// that we can't catch at compile time. For example, we can't divide by zero because we are trying to divide a number by zero.
// However, we can catch this error at runtime. These are called "panics" in go.

func defferedFunc(){
	fmt.Println("defer")
} 

func main() {
	// x := 2
	// y := 0
	// fmt.Println(x / y) // runtime error
	// if we write fmt.Println(1/0) then compiler will catch this error.
	// panic("this caused a crash")

	// What the defer keyword does is that it defers the execution of a function until the end of some specific function.
	//defer defferedFunc()
	//fmt.Println("run")

	// defer will run no matter what. So even if a panic occurs the defer statement will still happen. The reason why this is important
	// is because we can use this defer statement kind of like a dot.finally block that we had in java where this allows us to clean up 
	// some type of operation even if a crash of our program occurs.

	// So, as a great example, what we might be doing is something like opening a file. We open a file and then we attempt to write 
	// to the file.

	// Now, while we are writing to the file, something can happen. Maybe other program is using that file, we could have error and 
	// panic could be caused. If that's the case, I want to make sure that I close this file before I exit out this program.
	
	// So, I would defer operation that closes the file. And that means even if I am writing to the file, an error occurs, we 
	// will still end up closing the file. Whereas if I didn't defer that and I just put it say at the end of my program, what's
	// going to happen is if an error occurs, we won't reach that code because the panic happened first. 
	
	// So, anything after the panic, that's not deferred is not going to run. 

	// So, anything after the panic will not run.
	
	defer defferedFunc()
	panic("this caused a crash")
	fmt.Println("run")

}
