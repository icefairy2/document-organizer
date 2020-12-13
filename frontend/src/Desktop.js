import React from "react";
import { Grid, Container } from "@material-ui/core";
import "./Resizable.css";
import DocumentCard from "./DocumentCard";

export default function Desktop(props) {
    return (
        <Container maxWidth={false} style={{ height: '100%', overflow: 'auto' }}>
            <Grid
                height="100%"
                container
                spacing={1}
            >
                {props.documents.map(document => (
                    <Grid
                        item
                        md={3}
                    >
                        <DocumentCard
                            image={'http://localhost:8000/api/document/' + encodeURI(document.filePath)}
                            name={document.name}
                            id={document.id}
                        />
                    </Grid>
                ))}
            </Grid>
        </Container>

    );
}