package main

import "fmt"

func main() {
	x := 2
	y := 3
	z1 := x<y
	z2 := x>y
	z3 := x==y
	z4 := x!=y
	z := z1 && z2 && z3 && z4
	fmt.Println(z1)
	fmt.Println(z2)
	fmt.Println(z3)
	fmt.Println(z4)
	fmt.Println(z)

	if x <3 {
		fmt.Println("x is less than 3")
	} else if x < 5 {
		fmt.Println("x is less than 5")
	} else if x < 7 {
		fmt.Println("x is less than 7")
	} else {
		fmt.Println("x is greater than or equal to 7")
	} 


	// logical operators &&, ||, !
	p := true
	q := false
	fmt.Println(p && q)
	fmt.Println(p || q)
	fmt.Println(!p)

}