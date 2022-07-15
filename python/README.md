# Program Documentation

> <b>Author: </b> Kevin Jerebica

# High level overview

## Scanning Tokens 

This function will validate an input expression and return its scanned tokens, privilege levels and order levels for each token.

```check_expression -> generate_tokens_array -> generate_type_tokens_array -> generate privileges array -> generate_levels_array -> return```

## Generating a data tree

This function will take the previously generated arrays (tokens, privileges, levels) and store them in some structured manner. 

```
    tree:
        [levels]: {}
    
    level:
        [level]: int, 
        [privileges]: {}
    
    privilege:
        "privilege": int, 
        "elements": [elements]

    element:
        "index": int,
        "value": token_obj
```

## Generate a result 

Generate Result will simply loop through the data structure tree previously created and generate a tree from that data structure.

# Low level overview 

> <b>Coming soon...</b>