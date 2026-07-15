package main

import "fmt"

// An interface is a way for us to abstract on top of structs.

// What I mean by this is that we can create an interface 
// and this interface will define a series of methods that 
// various structs must implement. If a struct wants to implement
// the interface, it must have all of the different methods that interface defines.

// And that means that we are able to view that struct as the type
// of interface. 

// Interfaces are not things that we are going to instantiate. 
// I don't create an instance of an interface. Nothing is going 
// to be the shape interface below. But my other structs 
// will implement this interface that allowing me to treat them 
// as if they were a shape. 

// So, inside my interface, I define a bunch of different methods.
// these methods are things again that structs that implement the interface must implement.

type shape interface {
	getPerimeter() uint
}

func (s square) getPerimeter() uint {
	return s.width * 4
}

type Triangle struct {
	a uint
	b uint
	c uint
}

type square struct {
	width uint
}

func (t Triangle) getPerimeter() uint {
	return t.a + t.b + t.c
}

// Now, triangle implements our shape interface. 

func (t Triangle) getSides() []uint {
	return []uint{t.a, t.b, t.c}
}

func isEvenPerimeter(shape shape) bool {
	return shape.getPerimeter() % 2 == 0
}

func main() {
	//var s shape = Triangle{3, 4, 5}
	// once I have defined shape for s then I can only use the methods 
	// that interface defines i.e. getPerimeter and not getSides.
	//fmt.Println(s)
	//fmt.Println(s.getPerimeter())
	// now create more structs so that we can use interface more below

	// or we can modify the above line  to use it for shapes as:

	var shapes []shape = []shape{Triangle{3, 4, 5}, square{4}}
	perimeters := uint(0)

	for _, shape := range shapes {
		perimeters += shape.getPerimeter()
	}
	fmt.Println(perimeters)
}

