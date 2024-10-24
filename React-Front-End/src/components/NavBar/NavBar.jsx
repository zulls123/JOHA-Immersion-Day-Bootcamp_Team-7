import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import './NavBar.css';

const NavBar = ({ setSidebarVisible }) => {
    return (
        <AppBar position="static">
            <Toolbar>
                <div className='MenuIcon' >
                    <MenuIcon onClick={() => setSidebarVisible(true)} className='MenuIcon' />
                </div>
                <Typography variant="h6"> Pharmaceutical Back-Office Application</Typography>
            </Toolbar>
        </AppBar>
    );
};

export default NavBar;