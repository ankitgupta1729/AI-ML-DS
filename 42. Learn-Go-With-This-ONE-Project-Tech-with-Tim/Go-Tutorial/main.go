package main

import (
	"fmt"
	"math/rand"
)
func getBet(balance uint) uint {
	var bet uint
	for true {
		fmt.Printf("Enter your bet, or 0 to quit (balance = $%d): ",balance)
		fmt.Scan(&bet)
		if bet > balance {
			fmt.Println("Bet cannot exceed balance")
		}  else {
			break
		}
	}
	return bet
}

// Implementing slot machine
func generateSymbolArray(symbols map[string]uint) []string {
	symbolArr := []string{}
	for symbol,count := range symbols {
		for i := uint(0); i < count; i++ {
			symbolArr = append(symbolArr, symbol) 
		}
	}
	return symbolArr
} 

func getRandomNumber (min int, max int) int {
	return rand.Intn(max - min + 1) + min
}

// implementing random grid

func getSpin(reel []string, rows int, cols int) [][]string  {
	result := [][]string{}
	for i := 0; i < rows; i++ {
		result = append(result, []string{})
	}
	for col:=0 ; col <cols ; col++ {
		selected := map[int]bool{}
		for row :=0; row <rows ; row++ {
			for true{
				randomIndex := getRandomNumber(0, len(reel)-1)
				_,exists := selected[randomIndex]
				if !exists {
					selected[randomIndex] = true
					result[row] = append(result[row], reel[randomIndex]) 
					break
				}
			}
		}
	}
	return result
}

func printSpin(spin [][]string) {
	for _,row := range spin {
		for j, symbol := range row {
			fmt.Printf(symbol)
			if j != len(row)-1 {
				fmt.Printf(" | ")
			}
		}
		fmt.Println()
	}
}

func checkWin(spin [][]string, multipliers map[string]uint) []uint {
	lines := []uint{}

	for _,row := range spin {
		win := true
		checkSymbol := row[0]
		for _,symbol := range row[1:] {
			if symbol != checkSymbol {
				win = false
				break
			}
		}
		if win {
			lines = append(lines, multipliers[checkSymbol])
		} else {
			lines = append(lines, 0)
		}
	}

	return lines
}

func main () {

	symbols := map[string]uint{
		"A": 4,
		"B": 7,
		"C": 12,
		"D": 20,
	} // It shows in a wheel or column, how many times each symbol/character appears
	
	multipliers := map[string]uint{
		"A": 20,
		"B": 10,
		"C": 5,
		"D": 2,
	} 
	// it says how many times we bet , "A"'s frequency si 4 so it is rare and that's 
	// why it has many bets and others are mentioned accordingly. 

	symbolArr := generateSymbolArray(symbols)
	spin := getSpin(symbolArr, 3, 3)
	printSpin(spin)	

	balance := uint(200) // start the user with 200 dollars
	for balance > 0 {
		bet := getBet(balance)
		if bet == 0 {
			break
		}
		balance -= bet
		spin = getSpin(symbolArr, 3, 3)
		printSpin(spin)
		// check win, update balance
		winningLines := checkWin(spin, multipliers)
		// fmt.Println(winningLines)
		for i,multi := range winningLines {
			win := multi * bet
			balance += win
			if multi > 0 {
				fmt.Printf("You won $%d, (%dx) on line #%d\n",win,multi,i+1)
			}
		}
	}
	fmt.Printf("You left with, $%d\n",balance)
}