package main

import "fmt"


	// uint - default unsigned integer(only positive), other similar data types can be uint8,uint16, uint32, uint64
	// For uint32, total unique values = 2^32 and range of values are: min: 0, max: 2^32-1
	// int - signed integer (positive and negative both). other similar data types can be 
	// int8, int16, int32, int64.
	// For int8, total unique values = 2^8 and range of values are: min: -2^(8-1)=-128, max: 2^(8-1)-1=127

	// float32, float64 -  to store decimal values in 32 and 64 bits respectively
	// byte: this type is equivalent to int8 and we can store the character like 'a' here that can be represented by 1 byte.
	// rune: this type is equivalent to int32 and we can store the character like 'a' here that can be represented by 4 bytes. 
	// bool: Here we can store only true or false values.
	// string: Here we can store text in double quotes and not single quotes.
	// nil: This is kind of equal to undefined or no. 
	
	// var x string = "Hello World!" // Here we defined the variable x like in javascript with type string.
	// We don't need semicolon here

func main() {
	var x string // By default if don't assign a value then empty string will be assigned to x. 
	var y string = "Hello World!"
	// var z uint8 = 10000 // overflow error
	var z uint8 = 100
	var a uint8 // default value is 0
	
	fmt.Println(x)
	fmt.Println(y)
	fmt.Println(z)
}