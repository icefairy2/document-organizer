import React from "react";
import { Card, CardActionArea, CardMedia, makeStyles, Typography, Backdrop, InputBase, IconButton, Dialog, DialogContentText } from "@material-ui/core";
import Draggable from "react-draggable";
import { ResizableBox } from "react-resizable";
import "./Resizable.css";
import CancelIcon from '@material-ui/icons/Cancel';
import SaveIcon from '@material-ui/icons/Save';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

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
    }
}));

export default function DocumentCard({ image, name, id }) {
    const classes = useStyles();
    const [open, setOpen] = React.useState(false);
    const [alertOpen, setAlertOpen] = React.useState(false);
    const [isDragging, setIsDragging] = React.useState(false);
    const [isEditingName, setIsEditingName] = React.useState(false);
    const [modifiedName, setModifiedName] = React.useState(name);

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
        setIsDragging(true);
    };

    const handleDragStop = (e, data) => {
        setTimeout(() => setIsDragging(false), 50);
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
    }

    const handleDiscard = () => {
        setModifiedName(name);
        setIsEditingName(false);
        setAlertOpen(false);
        setOpen(false);
    }

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
            </Draggable>
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
                    <Button onClick={handleSave} color="primary">
                        Save
                    </Button>
                    <Button onClick={handleDiscard} color="primary" autoFocus>
                        Discard
                    </Button>
                </DialogActions>
            </Dialog>
        </React.Fragment>
    );
};
