package main

import "fmt"

func main() {
	x := -9
	y := uint(x) // converting x to uint8, which will wrap around and give a large positive number
	fmt.Println(x,y)
}