package main

import "fmt"

// Arrays are fixed-sized data structure that stores values of the same type
// Type of an array indicates its size

func main() {
	var arr [5]int // we can't change the size later as it is fixed-sized array
	fmt.Println(arr) // [0 0 0 0 0]
	var arr1 [5]bool
	fmt.Println(arr1) // [false false false false false

	// implicit assignment
	arr2 := [5]int{1,2,3,4,5}
	fmt.Println(arr2) // [1 2 3 4 5]

	// nested array
	arr3 := [3][3]int{{1,2,3},{4,5,6},{7,8,9}}
	fmt.Println(arr3) // [[1 2 3] [4 5 6] [7 8 9]]
	fmt.Printf("%T\n",arr3)

	// nested array with another way where compiler check the size from counting its elements
	arr4 := [...][3]int{{1,2,3},{4,5,6},{7,8,9}}
	arr4[0] = [3]int{'A','B','C'}
	fmt.Println(arr4) // [[1 2 3] [4 5 6] [7 8 9]]
	fmt.Printf("%T\n",arr4)
	fmt.Println(len(arr4))

	// looping in array

	for i,value := range arr4 {
		fmt.Println(i,value)
	}

	// nested looping in array

	for i,value := range arr4 {
		for j,v := range value {
			fmt.Println(i,j,v)
		}
	}
	//passing array to a function
	arr5 := [...][2]int{{1,2},{3,4},{5,6}}
	test(arr5)
	fmt.Println(arr5) // array will not be mutated like in javascript. Here in test function, we are 
	// mutating the copy of the array not the original array but when we talk (flexible version of array) 
	// then things will be changed
}

// Passing array to a function

func test(arr [3][2]int){
	arr[0] = [2]int{100,200}
}