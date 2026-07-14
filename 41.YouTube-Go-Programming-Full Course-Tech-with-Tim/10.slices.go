package main

import "fmt"

// Slices are a much more flexible version of arrays

// Slice is a view of an array. So, you always have an array and slice allows you to view 
// different portion of that array and then to kind of increase or decrease the capacity of
// that array.

// To make a slice we can either have an array that we take a slice of or we can create a slice
// from scratch that will automatically create an array for us.

func main() {
	arr := [5]int{1,2,3,4,5}
	slice := arr[1:4]
	slice1 := arr[2:]
	slice2 := arr[:3]
	fmt.Println(slice) // [2 3 4]
	fmt.Println(arr) // [1 2 3 4 5]
	fmt.Println(slice1) // [3 4 5]
	fmt.Println(slice2) // [1 2 3]
	fmt.Println(slice[0]) // 2
	slice[0] = 100
	fmt.Println(arr) // [1 100 3 4 5]

	// When we have a slice, we have 3 properties:
	// Pointer = where the slice is pointing to first element in my slice is in the underlying array
	// length = how many elements in the slice
	// capacity = it is how much larger I could make the slice from the pointer where it points to
	// to the end of the array
	fmt.Println(arr) // [1 100 3 4 5]
	fmt.Println(slice2) // [1 100 3]
	fmt.Println(len(slice2)) // 3
	fmt.Println(cap(slice2)) // 5
	// here pointer --> arr[0] in case of slice2 and in case of slice1 it will be arr[2] and 
	// in case of slice it will be arr[1]

	fmt.Println(arr) // [1 100 3 4 5]
	fmt.Println(slice1) // [3 4 5]
	fmt.Println(len(slice1)) // 3
	fmt.Println(cap(slice1)) // 3

	// slice of the slice
	slice3 := slice1[1:]
	fmt.Println(slice3) // [4 5]
	fmt.Println(len(slice3)) // 2
	fmt.Println(cap(slice3)) // 2

	// create a new slice without creating the underlying array
	slice4 := []string{"hello", "world"}
	// here an array will be created and pointer for this slice will point to that array
	fmt.Println(slice4) // [hello world]
	fmt.Printf("%T\n",slice4) // []string
	fmt.Println(len(slice4)) // 2
	fmt.Println(cap(slice4)) // 2
	
	s1 := []string{"hello", "world"}
	for x:=0 ; x<10 ; x++ {
		s1 = append(s1, "tim") // append after checking the capacity of the slice
		// initially for slice s1, capacity is 2 so to append "tim", it will create a new slice 
		// by doubling the capacity of slice so that "time" can be appended. Similarly append
		// in the same way further.
		fmt.Println(s1, len(s1), cap(s1)) 

	// To create am empty slice of length 10 and size 20, we can write something like using 
	// make() function as `s1 := make([]int, 10, 20)`
	}

	// iterate over the slice
	s2 := []string{"hello", "world","hi"}
	for i, value := range s2 {
		fmt.Println(i,value)
	}
	
	// Passing this slice to a function
	test(s2)
	fmt.Println(s2)

}

func test(arr []string){
	arr[0] = "changed it"
}

