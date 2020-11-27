import React, { useEffect, useState } from "react";
import { Card, CardActionArea, CardMedia, makeStyles, Grid, Container, Typography, Backdrop } from "@material-ui/core";
import Draggable from "react-draggable";
import { ResizableBox } from "react-resizable";
import "./Resizable.css";

const useStyles = makeStyles((theme) => ({
    root: {
        width: "100%",
        height: "100%",
        margin: theme.spacing(1),
    },
    media: {
        height: "100%",
        width: "100%"
    },
    backdrop: {
        zIndex: theme.zIndex.drawer + 1,
        color: '#fff',
    },
}));

function getDocuments(setDocuments) {
    fetch('http://localhost:8000/api/documents/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            setDocuments(data);
        });
};



export default function Desktop(props) {
    const [documents, setDocuments] = useState([]);

    const handleRefresh = () => {
        getDocuments(setDocuments);
    }

    useEffect(() => {
        handleRefresh();
    }, []);

    useEffect(() => {
        handleRefresh();
    }, [props.refresh]);


    return (
        <Container maxWidth={false} style={{ height: '100%', overflow: 'auto' }}>
            <Grid
                height="100%"
                container
                spacing={1}
            >
                {documents.map(document => (
                    <Grid
                        item
                        md={3}
                    >
                        <DraggableCard
                            image={'http://localhost:8000/api/document/' + encodeURI(document.filePath)}
                            name={document.name}
                            id={document.id}
                        />
                    </Grid>
                ))}
            </Grid>
        </Container>

    );
}

/**
 * Material-UI Card that you can drag and drop anywhere.
 */
const DraggableCard = ({ image, name }) => {
    const classes = useStyles();
    const [open, setOpen] = React.useState(false);
    const [isDragging, setIsDragging] = React.useState(false);

    const handleResizeStart = (e, { size }) => {
        e.stopPropagation();
    };

    const handleClose = () => {
        setOpen(false);
    };
    const handleToggle = () => {
        setOpen(!open);
    };

    const handleDragStart = (e, data) => {
        setIsDragging(true);
    };

    const handleDragStop = (e, data) => {
        setTimeout(() => setIsDragging(false), 50);
    };

    return (
        <React.Fragment>
            <Draggable onDrag={handleDragStart} onStop={handleDragStop}>
                <div>
                    <ResizableBox
                        width={240}
                        height={200}
                        minConstraints={[100, 100]}
                        onResizeStart={handleResizeStart}
                        draggableOpts={{ enableUserSelectHack: false }}
                    >

                        <Card className={classes.root}>
                            <CardActionArea className={classes.media} onClick={() => {
                                if (!isDragging) {
                                    handleToggle();
                                }
                            }}>
                                <Typography variant="overline">
                                    {name}
                                </Typography>

                                <CardMedia
                                    className={classes.media}
                                    image={image}
                                // title="Contemplative Reptile"
                                />
                            </CardActionArea>
                        </Card>
                    </ResizableBox>
                </div>
            </Draggable>
            <Backdrop className={classes.backdrop} open={open} onClick={handleClose}>
                <img src={image} alt={name} />
            </Backdrop>
        </React.Fragment>
    );
};
