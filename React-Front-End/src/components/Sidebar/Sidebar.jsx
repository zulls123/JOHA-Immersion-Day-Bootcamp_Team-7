import React from 'react';
import { Drawer, List, ListItem, ListItemText, ListSubheader, Collapse } from '@mui/material';
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Sidebar.css';

const drawerWidth = 240;

const Sidebar = ({ visible, setVisible }) => {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  const handleClick = () => {
    setOpen(!open);
  };

  const handleClose = () => {
    setVisible(false);
  };

  const minimizeSidebar = () => {
    setVisible(false);
  }

  const handleNavigate = (path) => { 
    minimizeSidebar();
    navigate(path);
  }

  return (
    <Drawer
      variant="temporary"
      style={{ width: drawerWidth, flexShrink: 0 }}
      classes={{ paper: { width: drawerWidth } }}
      open={visible}
      onClose={handleClose}
    >
      <List
        component="nav"
        subheader={<ListSubheader component="div">Menu</ListSubheader>}
      >
        <ListItem button onClick={() => { handleNavigate('/') }}>
          <ListItemText primary="Home" />
        </ListItem>
        <ListItem button onClick={handleClick}>
          <ListItemText primary="Example Components" />
          {open ? <ExpandLess /> : <ExpandMore />}
        </ListItem>
        <Collapse in={open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItem button style={{ paddingLeft: drawerWidth / 4 }} onClick={() => { handleNavigate('/pie-chart-component') }}> 
              <ListItemText primary="Pie Chart" />
            </ListItem>
            <ListItem button style={{ paddingLeft: drawerWidth / 4 }} onClick={() => { handleNavigate('/bar-chart-component') }}>
              <ListItemText primary="Bar Chart" />
            </ListItem>
            <ListItem button style={{ paddingLeft: drawerWidth / 4 }} onClick={() => { handleNavigate('/table-chart-component') }}>
              <ListItemText primary="Table" />
            </ListItem>
          </List>
        </Collapse>
      </List>
    </Drawer>
  );
};

export default Sidebar;