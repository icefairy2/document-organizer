import React, { useEffect, useState } from "react";
import { Card, Button, CardActionArea, CardMedia, makeStyles, CardActions, IconButton, Grid, Container } from "@material-ui/core";
import Draggable from "react-draggable";
import RefreshIcon from '@material-ui/icons/Refresh';

const useStyles = makeStyles((theme) => ({
    root: {
        maxWidth: 240,
        margin: theme.spacing(1),
    },
    media: {
        height: 140,
    },
}));

function getDocuments(setPaths) {
    fetch('http://localhost:8000/api/documents/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            const paths = data.map(doc => doc.filePath);
            setPaths(paths);
        });
};

export default function Desktop() {
    const [imagePaths, setPaths] = useState([]);

    useEffect(() => {
        getDocuments(setPaths);
    }, []);

    const handleRefresh = () => {
        getDocuments(setPaths);
    }

    return (
        <Container maxWidth={false} style={{ height: '100%', overflow: 'auto' }}>
            <IconButton aria-label="refresh" onClick={handleRefresh}>
                <RefreshIcon />
            </IconButton>
            <Grid
                height="100%"
                container
                spacing={1}
            >
                {imagePaths.map(path => (

                    <Grid
                        item
                        md={3}
                    >
                        <DraggableCard image={'http://localhost:8000/api/document/' + encodeURI(path)} />
                    </Grid>
                ))}
            </Grid>
        </Container>
    );
}

/**
 * Material-UI Card that you can drag and drop anywhere.
 */
const DraggableCard = ({ image }) => {
    const classes = useStyles();
    return (
        <Draggable>
            <Card className={classes.root}>
                <CardActionArea>
                    <CardMedia
                        className={classes.media}
                        image={image}
                    // title="Contemplative Reptile"
                    />
                </CardActionArea>
                <CardActions>
                    <Button size="small" color="primary">
                        Share
                    </Button>
                </CardActions>
            </Card>
        </Draggable>
    );
};
