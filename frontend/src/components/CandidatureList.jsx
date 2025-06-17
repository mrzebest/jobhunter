import { useEffect, useState } from 'react';
import api from '../api/axios';

export default function CandidatureList() {
  const [candidatures, setCandidatures] = useState([]);

  const fetchCandidatures = async () => {
    const token = localStorage.getItem('access_token');
    try {
      const res = await api.get('candidatures/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCandidatures(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchCandidatures();
  }, []);

  const deleteCandidature = async (id) => {
    const token = localStorage.getItem('access_token');
    try {
      await api.delete(`candidatures/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCandidatures((prev) => prev.filter((c) => c.id !== id));
    } catch (err) {
      console.error("Erreur suppression", err);
    }
  };

  return (
    <div>
      <h2>Mes candidatures</h2>
      <ul>
        {candidatures.map((c) => (
          <li key={c.id}>
            <strong>{c.entreprise}</strong> – {c.titre} ({c.type_contrat})<br />
            📍 <em>{c.ville}</em> – <i>{c.statut}</i>
            <button onClick={() => deleteCandidature(c.id)}>🗑️ Supprimer</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
