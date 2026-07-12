// Implicit Assignment

// There is a special operator in GO that allows us to declare variables more quickly without
// having to explicitly define the type of the variable.

// var x uint8 = 2, here I am explicitly defining the type of x. It is explicit because I am
// writing its type. However we don't have to do that. We can actually use another operator in
// GO called implicit assignment operator which will assign a variable and then it will decide
// what the type of that variable is, still at compile time but based on the value that's being
// stored. Now, this can save you a significant amount of time when you are using mode complicated 
// types that we'll look at later. Example: y := 3 will be implicitly typed as int.   


package main

import "fmt"

func main() {
	var x uint8 = 2
	y := 3
	fmt.Println(x)
	fmt.Println(y)
	fmt.Printf("%T",y)
	// y=3 is still static and here if we change its type as y ="hello"
	// Just put the cursor on y:=3 and we can see its type as int

	z := 2.3
	fmt.Println(z)
	fmt.Printf("%T",z)

	a :=false
	fmt.Println(a)
	fmt.Printf("%T",a)
}