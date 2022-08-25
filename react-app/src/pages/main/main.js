import { React  } from "react"; 
import { Button, ButtonGroup, Container, Grid } from "@mui/material"

import { spacing } from '@mui/system';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import { Link, useNavigate } from "react-router-dom";

const Main = () => {
    const navigate = useNavigate(); 
    
    return (
        <Container sx={{ my: 2}}>
            <h1>Xpression</h1>
            <hr></hr>
            <small>Side project that's based on one <a href="https://youtube.com/user/computerphile">Computerphile's</a> videos. A german professor of Computer Science introduced this idea of representing mathematical expressions in a 2D tree structure, and so I made a converter out of that video :3</small>
            <br></br>
            <ButtonGroup sx={{ my: 1 }} component="a" size="small" variant="contained" color="primary">
                <Button href="https://github.com/osamu-kj">My Github</Button>
                <Button href="https://github.com/osamu-kj/2dmathexpressions">Project's Source Code</Button>
                <Button href="/expression-converter">Expression Converter</Button>
            </ButtonGroup>
            <br></br>
            <iframe
                width="853"
                height="480"
                src="https://www.youtube.com/embed/7tCNu4CnjVc"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                title="Embedded youtube"
            />
        </Container>
    )
}

export default Main; 