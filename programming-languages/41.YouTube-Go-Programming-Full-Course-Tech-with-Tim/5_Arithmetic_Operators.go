package main

// Arithmetic operators in go are pretty much same as in Javascript. 

/*

Operators in Go:
+
-
*
/
--
++
%
we don't perform exponentiation using ** in Go 
*/

import (
	"fmt"
	"math"
	"strconv"
)
// multiple packages can be imported using "import" keyword and separated on each line

func main() {
	x:=7 // here x:=uint8(7) would not work because type should be same on left and right side while performing arithmetic operation. 
	// because if type is not same then go confuses what should be the type for resultant variable.
	y:=2
	z:=x+y
	fmt.Println(z)
	a:= uint8(7)
	b:=1000
	c:= a+uint8(b)
	fmt.Println(c) // c=239 which is weird because we have converted a large value to a smaller values using uint8(b)
	d := int(a)+b
	fmt.Println(d) // this is correct thing to do. Remember that convert always smaller type to larger type
	// so that you won't lose information in something called as overflow. Also make sure type should be same on both sides. 
	m:=1000
	n:=7
	o:=float64(m)/float64(n) // to get the correct decimal or floating point value, use float64 in numerator and denominator both 
	fmt.Println(o)

	// string concatenation
	s1:="Hello"
	s2:="World"
	s3:=s1+s2
	s4:=2
	s5:=s1+string(s4)
	s6:=s1+fmt.Sprint(s4)
	fmt.Println(s3)
	fmt.Println(s5)
	fmt.Println(s6)

	num:=4
	num--;
	res := num%3
	println(num)
	fmt.Println(res)

	// use math package for math operations
	fmt.Println(math.Min(2,3))
	fmt.Println(math.Max(2,3))
	fmt.Println(math.Sqrt(3))
	fmt.Println(math.Pow(2,3)) // to use exponentiation in go
	fmt.Println(math.Round(2.456))
	fmt.Println(math.Ceil(4.234))
	fmt.Println(math.Floor(4.234))

	// convert string to integer
	s:="123"
	i,err:=strconv.Atoi(s)
	fmt.Println(i)
	fmt.Println(err)

	s1="1234hello"
	i1,err1:=strconv.Atoi(s1)
	fmt.Println(i1)
	fmt.Println(err1)

	// convert integer to string
	i=123
	s=strconv.Itoa(i)
	fmt.Println(s)
}