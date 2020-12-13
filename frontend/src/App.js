import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Scanner from './Scanner';
import Desktop from './Desktop';
import Search from './Search';

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
        height: '100%',
        width: '100%',
    },
    searchSection: {
        paddingTop: theme.spacing(2),
        alignItems: "stretch",
        flexGrow: 1,
        // height: 'max-content',
    }
}));

function handleSave(callback) {
    fetch('http://localhost:8000/api/document/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    }).then(resp => {
        callback();
    });
};

export default function App() {
    const classes = useStyles();
    const [refresh, doRefresh] = useState(0);

    const handleSaveAndRefresh = () => {
        handleSave(() => doRefresh(prev => prev + 1));
    }

    return (
        <Container maxWidth={false} className={classes.root}>
            <Grid container spacing={2} style={{ height: '100%' }}>
                <Grid container spacing={2} direction="column" xs={3} style={{ paddingRight: 16 }}>
                    <Grid item>
                        <Paper className={classes.paper} >
                            <Scanner handleSave={handleSaveAndRefresh} />
                        </Paper>
                    </Grid>
                    <Grid item className={classes.searchSection}>
                        <Paper className={classes.paper} style={{ height: 'calc(100% - 16px)', overflow: 'auto' }}>
                            <Search />
                        </Paper>
                    </Grid>
                </Grid>
                <Grid item xs={9} className={classes.desktop} overflow="visible">
                    <Desktop refresh={refresh} />
                </Grid>
            </Grid>
        </Container>
    );
}
