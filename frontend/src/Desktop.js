import React from "react";
import { Container } from "@material-ui/core";
import "./Resizable.css";
import DocumentCard from "./DocumentCard";

export default function Desktop(props) {
    return (
        <Container maxWidth={false} style={{ height: '100%', overflow: 'auto' }}>
            {props.documents.map(document => (
                <DocumentCard
                    image={'http://localhost:8000/api/document/' + document.id}
                    document={document}
                    zIndexVar={props.zIndexVar}
                    setZIndexVar={props.setZIndexVar}
                    positions={props.documentsPositions}
                    setDocumentsPositions={props.setDocumentsPositions}
                />
            ))}
        </Container>
    );
}