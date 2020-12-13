import React, { useEffect, useState } from 'react';
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
        maxHeight: '50vh',
        height: '50vh'
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

function getGroups(setGroups) {
    fetch('http://localhost:8000/api/groups/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            var groups = [];
            data.forEach((group) => groups[group.id] = group);
            setGroups(groups);
        });
};

export default function App() {
    const classes = useStyles();
    const [refresh, doRefresh] = useState(0);
    const [filterTerm, setFilterTerm] = useState('');
    const [filteredGroups, setfilteredGroups] = useState([]);
    const [groups, setGroups] = useState([]);

    const [documentsPositions, setDocumentsPositions] = useState({});
    const [zIndexVar, setZIndexVar] = useState(1);

    useEffect(() => {
        var filtered = groups.filter((group) => {
            const searchVal = group.name.toLowerCase();
            return searchVal.indexOf(filterTerm) !== -1;
        });
        setfilteredGroups(filtered);
    }, [filterTerm, groups]);

    const handleRefresh = () => {
        getGroups(setGroups);
    }

    useEffect(() => {
        handleRefresh();
    }, []);

    useEffect(() => {
        handleRefresh();
    }, [refresh]);

    useEffect(() => {
        var positions = {};
        var i = 0;
        groups.forEach((document) => {
            positions[document.id] = [(i % 4) * 250, Math.floor(i / 4) * 210];
            i++;
        });
        setDocumentsPositions(positions);
    }, [groups]);

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
                        <Paper className={classes.paper} style={{ height: 'calc(100% - 16px)' }}>
                            <Search documents={filteredGroups} setFilterTerm={setFilterTerm} />
                        </Paper>
                    </Grid>
                </Grid>
                <Grid item xs={9} className={classes.desktop} overflow="visible">
                    <Desktop
                        groups={filteredGroups}
                        zIndexVar={zIndexVar}
                        setZIndexVar={setZIndexVar}
                        documentsPositions={documentsPositions}
                        setDocumentsPositions={setDocumentsPositions}
                        handleRefresh={() => doRefresh(prev => prev + 1)}
                    />
                </Grid>
            </Grid>
        </Container>
    );
}
