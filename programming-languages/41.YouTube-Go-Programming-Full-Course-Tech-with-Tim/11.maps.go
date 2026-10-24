package main

import "fmt"

func main() {
	// we can create the map somelike this:
	//var mp map[string]int = map[string]int{"ankit": 1, "amit": 2, "ayush": 3}
	// another simple way
	mp := map[string]int{"ankit": 1, "amit": 2, "ayush": 3}
	fmt.Println(mp)
	// empty map can by made using `mp := make(map[string]int)`
	mp1 := map[string][]int{"a":{1,2,3}, "b":{4,5,6}}
	mp1["c"] = []int{7,8,9} //key-value pair
	// to override "c" with empty slice
	mp1["c"] = []int{}
	fmt.Println(mp1)
	// to delete a key-value pair
	delete(mp1, "c") // it is in-place function unlike append
	fmt.Println(mp1)
	// to access a value
	fmt.Println(mp1["a"])
	// to check if a key is present
	val, ok := mp1["c"]
	fmt.Println(val, ok)

	mp2 := map[uint]uint{}
	n := 100

	for number :=1 ; number <= n; number++ {
		for d :=1; d<=5; d++{
			if number % d == 0 {
				mp2[uint(d)]++
			}
		}
	}

	fmt.Println(mp2) // {1:100,2:50, 3:33, 4:25, 5:20}: It means total 100 values are divisible by 1
	// total 50 values are divisible by 2
	// total 33 values are divisible by 3
	// total 25 values are divisible by 4
	// total 20 values are divisible by 5
}
