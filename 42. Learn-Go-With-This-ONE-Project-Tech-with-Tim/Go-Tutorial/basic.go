package main

import "fmt"

func getName() string {
	name := ""
	fmt.Printf("Enter your name: ")
	_,err := fmt.Scan(&name)
	if err != nil { // nil is like the None type in go
		fmt.Println(err)
		return ""
	}
	fmt.Printf("Hello %s\n",name)
	return name 
}

func main() {
	fmt.Println("Hello World!")
	fmt.Printf("Hello %s\n","Ankit")

	name := getName()
	fmt.Println(name)

}