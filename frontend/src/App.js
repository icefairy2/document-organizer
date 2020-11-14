import './App.css';
import Button from '@material-ui/core/Button';
import SaveIcon from '@material-ui/icons/Save';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  button: {
    margin: theme.spacing(1),
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

function App() {
  const classes = useStyles();

  return (
    <div className="App">
      <header className="App-header">
        <img src="http://localhost:8000/camera_feed" alt="camera_feed" />
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
      </header>
    </div>
  );
}

export default App;
