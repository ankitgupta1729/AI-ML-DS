package main

import "fmt"

// Pointers and references (both used synonymously in go) allow us to view memory address locations id where something exists.
// as well as to modify what's held at that location.

func change(x int) {
	x = 100
}

func change1(x *int) {
	*x = 100
}

func change2(x *int) {
	*x = 100
}

// Modify structs using pointers
type Book struct {
	id int
	title string
}

func (b *Book) setTitle(newTitle string) {
	b.title = newTitle
}

func test(pointerSlice *[]*int){
	values := *pointerSlice 

	for _,value := range values{
		*value = 100
	}
}

func main() {
	x := 10
	y := &x
	fmt.Println(x, y, *y)
	*y = 20
	fmt.Println(x, y, *y)
	a:=10
	change(a)
	fmt.Println(a) // a=10 because change function doesn't change the value of a
	b:=10
	change1(&b) // pass the memory address of b
	fmt.Println(b) // b=100 because change1 function changes the value of b using pointer
	c:=10
	change2(&c) // pass the memory address of c
	fmt.Println(c) // c=100 because change2 function changes the value of c using pointer and outside of the function the value of c is 100
	// here we affecting 'a' outside of main function

	// changing structs using pointers
	b1 := Book{1, "Book1"}
	fmt.Println(b1)
	b1.setTitle("Book2") // or you can write `(&b1).setTitle("Book2")`
	fmt.Println(b1)

	// pointers to pointers
	x1 := 10
	y1 := &x1
	fmt.Println(x1, y1, *y1)
	z1 := &y1
	fmt.Println(x1, y1, *y1, z1, *z1, **z1)
	fmt.Printf("%T\n", z1)

	// pointers to slices
	p:=1
	q:=2
	values := &[]*int{&p, &q}
	fmt.Println(*values)
	test(values)
	fmt.Println(*values)
}