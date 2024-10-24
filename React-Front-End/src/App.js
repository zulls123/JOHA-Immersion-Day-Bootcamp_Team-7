import './App.css';
import PageLayout from './pages/PageLayout/PageLayout';
import { BrowserRouter } from 'react-router-dom';


function App() {
  return (
    <div className="App">
      <BrowserRouter>
         <PageLayout />
      </BrowserRouter> 
    </div>
  );
}

export default App;
