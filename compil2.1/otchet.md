% Лабораторная работа № 2.1. Синтаксические деревья
% 13 октября 2023 г.
% Григорьев Роман, ИУ9-62Б

# Цель работы
Целью данной работы является изучение представления синтаксических деревьев 
в памяти компилятора и приобретение навыков преобразования синтаксических деревьев.

# Индивидуальный вариант
Каждый оператор for вида for expr {...} преобразовать
в оператор for fmt.Println("init"); expr; fmt.Println("next") {...}.


# Реализация

Демонстрационная программа:

```go
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
```

Программа, осуществляющая преобразование синтаксического дерева:

```go
package main

import (
	"fmt"
	"go/ast"
	"go/format"
	"go/parser"
	"go/token"
	"os"
)

func insertIndPost(file *ast.File) {
	ast.Inspect(file, func(node ast.Node) bool {
		//Проверка for
		if forStmt, ok := node.(*ast.ForStmt); ok {
			// Проверка инициализатора и пост-условия
			if forStmt.Init == nil && forStmt.Post == nil {
				//Если их нет то добавляем
				initStmt := &ast.ExprStmt{
					X: &ast.CallExpr{
						Fun: &ast.SelectorExpr{
							X:   ast.NewIdent("fmt"),
							Sel: ast.NewIdent("Println"),
						},
						Args: []ast.Expr{&ast.BasicLit{
							Kind:  token.STRING,
							Value: "\"init\"",
						}},
					},
				}
				forStmt.Init = initStmt

				postStmt := &ast.ExprStmt{
					X: &ast.CallExpr{
						Fun: &ast.SelectorExpr{
							X:   ast.NewIdent("fmt"),
							Sel: ast.NewIdent("Println"),
						},
						Args: []ast.Expr{&ast.BasicLit{
							Kind:  token.STRING,
							Value: "\"next\"",
						}},
					},
				}
				forStmt.Post = postStmt
			}
		}
		return true
	})
}

func main() {

	fset := token.NewFileSet()
	if file, err := parser.ParseFile(fset, "test.go",
	 nil, parser.ParseComments); err == nil {
		insertIndPost(file)

		if format.Node(os.Stdout, fset, file) != nil {
			fmt.Printf("Formatter error: %v\n", err)
		}
	} else {
		fmt.Printf("Errors in %s\n", os.Args[1])
	}
}

```

# Тестирование

Результат трансформации демонстрационной программы:

```go
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


```

# Вывод
В ходе выполнения данной лабораторной работы, я освоил работу с синтаксическими деревьями
в языке программирования Go и использовал инструменты go/ast и go/parser для этой цели.
С их помощью была создана программа, способная изменять синтаксическое дерево программы и,
таким образом, вносить модификации в исходный код. Эта программа принимает входной файл с
кодом на языке Go и генерирует новую, измененную версию этой программы в
качестве выходного результата.
