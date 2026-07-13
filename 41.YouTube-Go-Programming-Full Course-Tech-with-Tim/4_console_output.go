package main

import "fmt"

// fmt package stands for format, it is a package that allows us to output things to console.
// We use it to well format our output and to create specific strings.

// In fmt.Println(), Println() stands for print line. It automatically prints newline "\n" at the end of the line.
// Also put spaces between arguments of this function.

// Like Println(), Printf() stands for print formatted and this allows us to print out specifically
// formatted strings.

// for Printf(), we need "\n" for new line because by default it doesn't print new line.

func main() {
	x:=2
	fmt.Println("Hello",2,x)
	y := false
	fmt.Printf("%T\n",y) // %T is a formatted string and y is passed as an argument. 'T' stands for type
	fmt.Printf("%T %T\n",y,y)
	fmt.Printf("The value of y is:%v\n",y) // %v is a formatted string and y is passed as an argument. 'v' stands for value
	z:=10
	fmt.Printf("%b\n",z) // b stands for binary representation

	a := 2.23454453535353
	fmt.Printf("%e\n", a) // e represents scientific notation
	fmt.Printf("%f\n", a) // f represents float
	fmt.Printf("%.2f\n",a) // .2f represents float with 2 decimal places of precision
	fmt.Printf("%10.2f\n",a) // 10.2f represents float with 2 decimal places of precision and total 10 places
	fmt.Printf("\"%10.2f%%\n",a) // for % sign we have to use %% and \" represents double quotes due to escape sequence
	t:=fmt.Sprint("\"%10.2f%%\n",a) // Sprint() is a function that creates a string for us but not print it out. 
	fmt.Println(t, t, t)

	b:="hello"
	fmt.Printf("%s",b) // s represents string

}