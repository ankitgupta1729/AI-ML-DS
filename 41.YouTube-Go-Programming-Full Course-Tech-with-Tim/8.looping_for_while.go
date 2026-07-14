package main

import "fmt"

// In go, we don't have while loop, we use for loop like syntax to create while loop

// ASCII encoding = 1 byte = 256 characters
// UTF-8 encoding = 4 bytes 
// Generally we use UTF-8 encodings for many things like emojis, special characters like - etc.


func main(){
	
	// for loop
	for idx :=0 ; idx < 10 ; idx++ {
		fmt.Println(idx)
	}
	// while loop
	idx := 0
	for idx < 10 {
		fmt.Println("loop")
		idx++
	}

	str := "hello world"
	fmt.Println(str[0]) // integer representation of the character
	fmt.Printf("%T\n",str[0]) // every character is a byte type which is uint8
	fmt.Println(string(str[0])) // character representation of the integer

	str1 := "-"

	for idx := 0; idx < len(str1); idx++ {
		fmt.Printf("%c\n", str1[idx])
	} 

	str2 := "hello world"

	for idx := 0; idx < len(str2); idx++ {
		fmt.Printf("%c", str2[idx])
	} 
	fmt.Printf("\n")	
	// for strings with emojis
	str3 := "hello world 😀"

	for _, char := range str3 { // _ is a placeholder which takes 
	// the value from range and char takes the values from str3
		fmt.Printf("%c\n", char)
		// fmt.Printf("%T", char) it is int32 which is of rune type
		// break and continue statements we can use here like in javascript
	}	
}