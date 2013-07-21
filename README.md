TCforTestLink
=============

: converter for testlink


### 1. Schema: schema.py

: Schema mapping xls to testlink xml

* SCHEMA

```
col 0: Test Suit: Top, P[1..9] : testcase, XXX : Testsuite name 

col 1: id: can be skipped at the moment

col 2: Title: testacase name

col 3: Description: Preconditions, Steps

col 4: Expected result

```

### 2. Regex Pattern: tcPattern.py

: Regex pattern to parse a cell from spreadsheet

* testcase for sample

```
steps = '(\d\.)(.*)'

precondition = '(Preconditions:)([a-zA-Z\s\'-\.]*)(?=step)'
    
sel_subgroup = 2
```
    
* test in http://pythex.org/
    
    
###3. Prerequsite
: additional python modules to install

  - xlrd: python module to read xls spreadsheet
  - lxml: cython module to create XML tree
