import Navbar from '../components/Navbar';
import CandidatureList from '../components/CandidatureList';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  return (
    <>
      <Navbar />
      <div className="container" style={{ marginTop: '-15rem' }}>
      <div className="container">
        <h1>Dashboard</h1>
        <Link to="/ajouter">+ Ajouter une candidature</Link>
        <CandidatureList />
      </div>
      </div>
    </>
  );
}