
# Brainstorm

### re 'hello' 'file.py'

### re 'hello' 'file.py' | rfmt -l

### re 'hello' -r 'bye' 'file.py'

### re 'hello' 'file.py' |  rsub 'bye'

### re 'hello' 'file.py' | rfmt -c | rsub 'bye'

Problem:
Wie soll 'rsub' die printausbe bei --confirm handeln??



find '.' | re 'search' | rsub 'bye'
find '.' | pyre 'search' | rsub 'bye'
find '.' | re2 'search' | rfmt 
ag 'hello' '.' -J | rsub 'bye'


# Possible Groups

## re search tools
These use different re libraries (each uses it's own) to search 
(file-content, strings)' and use rfmt (internally) to format the ouput. 
NOTE: Wozu brauchst du diese, wenn es die 'sub' tools gibt?
-pyre
-rure
...

## re sub tool.
These use different re libraries (each uses it's own) to search 
(file-content, strings)' and use rfmt (internally) to format the ouput. 
-pysub
-rusub



# Group conclusion:

## universal regex tools
These use different re libraries (each uses it's own) to search/replace
(file-content, strings)' and use rfmt (internally) to format the ouput.
They may use 'resub' (universal substitution engine).

find '.' | pyre 'hello' -r 'bye'

re?
pyre
rure
r2re
pcre
...

## universal substitution engine tools
These run substitutions. The only thing they can read is URM compliant data.
They are silent. The can however forward the input data and print errors.

resub
pysub
rusub






This is nice! :

re 'hello' | rfmt 
pyre 'hello' | rfmt 
rure 'hello' | rfmt2


re 'hello' | rsub 'bye' 
re 'hello' | rsub 'bye' --fmt rfmt
re 'hello' | rsub 'bye' -f rfmt
re 'hello' | rsub 'bye' --no-confirm

   
 
 
 
 
 
 
 
 
 
