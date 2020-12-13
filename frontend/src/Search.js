import React from 'react';
import './App.css';
import { makeStyles } from '@material-ui/core/styles';
import SearchBar from "material-ui-search-bar";
import { List, ListItem, ListItemIcon, ListItemText } from '@material-ui/core';
import DescriptionIcon from '@material-ui/icons/Description';

const useStyles = makeStyles((theme) => ({
    root: {
        overflow: 'auto',
        position: 'relative',
        maxHeight: '80%',
        height: '80%',
        marginTop: theme.spacing(2),
    },
}));

function Search(props) {
    const classes = useStyles();

    return (
        <React.Fragment>
            <SearchBar
                style={{ height: '10%' }}
                onChange={(newValue) => props.setFilterTerm(newValue)}
                onCancelSearch={() => props.setFilterTerm('')}
            />
            <List dense={true} className={classes.root}>
                {props.groups.map(group => (
                    <ListItem button>
                        <ListItemIcon>
                            <DescriptionIcon />
                        </ListItemIcon>
                        <ListItemText
                            primary={group.name + '(' + group.nrPages + ')'}
                        />
                    </ListItem>
                ))}
            </List>
        </React.Fragment>
    );
}

export default Search;