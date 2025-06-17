import { useState } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLoginPage = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('token/', {
        username: username,
        password: password,
      });
      localStorage.setItem('access_token', res.data.access);
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      alert("Nom d'utilisateur ou mot de passe invalide.");
    }
  };

  return (
    <form onSubmit={handleLoginPage}>
      <h2>Connexion</h2>
      <input
        type="text"
        placeholder="Nom d'utilisateur"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Mot de passe"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Se connecter</button>
    </form>
  );
}

