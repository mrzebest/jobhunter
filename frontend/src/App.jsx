import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import AddCandidature from './pages/AddCandidature';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/ajouter" element={<AddCandidature />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
