import React from "react";
import { Card, CardActionArea, CardMedia, makeStyles, Typography, Backdrop, InputBase, IconButton, Dialog, DialogContentText } from "@material-ui/core";
//import Draggable from "react-draggable";
import { Rnd } from "react-rnd";
import { ResizableBox } from "react-resizable";
import "./Resizable.css";
import CancelIcon from '@material-ui/icons/Cancel';
import SaveIcon from '@material-ui/icons/Save';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';

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
    fullImage: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        flexWrap: 'wrap',
        margin: theme.spacing(1)
    },
    style: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: 'solid 1px #ddd',
        background: '#f0f0f0'
    }

}));

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
  }

function mergeDocs(id1, id2) {
    fetch('http://localhost:8000/api/group/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'doc1_id': id1,
            'doc2_id': id2
        })
    })
}

export default function DocumentCard({ image, name, id, zIndexVar, setZIndexVar, positions, setDocumentsPositions }) {
    const classes = useStyles();
    const [open, setOpen] = React.useState(false);
    const [alertOpen, setAlertOpen] = React.useState(false);
    const [isDragging, setIsDragging] = React.useState(false);
    const [isEditingName, setIsEditingName] = React.useState(false);
    const [modifiedName, setModifiedName] = React.useState(name);
    const [zIndexLocal, setZIndexLocal] = React.useState(1);
    
    const [openBar, setOpenBar] = React.useState(false);

    const handleClickBar = () => {
        setOpenBar(true);
    };

    const handleCloseBar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setOpenBar(false);
    };

    const handleResizeStart = (e, { size }) => {
        e.stopPropagation();
    };

    const handleClose = () => {
        if (isEditingName) {
            setAlertOpen(true);
        } else {
            setOpen(false);
        }
    };

    const handleToggle = () => {
        setOpen(!open);
    };

    const handleDragStart = (e, data) => {
        setZIndexLocal(zIndexVar);
        setZIndexVar(zIndexVar + 1);
        setIsDragging(true);
    };

    const handleDragStop = (e, data) => {
        setTimeout(() => setIsDragging(false), 50);
        
        // Update the current card (document) position in the global var
        positions[id] = [e.x, e.y];
        setDocumentsPositions(positions);

        // Iterate over (doc id - coords collection) key value pairs
        for (const [currentDocId, coords] of Object.entries(positions))
        {
            if(currentDocId != id)
            {   
                // TODO: The position is a bit off for some cards, investigate why later
                let xdif = Math.abs(e.x - coords[0]);
                let ydif = Math.abs(e.y - coords[1]);
                if( xdif < 70 && ydif < 70)
                {
                    mergeDocs(currentDocId, id);
                    handleClickBar();
                }
         
            }
        }
    };

    const onChange = (event) => {
        if (name !== event.target.value) {
            setIsEditingName(true);
            setModifiedName(event.target.value)
        } else {
            setIsEditingName(false);
        }
    };

    const handleSave = () => {
        // TODO: Validate new name

        fetch('http://localhost:8000/api/rename/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'id': id,
                'new_name': modifiedName
            })
        }).then(response => {
            if (response.ok) {
                setIsEditingName(false);
            }
        });
    }

    const handleDialogSave = () => {
        handleSave();
        setAlertOpen(false);
        setOpen(false);
    }

    const handleDiscard = () => {
        setModifiedName(name);
        setIsEditingName(false);
        setAlertOpen(false);
        setOpen(false);
    }

    return (
        <React.Fragment>
            <Rnd
                default={{
                    x: positions[id][0],
                    y: positions[id][1],
                    width: 240,
                    height: 200,
                }}
                onDrag={handleDragStart} onDragStop={handleDragStop}
                style={{ zIndex: zIndexLocal }}
                bounds={'parent'}
            >
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
                                    {modifiedName}
                                </Typography>

                                <CardMedia
                                    className={classes.media}
                                    image={image}
                                />
                            </CardActionArea>
                        </Card>
                    </ResizableBox>
                </div>
            </Rnd>
            <Backdrop className={classes.backdrop} open={open}>
                <div className={classes.fullImage}>
                    <div style={{ display: 'flex', flexDirection: 'row', width: '100%' }}>
                        <InputBase
                            style={{ color: 'white', fontSize: 30, width: '400' }}
                            size="large"
                            defaultValue={name}
                            value={modifiedName}
                            fullWidth
                            multiline
                            onChange={onChange}
                            inputProps={{ 'aria-label': 'naked' }}
                        />
                        {isEditingName &&
                            <IconButton
                                style={{ color: 'white' }}
                                aria-label="close"
                                onClick={handleSave}
                            >
                                <SaveIcon fontSize="large" />
                            </IconButton>
                        }
                    </div>
                    <img src={image} alt={name} />
                </div>
                <IconButton
                    style={{
                        color: 'white',
                        position: 'absolute',
                        left: '90%',
                        top: '10%',
                    }}
                    aria-label="close"
                    onClick={handleClose}
                >
                    <CancelIcon fontSize="large" />
                </IconButton>
            </Backdrop>
            <Dialog
                open={alertOpen}
                onClose={() => setAlertOpen(false)}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">{"You have unsaved naming changes"}</DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        Do you want to rename document "{name}" to "{modifiedName}"?
                </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleDialogSave} color="primary">
                        Save
                    </Button>
                    <Button onClick={handleDiscard} color="primary" autoFocus>
                        Discard
                    </Button>
                </DialogActions>
            </Dialog>
            <Snackbar open={openBar} autoHideDuration={2000} onClose={handleCloseBar}>
                <Alert onClose={handleCloseBar} severity="success">
                 Documents succesfully merged!
                </Alert>
            </Snackbar>
        </React.Fragment>
        
    );
};
