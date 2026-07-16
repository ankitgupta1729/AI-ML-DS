package main

import "fmt"

// Generics is a way that we can have flexible types in a statically typed language. 

func add(num1 int, num2 int) int {
	return num1 + num2
}

// Here , if we have to use uint or float for num1 and num2 then we have to write the same function again and again 
// for uint and float.

// To fix it, we can use generics. 

func addNumber[T int | float64](num1 T, num2 T) T {
	return num1 + num2
}

// so here T can be of int or float64.

func getValues[K comparable, V any](mp map[K]V)[]V{
	values := []V{}

	for _, value := range mp {
		values = append(values, value)
	}
	return values
}

// I have written a generic getValues function which can iterate through any map and return to me all of the values inside of 
// that map.

func main() {
	fmt.Println(addNumber(1,2))
	fmt.Println(addNumber(1,2.3))
	
	mp := map[string]int{"ankit": 1, "amit": 2, "ayush": 3}
	fmt.Println(getValues(mp))
}