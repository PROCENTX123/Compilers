import abc
import parser_edsl as pe
import re
from dataclasses import dataclass


func = {}
checkVariablesMap = {}
boolVariable1 = False


class SemanticError(pe.Error):
    pass


class Element(abc.ABC):
    pass


class BadArgument(SemanticError):
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type

    @property
    def message(self):
        return f'в функцию передают неверный аргумент: {self.type.__name__}'


class DifferentSample(SemanticError):
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type

    @property
    def message(self):
        return f'несоответствие типов: {self.type.__name__}'


class VarRedefinition(SemanticError):
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type

    @property
    def message(self):
        return f'Переопределение переменной: {self.type}'


class VarNotExist(SemanticError):
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type

    @property
    def message(self):
        return f'Неопределенная переменная: {self.type.__name__}'


class VariableTypeIncorrect(SemanticError):
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type

    @property
    def message(self):
        return f'Некорректный тип переменной: {self.type}'


@dataclass
class Comment(Element):
    value: str

    def check(self):
        # print("comment")
        pass


class Value(abc.ABC):
    def getType(self):
        pass

    def check(self):
        pass


@dataclass
class Variable(Value):
    varname: str
    typeVarCoords: pe.Fragment

    @pe.ExAction
    def create(attrs, coords, res_coord):
        varname = attrs
        name = ""
        for cur in varname:
            name += cur
        typeVarCoords = coords
        return Variable(name, typeVarCoords)

    def check(self, example):

        if boolVariable1:
            if self.varname in checkVariablesMap:
                raise VarRedefinition(self.typeVarCoords, self.varname)
            else:
                checkVariablesMap[self.varname] = example
        else:
            if self.varname not in checkVariablesMap:
                raise VarNotExist(self.typeVarCoords, self.varname)
            if not checkVariablesMap[self.varname].equal(example):
                raise VariableTypeIncorrect(self.typeVarCoords, self.varname)

    def getType(self):
        return 'INT'


@dataclass
class IntValue(Value):
    typeVarCoords: pe.Fragment
    value: int

    @pe.ExAction
    def create(attrs, coords, res_coord):
        typeVarCoords = coords
        val = attrs[0]
        return IntValue(typeVarCoords, val)

    def check(self, example):
        pass

    def getType(self):
        return 'INT'


@dataclass
class PriorityVal(Value):
    typeVarCoords: pe.Fragment
    vals: list[Value]

    @pe.ExAction
    def create(attrs, coords, res_coord):
        vals = attrs[0]
        typeVarCoords = coords
        return PriorityVal(typeVarCoords, vals)

    def check(self, example):

        self.vals.check(example)

    def getType(self):
        if len(self.vals) == 0:
            return ''
        curType = "prior"
        for cur in self.vals:
            curType += cur.getType() + "* "
        return curType


@dataclass
class Cons():
    typeVarCoords: pe.Fragment
    vals: list[Value]

    def create(attr1, attr2):
        typeVarCoords = attr1.typeVarCoords
        res = [attr1] + attr2
        return Cons(typeVarCoords, res)

    def check(self, example):
        if len(self.vals) == 1:
            self.vals[0].check(example)
            return

        if type(example) != ScalaList:
            raise DifferentSample(self.typeVarCoords, type(self))
        exampleDef = example
        for cur in reversed(self.vals):
            if type(cur) != list:
                cur.check(exampleDef)
                if len(self.vals) > 0 and cur != self.vals[0]:
                    if type(exampleDef) != ScalaList:
                        raise DifferentSample(self.typeVarCoords, type(self))
                    exampleDef = exampleDef.type

    def getType(self):
        str = "Переменные("
        for cur in self.vals:
            str += cur.getType() + " "
        str += ")"
        return str


@dataclass
class ValCortage(Value):
    typeVarCoords: pe.Fragment
    vals: list[Cons]

    @pe.ExAction
    def create(attrs, coords, res_coord):
        typeVarCoords = coords
        vals = attrs[0]

        return ValCortage(typeVarCoords, vals)

    def check(self, example):
        if type(example) != TypeCortage:
            raise DifferentSample(self.typeVarCoords, type(example))
        if len(self.vals) != len(example.types):
            raise DifferentSample(self.typeVarCoords, type(example))
        for ind in range(0, len(self.vals)):
            self.vals[ind].check(example.types[ind])

    def getType(self):
        str = ""
        for cur in self.vals:
            if type(cur) is list:
                for temp in cur:
                    str += temp.getType()
            else:
                str += cur.getType()
        return str


@dataclass
class ValFunc(Value):
    typeVarCoords: pe.Fragment
    funcname: str
    value: Value

    @pe.ExAction
    def create(attrs, coords, res_coord):
        typeVarCoords = coords
        funcname = attrs[0]
        value = attrs[1]
        return ValFunc(typeVarCoords, funcname, value)

    def check(self, example):
        cond = func[self.funcname][1].equal(example)
        if not cond:
            raise BadArgument(self.typeVarCoords, type(self))
        self.value.check(func[self.funcname][0])

    def getType(self):
        return "ValFunc"


@dataclass
class ValList(Value):
    typeVarCoords: pe.Fragment
    vals: list[Cons]

    @pe.ExAction
    def create(attrs, coords, res_coord):
        typeVarCoords = coords
        vals = attrs[0]
        return ValList(typeVarCoords, vals)

    def check(self, example):
        if type(example) != ScalaList:
            raise DifferentSample(self.typeVarCoords, type(self))

        for cur in self.vals:
            cur.check(example.type)

    def getType(self):
        return "ValList"


class ExprElement(abc.ABC):
    pass


@dataclass
class ExprOp():
    op: str
    elem: ExprElement

    def check(self, example):
        self.elem.check(example)


@dataclass
class Expr():
    beg: ExprElement
    elems: list[ExprOp]

    def create(attr, elems):
        beg = attr
        return Expr(beg, elems)

    def check(self, example):
        self.beg.check(example)
        for cur in self.elems:
            cur.check(example)


@dataclass
class PriorityExpr(Value):
    typeVarCoords: pe.Fragment
    vals: list[Expr]

    @pe.ExAction
    def create(attrs, coords, res_coord):
        typeVarCoords = coords
        vals = attrs[0]
        return PriorityExpr(typeVarCoords, vals)

    def check(self, example):
        if type(self.vals) == list:
            for cur in self.vals:
                cur.check(example)
        else:
            self.vals.check(example)

    def getType(self):
        return "PriorityExpr"


@dataclass
class ExprVal(ExprElement):
    value: Cons
    typeVarCoords: pe.Fragment

    @pe.ExAction
    def create(attrs, coords):
        value = attrs
        return ExprVal(value, coords)

    def check(self, example):
        self.value.check(example)


@dataclass
class ExprBr(Value):
    typeVarCoords: pe.Fragment
    value: Expr

    @pe.ExAction
    def create(attrs, coords, res_coord):
        typeVarCoords = coords
        value = attrs[0]
        return ExprBr(typeVarCoords, value)

    def getType(self):
        return "ExprBr"


@dataclass
class Pattern():
    sample: Cons
    result: Expr

    def check(self, funcname, example):
        checkVariablesMap.clear()
        global boolVariable1
        boolVariable1 = True
        self.sample.check(func[funcname][0])
        boolVariable1 = False
        self.result.check(func[funcname][1])


class UserType(abc.ABC):
    pass


@dataclass
class DefaultType(UserType):
    typename: str

    def equal(self, ut):
        if type(self) != type(ut):
            return False
        if self.typename != ut.typename:
            return False
        return True


@dataclass
class TypeCortage(UserType):
    types: list[UserType]

    def equal(self, ut):
        if type(self) != type(ut):
            return False
        if len(self.types) != len(ut.types):
            return False
        for cur in range(0, len(self.types)):
            cond = self.types[cur].equal(ut.types[cur])
            if not cond:
                return cond
        return True


@dataclass
class ScalaList(UserType):
    type: UserType

    def equal(self, ut):
        if type(self) != type(ut):
            return False
        return self.type.equal(ut.type)


class FuncRedefinition(SemanticError):
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type

    @property
    def message(self):
        return f'Переопределение функции: {self.type}'


@dataclass
class Define(Element):
    funcname: str
    intype: UserType
    outtype: UserType
    patterns: list[Pattern]
    variants: dict[str, tuple[UserType, UserType]]
    typeDefineCoords: pe.Fragment

    @pe.ExAction
    def create(attrs, coords, res_coord):
        funcname, intype, outtype, patterns = attrs

        temp = func.copy()
        if funcname not in func:
            func[funcname] = (intype, outtype)
        typeDefineCoords, _, _, _, _, _, _ = coords
        return Define(funcname, intype, outtype, patterns, temp, typeDefineCoords)

    def check(self):
        if self.funcname in self.variants:
            raise FuncRedefinition(self.typeDefineCoords, self.funcname)
        for cur in self.patterns:
            cur.check(self.funcname, self.intype)


@dataclass
class Program:
    defs: list[Element]

    def check(self):
        for name in self.defs:
            name.check()


INT = pe.Terminal('INT', '[0-9]+', int, priority=7)
FUNCNAME = pe.Terminal('FUNCNAME', '[A-Z][A-Za-z0-9]*', str)
VARNAME = pe.Terminal('VARNAME', '[a-z][A-Za-z0-9]*', str)
STRING = pe.Terminal('STRING', '[@][^\n]*', str.upper)
INTEGER = pe.Terminal('INTEGER', 'int', str.upper)


def make_keyword(image):
    return pe.Terminal(image, image, lambda name: None,
                       re_flags=re.IGNORECASE, priority=10)


DOUBLECOLON, IS, END = \
    map(make_keyword, ':: is end'.split())

NElement, NComment, NDefine = \
    map(pe.NonTerminal, 'Element Comment Define'.split(' '))

NTypes, NType, NPatterns, NPattern, NVal, NExpr = \
    map(pe.NonTerminal, 'Types Type Patterns Pattern Val Expr'.split(' '))

NVals, NCons, NExprOp, NExprOps, NConsVal = \
    map(pe.NonTerminal, 'Vals Cons ExprOp ExprOps NConsVal'.split(' '))

NProgram, NElements, NOp, NExprElement = \
    map(pe.NonTerminal, 'Program Elements Op ExprElement'.split(' '))

NVarnames, NLCons, NLVal, NLVals, NLConsVal = \
    map(pe.NonTerminal, 'Varnames NLCons NLVal NLVals NLConsVal'.split(' '))

NProgram |= NElements, Program

NElements |= NElement, lambda x: [x]
NElements |= NElements, NElement, lambda xs, x: xs + [x]

NElement |= NComment
NElement |= NDefine

NComment |= STRING, Comment

NDefine |= FUNCNAME, NType, DOUBLECOLON, NType, IS, NPatterns, END, Define.create

NType |= VARNAME, DefaultType
NType |= INTEGER, DefaultType
NType |= '(', NTypes, ')', TypeCortage
NType |= '*', NType, ScalaList

NTypes |= NType, lambda x: [x]
NTypes |= NTypes, ',', NType, lambda xs, x: xs + [x]

NPatterns |= NPattern, lambda x: [x]
NPatterns |= NPatterns, ';', NPattern, lambda xs, x: xs + [x]

NPattern |= NLConsVal, '=', NExpr, Pattern

NLConsVal |= NLVal, NLCons, Cons.create
NLCons |= lambda: []
NLCons |= ':', NLVal, NLCons, lambda x, xs: [x] + xs

NLVal |= VARNAME, Variable.create
NLVal |= INT, IntValue.create
NLVal |= '[', NLConsVal, ']', PriorityVal.create
NLVal |= '(', NLVals, ')', ValCortage.create
NLVal |= '{', NLVals, '}', ValList.create

NLVals |= lambda: []
NLVals |= NLConsVal, lambda x: [x]
NLVals |= NLVals, ',', NLConsVal, lambda xs, x: xs + [x]

NVal |= FUNCNAME, NVal, ValFunc.create
NVal |= VARNAME, Variable.create
NVal |= INT, IntValue.create
NVal |= '[', NExpr, ']', PriorityExpr.create
NVal |= '(', NVals, ')', ValCortage.create
NVal |= '{', NVals, '}', ValList.create

NVals |= lambda: []
NVals |= NConsVal, lambda x: [x]
NVals |= NVals, ',', NConsVal, lambda xs, x: xs + [x]

NConsVal |= NVal, NCons, Cons.create
NCons |= lambda: []
NCons |= ':', NVal, NCons, lambda x, xs: [x] + xs

NExpr |= NExprElement, NExprOps, Expr.create

NExprOps |= lambda: []
NExprOps |= NExprOps, NExprOp, lambda xs, x: xs + [x]

NExprOp |= NOp, NExprElement, ExprOp

NExprElement |= NConsVal

NOp |= '+', lambda: '+'
NOp |= '-', lambda: '-'
NOp |= '*', lambda: '*'
NOp |= '/', lambda: '/'


if __name__ == "__main__":
    p = pe.Parser(NProgram)
    p.add_skipped_domain('\\s')
    try:
        tree = p.parse(open('test.txt', 'rt', encoding='utf-8').read()) #тут все чисто

        tree.check()
        print("Программа корректна")
    except pe.Error as e:
        print(f'Ошибка {e.pos}: {e.message}')
    except Exception as e:
        print(e)
