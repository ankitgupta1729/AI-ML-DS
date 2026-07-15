package main

import "fmt"

// structs inside structs or embedded structs

type Sport struct {
	name string
	position string
}
type Person struct {
	name string
	age  uint
	favSport Sport
}

func main() {
	p1 := Person{
		name: "John Doe",
		age: 30,
		favSport: Sport{
			name: "Basketball",
			position: "Point Guard",
		},
	}
	fmt.Println(p1)
	fmt.Println(p1.name)
	fmt.Println(p1.age)
	fmt.Println(p1.favSport)
	fmt.Println(p1.favSport.name)
	fmt.Println(p1.favSport.position)
}