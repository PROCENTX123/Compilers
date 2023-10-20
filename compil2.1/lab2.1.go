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
	if file, err := parser.ParseFile(fset, "test.go", nil, parser.ParseComments); err == nil {
		insertIndPost(file)

		if format.Node(os.Stdout, fset, file) != nil {
			fmt.Printf("Formatter error: %v\n", err)
		}
	} else {
		fmt.Printf("Errors in %s\n", os.Args[1])
	}
}
