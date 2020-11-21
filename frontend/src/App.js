import React, { useRef } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Scanner from './Scanner';
import Desktop from './Desktop';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
        height: '100%',
        width: '100%',
        position: 'absolute',
        top: '0',
        left: '0',
    },
    paper: {
        padding: theme.spacing(1),
        textAlign: 'center',
        color: theme.palette.text.secondary,
        backgroundColor: "#aeaeae",
    },
    desktop: {
        padding: theme.spacing(0),
        backgroundColor: "#aeaeae",
        paddingRight: 0,
        height: '100%'
    }
}));

export default function CenteredGrid() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <Grid container spacing={2} style={{ height: '100%' }}>
                <Grid item xs={3}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Paper className={classes.paper} >
                                <Scanner />
                            </Paper>
                        </Grid>
                        <Grid item xs={12}>
                            <Paper className={classes.paper}>
                                TODO: Folder structure
                            </Paper>
                        </Grid>
                    </Grid>
                </Grid>
                <Grid item xs={9} className={classes.desktop}>
                    <Desktop />
                </Grid>
            </Grid>
        </div>
    );
}
