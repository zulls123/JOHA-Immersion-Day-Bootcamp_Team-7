import React, { useEffect, useState } from 'react';
import { Typography, Container } from '@mui/material';
import Table from '../../components/Table/Table';
import PredictiveModelAPI from '../../api/PredictiveModelApi';
import './TabularPage.css';

const headers = [
  "Scenario",
  "Raw1",
  "Raw2",
  "Raw3 1",
  "Raw3 2",
  "Weight byproduct to unit2",
  "Weight byproduct to unit3",
  "Product1 production",
  "Product2 production",
  "Product3 production",
  "Byproduct production",
  "Total Revenue",
  "Product1 Revenue",
  "Product1 Over Production cost",
  "Product1 Under Production cost",
  "Product2 Revenue",
  "Product2 Over Production cost",
  "Product2 Under Production cost",
  "Product3 Revenue",
  "Product3 Over Production cost",
  "Product3 Under Production cost",
  "Excess byproduct cost"
];

const TabularPage = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = PredictiveModelAPI.getResults();
      setData(result);
    };
    fetchData();
  }, []);

  return (
    <>

      <Container className="container">
        <Typography variant="h4" component="h1" gutterBottom className="header">
          Tabular Example Page
        </Typography>
        <Typography variant="body1" className="description">
          This page provides an example of results displayed in a tabular format.
        </Typography>
       
        <Table headers={headers} data={data} />
    

      </Container>
    </>
  );
};

export default TabularPage;