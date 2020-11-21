import React from 'react';
import './App.css';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';
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

function handleSave() {
  fetch('http://localhost:8000/api/document/', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({})
  });
};

function Scanner() {
  const classes = useStyles();

  return (
    <React.Fragment>
      <img src="http://localhost:8000/camera_feed" width="100%" alt="camera_feed" />
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
