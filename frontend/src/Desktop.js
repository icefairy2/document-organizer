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

function getDocuments(setDocuments, setDocumentsPositions, documentCount, setDocumentCount, setIsLoading) {
    fetch('http://localhost:8000/api/documents/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
        .then(data => {
            setDocuments(data);

            //let positions = [[100,100], [20, 20], [30, 30]];
            var positions = {};
            var i = documentCount;
            for (const doc of data) {
                positions[doc.id] = [i * 150, i * 80];
                i++;
            }
            setDocumentCount(i);
            setDocumentsPositions(positions);       
            setIsLoading(false); 
        });
};



export default function Desktop(props) {
    const [documents, setDocuments] = useState([]);
    const [documentCount, setDocumentCount] = useState(0);
    const [documentsPositions, setDocumentsPositions] = useState({});
    const [zIndexVar, setZIndexVar] = useState(1);
    const [isLoading, setIsLoading] = useState(true);

    const handleRefresh = () => {
        getDocuments(setDocuments, setDocumentsPositions, documentCount, setDocumentCount, setIsLoading);
    }

    useEffect(() => {
        handleRefresh();
    }, []);

    useEffect(() => {
        handleRefresh();
    }, [props.refresh]);

    if(!isLoading)
    {
        return (
            <Container maxWidth={false} style={{ height: '100%', overflow: 'auto' }}>
         
                    {documents.map(document => (
                    
                            <DocumentCard
                                image={'http://localhost:8000/api/document/' + encodeURI(document.filePath)}
                                name={document.name}
                                id={document.id}
                                zIndexVar={zIndexVar}
                                setZIndexVar={setZIndexVar}
                                positions={documentsPositions}
                                setDocumentsPositions={setDocumentsPositions}
                            />
                    
                    ))}

          
        </Container>
        );
    }
    {
        return (<div></div>);
    }
}