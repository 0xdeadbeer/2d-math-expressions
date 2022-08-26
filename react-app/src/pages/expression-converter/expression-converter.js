import { Button, Grid, TextField } from "@mui/material";
import { Box, Container } from "@mui/system";
import { React, useState } from "react"; 
import { Tree, TreeNode } from 'react-organizational-chart';

import { scan_tokens, generate_data_tree, generate_result } from "../../resources/functions";

const ExpressionConverter = () => {

    // variables 
    const [expression, setExpression] = useState(""); 

    const generateTree = () => {
        let token_info = scan_tokens(expression); 

        let tokens_array = token_info["tokens_array"]; 
        let privileges_array = token_info["privileges_array"]; 
        let levels_array = token_info["levels_array"]; 

        let data_tree_outcome = generate_data_tree(tokens_array, privileges_array, levels_array);
        
        let tree = data_tree_outcome["tree"]; 
        let index_dictionary = data_tree_outcome["index_dictionary"]; 
        
        let result_array = generate_result(tree, index_dictionary);         
        
    }

    return ( 
        <Container sx={{ my: 2 }}>
            <h1>Expression Converter</h1>
            <hr></hr>
            <Button tabIndex={-1} component="a" href="/" variant="contained" size="small">Home</Button>

            <Box sx={{ my: 5 }} >
                <TextField onChange={(e) => {
                    setExpression(e.target.value.trim());
                }} sx={{ mr: 2 }} size="small" autoComplete="off" label="Enter Expression: " variant="outlined" />
                <Button variant="contained" onClick={() => generateTree()}>Generate Tree</Button>
            </Box>

            <Container>
                <Tree label={<div>Root</div>}>
                    <TreeNode label={<div>Child 1</div>}>
                        <TreeNode label={<div>Child 1</div>}>
                            <TreeNode label={<div>Grand Child</div>} />
                        </TreeNode>
                        <TreeNode label={<div>Child 1</div>}>
                            <TreeNode label={<div>Child 1</div>}>
                                <TreeNode label={<div>Grand Child</div>} />
                            </TreeNode>
                            <TreeNode label={<div>Child 1</div>}>
                                <TreeNode label={<div>Grand Child</div>} />
                            </TreeNode>
                        </TreeNode>
                    </TreeNode>
                    <TreeNode label={<div>Child 1</div>}>
                        <TreeNode label={<div>Grand Child</div>} />
                    </TreeNode>
                </Tree>
            </Container>
        </Container>
    )
}

export default ExpressionConverter; 