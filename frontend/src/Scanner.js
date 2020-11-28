import React from 'react';
import './App.css';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';
import Input from '@material-ui/core/Input'
import { makeStyles } from '@material-ui/core/styles';

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

let state = {
        name : "Title"
    };

function handleSave() {

  fetch('http://localhost:8000/api/document/' + state.name + '/', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({})
  });
}

function handleChange(e) {
    state = {
        name : e.target.value
    };
}

function Scanner() {
  const classes = useStyles();

  return (
    <React.Fragment>
      <img src="http://localhost:8000/camera_feed" width="100%" alt="camera_feed" />
      <Input
        type="text"
        onChange={(e) => handleChange(e)}
        defaultValue={"Title"}
      >
      </Input>
      <Button
        variant="contained"
        color="primary"
        size="large"
        className={classes.button}
        startIcon={<SaveIcon />}
        onClick={handleSave}
      >
        Save
      </Button>
    </React.Fragment>
  );
}

export default Scanner;
