# Jack Compiler Structure (Chapter 10)

## class
- keyword: class
- className
- symbol: {
- classVarDec*
- subroutineDec*
- symbol: }

## classVarDec
- keyword: static | field
- type
- varName (',' varName)*
- symbol: ;

## subroutineDec
- keyword: constructor | function | method
- returnType
- subroutineName
- symbol: (
- parameterList
- symbol: )
- subroutineBody

## parameterList
- (type varName) (',' type varName)*

## subroutineBody
- symbol: {
- varDec*
- statements
- symbol: }

## varDec
- keyword: var
- type
- varName (',' varName)*
- symbol: ;

## statements
- letStatement*
- ifStatement*
- whileStatement*
- doStatement*
- returnStatement*
