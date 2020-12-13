import React from 'react';
import './App.css';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';
import { makeStyles } from '@material-ui/core/styles';
import SearchBar from "material-ui-search-bar";

const useStyles = makeStyles((theme) => ({
    button: {
        margin: theme.spacing(1),
    },
    media: {
        // height: '100%',
        // width: '100%',
    },
    root: {
        display: 'flex',
    },
}));

function Search(props) {
    const classes = useStyles();

    return (
        <React.Fragment>
            <SearchBar
                value={'yes'}
            // onChange={(newValue) => this.setState({ value: newValue })}
            // onRequestSearch={() => doSomethingWith(this.state.value)}
            />
        </React.Fragment>
    );
}

export default Search;