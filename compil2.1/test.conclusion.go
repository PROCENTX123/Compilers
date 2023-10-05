package main

import "fmt"

func main() {
	i := 0
	j := 10
	for fmt.Println("init"); i < 5; fmt.Println("next") {
		i++
		fmt.Println(i)
	}

	for fmt.Println("init"); j > 5; fmt.Println("next") {
		j--
		fmt.Println(j)
	}
}
