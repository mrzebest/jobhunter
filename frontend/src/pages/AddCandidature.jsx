import { useState } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

export default function AddCandidature() {
  const [form, setForm] = useState({
    entreprise: '',
    titre: '',
    lien: '',
    ville: '',
    type_contrat: 'CDI',
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('access_token');
    try {
      await api.post('candidatures/', form, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      navigate('/dashboard'); // Retour à la liste
    } catch (err) {
        console.error("Erreur POST:", err.response?.data || err.message);
        alert("Erreur lors de l'envoi de la candidature.");
      }      
  };

  return (
    <>
      <Navbar />
      <div className="container" style={{ marginTop: '-15rem' }}></div>
        <form onSubmit={handleSubmit} style={{ padding: '2rem' }}>
          <h2>Ajouter une candidature</h2>
           <input name="entreprise" placeholder="Entreprise" onChange={handleChange} required />
           <input name="titre" placeholder="Titre du poste" onChange={handleChange} required />
           <input name="lien" placeholder="Lien de l'offre" onChange={handleChange} required />
           <input name="ville" placeholder="Ville" onChange={handleChange} required />
           <select name="type_contrat" onChange={handleChange} required>
             <option value="CDI">CDI</option>
             <option value="CDD">CDD</option>
             <option value="ALTERNANCE">Alternance</option>
             <option value="STAGE">Stage</option>
             <option value="FREELANCE">Freelance</option>
             <option value="AUTRE">Autre</option>
           </select>
           <button type="submit">Ajouter</button>
        </form>
    </>
  );
}
