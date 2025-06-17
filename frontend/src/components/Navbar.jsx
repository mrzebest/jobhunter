import { Link, useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div className="container-fluid px-4">
        <Link className="navbar-brand fw-bold" to="/dashboard">
          JobHunter
        </Link>
        <div className="ms-auto">
          <button className="btn btn-danger" onClick={handleLogout}>
            🔒 Se déconnecter
          </button>
        </div>
      </div>
    </nav>
  );
}
