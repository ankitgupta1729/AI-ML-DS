package main

import "fmt" // this package allows to output things in console

func main() { // entry point of the program, if we write "Main" instead of "main" then it will give error
	// fmt.Println("Hello World!") // print "Hello World"  
}

// Run this code in terminal by typing "go run 1.demo.go", it first creates a temporary compiled file of the program
// and then runs this compiled file using CPU. It is kind of 2 steps. If we use "go build 1.demo.go" then it will create 
// an executable file instead of compiled file and then we can run this executable file by typing "./1.demo".

// we can give this compiled file to anyone and who can run the code without installing go on their computer.




// If we write the code as:

/*
func main() { // entry point of the program, if we write "Main" instead of "main" then it will give error
	// fmt.Println("Hello World!") // print "Hello World"  
}
*/
// then after running this code using "go run 1.demo.go" it will give error as "# command-line-arguments
// ./1.demo.go:3:8: "fmt" imported and not used" because fmt is not imported, so in go, it is not allowed and 
// even we can't build this code using "go build 1.demo.go" because fmt is not imported.

