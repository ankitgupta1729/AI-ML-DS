package main

import "fmt"

// struct is similar to a class. It's kind of replacement to a class in languages like go.
// It does work differently but it allows us to do similar things to what we do with objects 
// and classes in javascript. 

// Now, a struct by definition is a typed collection of fields. When we create a struct that 
// allows us to create a new type that we can use within go. 

// So, this is quite helpful when you want to have a type that allows you to have something 
// like a string, an int, maybe a slice or store some information about some kind of entity 
// or object. 

// create a struct

type Person struct {
	Name string
	Age  uint
	f func(string) string // associating function with struct
	// and this function is going to be different for every instance of the struct. So if 
	// I create p2 then this function will be different for p2.
	// So, to resolve this we can add the function directly as a field value to the struct.
	// Some functions behave the same for every instance of the struct and for that we have to 
	// create a method as in 13.structs2.go
}



// passing struct to a function

func getName(p Person) string {
	return p.Name
}

func main() {
	// initialize a struct
	//p1 := Person{Name: "John Doe", Age: 30} // p1 := Person{} create an empty struct
	// reference to the struct object
	p1 := Person{Age: 30}
	p1.Name = "John Doe"
	fmt.Println(p1)
	fmt.Println(p1.Name)
	fmt.Println(p1.Age)

	p1.f = func(name string) string {
		return fmt.Sprintf("Hello %s", name)
	}
	fmt.Println(p1.f("John Doe"))

	// we can also use this as:
	var p2 Person = Person{Name: "John Doe", Age: 30} 
	name := getName(p2)
	fmt.Println(name)
}