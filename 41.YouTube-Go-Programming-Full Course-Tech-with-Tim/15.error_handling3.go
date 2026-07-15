package main

import ("fmt"
"errors"
)

func divide (x, y int) (int, error) {
	if y == 0 {
		return 0, errors.New("cannot divide by zero")
	}
	return x / y, nil
}

func main() {
	x := 2
	y := 0
	z, err := divide(x, y)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(z)
}