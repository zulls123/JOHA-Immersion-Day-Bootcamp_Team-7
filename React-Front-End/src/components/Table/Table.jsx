import React from 'react';
import { Table as MuiTable, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import './Table.css';

const Table = ({ headers, data }) => {
  return (
    <TableContainer component={Paper} className="table-container">
      <MuiTable>
        <TableHead>
          <TableRow className="table-header">
            {headers.map((header) => (
              <TableCell key={header} className="table-cell">{header}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index} className="table-row">
              {Object.values(row).map((value, idx) => (
                <TableCell key={idx} className="table-cell">{value}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </MuiTable>
    </TableContainer>
  );
};

export default Table;
