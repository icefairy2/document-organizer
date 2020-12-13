import React from "react";
import { Container } from "@material-ui/core";
import "./Resizable.css";
import DocumentCard from "./DocumentCard";

export default function Desktop(props) {
    return (
        <Container maxWidth={false} style={{ height: '100%', overflow: 'auto' }}>
            {props.groups.length > 0 &&
                props.groups.map(group => (
                    <DocumentCard
                        documents={group.documents}
                        id={group.id}
                        name={group.name}
                        nrPages={group.nrPages}
                        zIndexVar={props.zIndexVar}
                        setZIndexVar={props.setZIndexVar}
                        positions={props.documentsPositions}
                        setDocumentsPositions={props.setDocumentsPositions}
                        handleRefresh={props.handleRefresh}
                    />
                ))}
        </Container>
    );
}