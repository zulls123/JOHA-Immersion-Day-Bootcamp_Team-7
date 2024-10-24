import React from 'react';
import './PageLayout.css';
import NavBar from '../../components/NavBar/NavBar';
import Sidebar from '../../components/Sidebar/Sidebar';
import LandingPage from '../LandingPage/LandingPage';
import { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import CustomRouter from '../../components/CustomRouter/CustomRouter';


const PageLayout = () => {
    const [sidebarVisible, setSidebarVisible] = useState(false);

    return (
        <div className="page-layout">
            <NavBar setSidebarVisible={setSidebarVisible}/>
            <Sidebar visible={sidebarVisible} setVisible={setSidebarVisible}/>
            <main className="content">
                <CustomRouter />
            </main>
        </div>
    );
};

export default PageLayout;