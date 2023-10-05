package main

import "fmt"

func main() {
	i := 0
	j := 10
	for i < 5 {
		i++
		fmt.Println(i)
	}

	for j > 5 {
		j--
		fmt.Println(j)
	}
}

//package main
//
//import "fmt"
//
//func main() {
//	for i := 0; i < 5; i++ {
//		fmt.Println(i)
//	}
//
//	for j := 10; j > 5; j-- {
//		fmt.Println(j)
//	}
//}

//package main
//
//import "fmt"
//
//func main() {
//	for i := 0; i < 5; {
//		i++
//		fmt.Println(i)
//	}
//
//	for j := 10; j > 5; {
//		j--
//		fmt.Println(j)
//	}
//}
