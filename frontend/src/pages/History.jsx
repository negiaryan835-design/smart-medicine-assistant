import { useEffect, useState } from "react";
import "./History.css";

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  async function loadHistory() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/history"
      );

      if (!response.ok) {
        throw new Error("Failed to load history");
      }

      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.error("Could not load history:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  if (loading) {
    return (
      <div className="history-page">
        <div className="page-header">
          <h1>Medication History</h1>
          <p>Loading your history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <div className="page-header">
        <h1>Medication History</h1>
        <p>View your previously recorded doses.</p>
      </div>

      <div className="history-list">
        {history.length === 0 ? (
          <p>No medication history yet.</p>
        ) : (
          history.map((item) => (
            <div className="history-card" key={item.LogID}>
              <div>
                <h2>{item.MedicineName}</h2>
                <p>Taken on: {item.TakenDate}</p>
                <p>Time: {item.TakenTime}</p>
              </div>

              <span className="history-status">
                Taken
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default History;