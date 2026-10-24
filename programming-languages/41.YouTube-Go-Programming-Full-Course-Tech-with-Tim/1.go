package main// every time we create a go file then we have to give extension ".go" and then we always need to declare a package "main".

import "fmt"

// This package allows us to actually output things to console and you can see below the "fmt.Println()".

func main() 
{ // this is the entry point of the program. "main" and "Main" both are different.
	fmt.Println("Hello World!") // print line function "println()" prints "Hello World!"
}

// Run this code using "go run 1.go" in the current working directory in terminal.

// When you run this code then it takes few seconds. Now it took this time because go run command is creating a temporary 
// compiled file of this program. Then it's running this temporary compiled file using our CPU. It's kind of doing 2 steps in one.
// However we have another command that can just build the compiled file. And then we can directly execute that file if we want.

// Here, "go build 1.go" will create an exe file for me on windows and different file on mac or linux. Them execute this exe file using "1.exe" on windows
// and "./1" on mac or linux.

// The good thing about compiled or executable file is that we can give it to anyone like mother, father etc. and they can run without installing go.

//  If I comment out "fmt.Println("Hello World!")" then it will give output as:

// 🍎 ankit@MacBook-Air 💻  …/AI-ML-DS/41.YouTube-Go-Programming-Full Course-Tech-with-Tim on  main [ ?3  ] 🐍  v3.14.2 via  v1.26.0 
// ╰─ go run 1.go  
// # command-line-arguments

// this is type of error because without uncommenting "fmt.Println("Hello World!")" then it will give error and will not create 
// a compiled file using "go build 1.go".

// So, Go is more stricter than javascript and can catch the errors easily.