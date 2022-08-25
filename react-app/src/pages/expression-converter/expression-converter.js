import { Button, Grid, TextField } from "@mui/material";
import { Box, Container } from "@mui/system";
import { React, useState } from "react"; 


const ExpressionConverter = () => {

    // variables 
    const [expression, setExpression] = useState(""); 

    const generateTree = () => {
        alert(expression); 
    }

    return ( 
        <Container sx={{ my: 2 }}>
            <h1>Expression Converter</h1>
            <hr></hr>
            <Button tabIndex={-1} component="a" href="/" variant="contained" size="small">Home</Button>

            <Box sx={{ my: 5 }} >
                <TextField onChange={(e) => {
                    setExpression(e.target.value)
                }} sx={{ mr: 2 }} size="small" autoComplete="off" label="Enter Expression: " variant="outlined" />
                <Button variant="contained" onClick={() => generateTree()}>Generate Tree</Button>
            </Box>

            <Container>
                
            </Container>
        </Container>
    )
}

export default ExpressionConverter; 