import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { Home } from './pages/home';
import { Trainings } from './pages/trainings';
import Header from './components/Header';
import './App.css';


function App() {


  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/trainings" element={<Trainings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
