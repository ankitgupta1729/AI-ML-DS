package main

import "fmt"

func add(num1 int, num2 int) (int,string) {
	return num1 + num2, "hello"
}

func callFunc(callable func(int) int) int{ // function inside a function
	return callable(10)
}

func doubleNumber(num int) int {
	return num * 2
}

func tripleNumber(num int) int {
	return num * 3
}

// Return function from a function

func getFunc(str string) func(string) string {
	return func(str2 string) string {
		return str + str2
	}
} 

// Variadic function: Function which takes variable number of arguments
func sum(nums ...int) int { // it accepts any number of numbers
	total := 0
	for _,num := range nums {
		total += num
	}
	return total
}

// named return value
func sum1(nums ...int) (total int) { // it accepts any number of numbers and we can also 
// return many number of outputs as total int, total1 int etc.
	for _,num := range nums {
		total += num
	}
	return
}

func main() {
	//value,str := add(1,2)
	//fmt.Println(value,str)


	// function inside a function
	//value := callFunc(doubleNumber)
	//fmt.Println(value)
	//fmt.Printf("%T",doubleNumber)

	// Anonyomus function -- unnamed function
	//value := callFunc(func(x int) int {
	//	return x+1
	//})
	//fmt.Println(value)

	// return function from a function
	f1 := getFunc("Hello")
	value := f1("World")
	value2 := f1("Go")
	fmt.Println(value,value2)
	fmt.Printf("%T\n",getFunc)

	s := sum(1,2,3,4,5)
	// we can also write it in another way as
	s1 := sum([]int{1,2,3,4,5}...)
	fmt.Println(s)
	fmt.Println(s1)

	s2 := sum1(1,2,3,4,5)
	fmt.Println(s2)

}