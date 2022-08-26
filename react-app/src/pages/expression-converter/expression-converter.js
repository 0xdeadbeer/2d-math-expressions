import { Button, Grid, TextField } from "@mui/material";
import { Box, Container } from "@mui/system";
import { React, useState } from "react"; 
import { Tree, TreeNode } from 'react-organizational-chart';

import { scan_tokens, generate_data_tree, generate_result } from "../../resources/functions";
import { OperatorToken } from "../../resources/tokens";

const ExpressionConverter = () => {

    // variables 
    const [expression, setExpression] = useState(""); 
    const [resultTree, setResultTree] = useState(); 

    const generateTree = () => {
        let token_info = scan_tokens(expression); 

        let tokens_array = token_info["tokens_array"]; 
        let privileges_array = token_info["privileges_array"]; 
        let levels_array = token_info["levels_array"]; 

        let data_tree_outcome = generate_data_tree(tokens_array, privileges_array, levels_array);
        
        let tree = data_tree_outcome["tree"]; 
        let index_dictionary = data_tree_outcome["index_dictionary"]; 
        
        let results = generate_result(tree, index_dictionary); 
        let result; 
        Object.keys(results).forEach((key) => {
            if (results[key] instanceof OperatorToken)
                result = results[key];  
        }); 

        console.log(result);
        setResultTree(result);
    }

    const outputTree = (tree) => {
        if (tree == null) return; 

        console.log(tree);

        if (tree instanceof OperatorToken) {
            return (
                <TreeNode label={<div>{tree.label}</div>}>
                    { outputTree(tree.left )}
                    { outputTree(tree.right )}
                </TreeNode>
            )
        } else 
            return (
                <TreeNode label={<div>{tree.value}</div>} />
            )
    }

    return ( 
        <Container sx={{ my: 2 }}>
            <h1>Expression Converter</h1>
            <hr></hr>
            <Button tabIndex={-1} component="a" href="/" variant="contained" size="small">Home</Button>

            <Box sx={{ my: 5 }} >
                <TextField onChange={(e) => {
                    setExpression(e.target.value.trim());
                }} sx={{ my: 2 }} size="small" autoComplete="off" fullWidth label="Enter Expression: " variant="outlined" />
                <Button variant="contained" onClick={() => generateTree()}>Generate Tree</Button>
            </Box>

            <Container>
                <Tree label={<div>Root</div>}>
                    { outputTree(resultTree) }
                </Tree>
            </Container>
        </Container>
    )
}

export default ExpressionConverter; 