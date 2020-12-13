import React, { useEffect, useState } from "react";
import { makeStyles, Grid, Container } from "@material-ui/core";
import "./Resizable.css";
import DocumentCard from "./DocumentCard";

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
}));

function getDocuments(setDocuments) {
    fetch('http://localhost:8000/api/documents/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            setDocuments(data);
        });
};



export default function Desktop(props) {
    const [documents, setDocuments] = useState([]);

    const handleRefresh = () => {
        getDocuments(setDocuments);
    }

    useEffect(() => {
        handleRefresh();
    }, []);

    useEffect(() => {
        handleRefresh();
    }, [props.refresh]);


    return (
        <Container maxWidth={false} style={{ height: '100%', overflow: 'auto' }}>
            <Grid
                height="100%"
                container
                spacing={1}
            >
                {documents.map(document => (
                    <Grid
                        item
                        md={3}
                    >
                        <DocumentCard
                            image={'http://localhost:8000/api/document/' + encodeURI(document.id)}
                            name={document.name}
                            id={document.id}
                        />
                    </Grid>
                ))}
            </Grid>
        </Container>

    );
}