package main

import "fmt"

type Person struct {
	Name string // Writing "Name" makes it public so that anyone cas access and if we write "name" it will be private/protected as in Java 
	Age  uint // Writing "Age" makes it public so that anyone cas access and if we write "age" it will be private/protected as in Java
}

func (p Person) getName() string { // here we pass the struct Person in this function
	return p.Name
}

// getName() is not exported name but GetName() is exported name so that I can access it outside of package
// same for setName()

func (p Person) setName(newName string){ // This function modifies the fields of our struct
	p.Name = newName
	fmt.Println(p)
}

func main() {
	var p1 Person = Person{Name: "John Doe", Age: 30}
	value := p1.getName()
	fmt.Println(value)
	p1.setName("Tim")
	fmt.Println(p1) // we pass the copy of struct in the function but it does not change the original struct
}
