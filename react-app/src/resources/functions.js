import { v4 as uuidv4 } from 'uuid';
import { NumberToken, OperatorToken, PointerToken, VariableToken } from './tokens';
import { NumberTypeToken, SymbolTypeToken, VariableTypeToken } from "./typetokens";

const expression_symbols = {
    "+": {
        "privilege": 4,
        "label": "operator"
    },
    "-": {
        "privilege": 4,
        "label": "operator"
    },
    "*": {
        "privilege": 3,
        "label": "operator"
    },
    "/": {
        "privilege": 3,
        "label": "operator"
    },
    "^": {
        "privilege": 2, 
        "label": "operator"
    },
    "(": {
        "privilege": 5,
        "label": "privilege_operator"
    },
    ")": {
        "privilege": 5,
        "label": "privilege_operator"
    },
}

const unnecessary_tokens = {
    "(": {}, 
    ")": {}
}

const isNumber = (val) => {
    return !isNaN(val); 
}

const check_expression = (expression) => {
    let symbols = Object.keys(expression_symbols).map((key) => "\\" + key).join("");
    let regex_expression = new RegExp(`^[a-zA-Z0-9${symbols} ]+$`, "g");
    return regex_expression.test(expression);
}

const isolate_elements = (expression) => {
    let tokens_array = [] 
    let symbols = Object.keys(expression_symbols).map((key) => "\\" + key).join(""); 
    let regex_expression = new RegExp(`(?:[0-9]+)|(?:[a-z]+)|(?:[${symbols}])`, "g"); 
    let match; 
    while ((match = regex_expression.exec(expression)) !== null)
        tokens_array.push(match[0]); 

    return tokens_array; 
}

const return_token_type = () => {

}

const char_to_type_tokens = (char_array) => {
    let type_tokens_array = [] 

    char_array.map((char) => {
        let type_token; 
        let char_regex = new RegExp(`^[a-zA-Z]+$`, "g");

        if (isNumber(char)) {
            let number = parseInt(char); 
            type_token = new NumberTypeToken(number, 1); 
        }

        else if (char_regex.test(char)) {
            type_token = new VariableTypeToken(char, 1); 
        }

        else if (char in expression_symbols) {
            let privilege = expression_symbols[char].privilege; 
            let label = expression_symbols[char].label; 
            type_token = new SymbolTypeToken(char, label, privilege); 
        }
        
        else throw new Error(`Unable to figure out the type token of '${char}'`); 

        type_tokens_array.push(type_token); 
    })

    return type_tokens_array; 
}

const check_token_rules = () => {
    return true; 
}

const generate_levels_array = (privileges_array, tokens_array) => {

    let levels_array = []; 
    let brackets_trace = []; 
    let level = 0; 

    for (let index = 0; index < tokens_array.length; index++) {
        let privilege = privileges_array[index];         
        let token_value = tokens_array[index].value; 
        
        if (privilege !== 5) {
            levels_array.push(level)
            continue; 
        } 

        if (token_value === "(") {
            levels_array.push(level); 
            brackets_trace.push(1); 

            level += 1; 
            continue; 
        }

        if (token_value === ")") {
            if (level <= 0 || brackets_trace.length <= 0)
                throw new Error("Program error!");
            
            level -= 1; 
            levels_array.push(level); 
            brackets_trace.pop();         
            continue; 
        }

        throw new Error("Program error!");
    }

    if (brackets_trace.length > 0)
        throw new Error("Program error!"); 
    
    return levels_array; 
}

const sync_element = (index_dictionary, target_id, pointing_id) => {
    while (index_dictionary[target_id] instanceof PointerToken)
        target_id = index_dictionary[target_id].fetch_destination(); 

    index_dictionary[target_id] = new   PointerToken(pointing_id); 
}

const find_target = (index_dictionary, target_id) => {
    while (index_dictionary[target_id] instanceof PointerToken)
        target_id = index_dictionary[target_id].fetch_destination(); 
    
    return index_dictionary[target_id]; 
}

// exported functions 
export const scan_tokens = (expression) => {
    let tokens_array = []; 
    let privileges_array = []; 
    let levels_array = []; 

    if (!check_expression(expression))
        throw new Error("Given expression is invalid!");

    tokens_array = isolate_elements(expression);

    if (!tokens_array.length)
        throw new Error("Expression does not follow the expression rules!"); 
    
    tokens_array = char_to_type_tokens(tokens_array); 

    if (!check_token_rules(tokens_array)) 
        throw new Error("Given expression is invalid!"); 
    
    privileges_array = tokens_array.map((token) => token.privilege)

    levels_array = generate_levels_array(privileges_array, tokens_array); 

    let new_tokens_array = []; 
    let new_privileges_array = []; 
    let new_levels_array = [];
    
    for (let index = 0; index < tokens_array.length; index++) {
        let token_value = tokens_array[index].value; 
        
        if (token_value in unnecessary_tokens)
            continue; 
        
        new_tokens_array.push(tokens_array[index]); 
        new_privileges_array.push(privileges_array[index]); 
        new_levels_array.push(levels_array[index]); 
    }

    return {
        "tokens_array": new_tokens_array,
        "privileges_array": new_privileges_array,
        "levels_array": new_levels_array,
    }
}

export const generate_data_tree = (tokens, privileges, levels) => {
    let tree = {} 
    let index_dictionary = {} 

    for (let index = 0; index < tokens.length; index++) {
        let token = tokens[index]; 
        let privilege = privileges[index]; 
        let level = levels[index]; 

        if (!(level in tree))
            tree[level] = {
                "level": level, 
                "privileges": {},
            }
        
        if (!(privilege in tree[level]["privileges"]))
            tree[level]["privileges"][privilege] = {
                "privilege": privilege,
                "elements": []
            }
        
        let token_id = uuidv4();
        
        tree[level]["privileges"][privilege]["elements"].push({
            "index": index, 
            "value": token,
            "id": token_id,
        })

        index_dictionary[index] = token_id
    }

    return {
        "tree": tree,
        "index_dictionary": index_dictionary,
    }
}

export const generate_result = (tree, index_dictionary) => {
    let calculations_array = {}
    let result; 

    let levels = Object.keys(tree); 
    levels = levels.sort((a, b) => { return b - a }); 

    for (let level_index = 0; level_index < levels.length; level_index++) {
        let level = tree[levels[level_index]]; 
        
        let privileges = Object.keys(level["privileges"]); 
        privileges = privileges.sort((a, b) => { return a - b }); 
        
        for (let privilege_index = 0; privilege_index < privileges.length; privilege_index++) {
            let privilege = level["privileges"][privileges[privilege_index]]; 
            let privilege_number = privilege["privilege"]; 

            let elements = privilege["elements"];
            for (let element_index = 0; element_index < elements.length; element_index++) {
                let expression_element_index = elements[element_index]["index"]; 
                let token = elements[element_index]["value"]; 
                let token_id = elements[element_index]["id"]; 
                
                if (token instanceof NumberTypeToken) 
                    token = new NumberToken(token.value); 
                
                else if (token instanceof VariableTypeToken)
                    token = new VariableToken(token.value); 
                
                else if (token instanceof SymbolTypeToken) {
                    let left_index = expression_element_index - 1; 
                    let right_index = expression_element_index + 1; 
                    
                    let left_id = index_dictionary[left_index]; 
                    let right_id = index_dictionary[right_index]; 

                    let left = find_target(calculations_array, left_id); 
                    let right = find_target(calculations_array, right_id); 

                    token = new OperatorToken(left, right, privilege_number, token.value); 

                    sync_element(calculations_array, left_id, token_id); 
                    sync_element(calculations_array, right_id, token_id); 
                }

                else throw new Error("Program error!"); 
            
                calculations_array[token_id] = token;  
                result = token; 
            }
        }
    }
    return result;
}