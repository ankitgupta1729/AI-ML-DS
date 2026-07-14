package main

import "fmt"

// In switch case, if first condition is true then rest will be ignored
// But using fallthrough keyword we can execute the next case as well

func main() {
	x := 2
	switch x {
	case 1:
		fmt.Println("x is 1") // break statement is automatically executed in go
	case 2:
		fmt.Println("x is 2")
	case 3:
		fmt.Println("x is 3")
	default:
		fmt.Println("x is not 1, 2, or 3")
	}
	switch {
	case x <= 2:
		fmt.Println("x is 1")
	case x == 2:
		fmt.Println("x is 2")
	case x == 3:
		fmt.Println("x is 3")
	default:
		fmt.Println("x is not 1, 2, or 3")
	}
	switch {
	case x <= 2:
		fmt.Println("x is 1")
		fallthrough
	case x == 2:
		fmt.Println("x is 2")
	case x == 3:
		fmt.Println("x is 3")
	default:
		fmt.Println("x is not 1, 2, or 3")
	}
	a :=-1
	switch {
	case a < -1:
		fmt.Println("a is less than -1")
		fallthrough
	case a<0:
		fmt.Println("a is less than 0")
		fallthrough
	case a<1:
		fmt.Println("a is less than 1")
	default:
		fmt.Println("default")
	}

	character := "h"
	switch character {
		case "a", "e", "i", "o", "u":
			fmt.Println(character, "is a vowel")
		default:
			fmt.Println(character, "is not a vowel")
	}

}