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

function Scanner(props) {
  const classes = useStyles();
//  var endpoint = ''
//
//  var wsStart = 'ws://' + window.location.host + window.location.pathname
//
//  var socket - new WebSocket(endpoint)
//
//  socket.onopen = function(e){
//    console.log("open", e)
//    }
//  socket.onmessage = function(e){
//    console.log("message", e)
//    }
//  socket.onerror = function(e){
//    console.log("error", e)
//    }
//  socket.onclose = function(e){
//    console.log("close", e)
//    }

  return (
    <React.Fragment>
      <img src="http://localhost:8000/camera_feed" width="100%" alt="camera_feed" />
      <Button
        variant="contained"
        color="primary"
        size="large"
        className={classes.button}
        startIcon={<SaveIcon />}
        onClick={props.handleSave}
      >
        Save
      </Button>
    </React.Fragment>
  );
}

export default Scanner;
