import "./History.css";

function History() {
  return (
    <div className="history-page">
      <div className="page-header">
        <h1>Scan History</h1>
        <p>View your previously scanned medicines.</p>
      </div>

      <div className="history-card">
        <div>
          <h2>Paracetamol</h2>
          <p>Scanned on: July 16, 2026</p>
          <p>Dosage: 500 mg</p>
        </div>

        <span className="history-status">Scanned</span>
      </div>
    </div>
  );
}

export default History;