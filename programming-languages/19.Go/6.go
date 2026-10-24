package main

import "fmt"

func main() {
	var x uint8 = 100 // explicitly typed as uint8
	var x1 uint8 // explicitly typed as uint8 but not assigned a value, so it will have the zero value of 0
	x1 = 200 // assigning a value to x1 after declaring it
	y := 8 // implicitly typed as int 
	z := 3.14 // implicitly typed as float64
	s := "Hello, Go!" // implicitly typed as string
	fmt.Println(x)
	fmt.Println(x1)
	fmt.Println(y)
	fmt.Println(z)
	fmt.Println(s)
	fmt.Printf("%T\n",y) // prints the type of y
	fmt.Printf("%T\n",z) // prints the type of z
	fmt.Printf("%T\n",s) // prints the type of s
}

// In Go, we can use implicit assignment operator which will assign a variable and then decide its type still at
// compile time but based on the value that's being stored.  

// we have to use explicitly typed variable when we want to specify the type of the variable and don't have to 
// give value to it, otherwise Go will infer the type based on the value assigned to it.