import { useState } from "react";
import "./Dashboard.css";

function Dashboard() {
  const [stats] = useState({
    totalMedicines: 2,
    activeReminders: 3,
    medicinesScanned: 5,
  });

  const [reminders] = useState([
    {
      medicine: "Paracetamol",
      dosage: "500 mg",
      time: "10:00 AM",
    },
    {
      medicine: "Vitamin D",
      dosage: "1000 IU",
      time: "8:00 PM",
    },
  ]);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <h2>Welcome to Smart Medicine Assistant</h2>
        <p>
          Manage your medicines, reminders, and health information.
        </p>
      </div>

      <div className="stats-container">
        <div className="stat-card">
          <h3>Total Medicines</h3>
          <p>{stats.totalMedicines}</p>
        </div>

        <div className="stat-card">
          <h3>Active Reminders</h3>
          <p>{stats.activeReminders}</p>
        </div>

        <div className="stat-card">
          <h3>Medicines Scanned</h3>
          <p>{stats.medicinesScanned}</p>
        </div>
      </div>

      <div className="reminders-section">
        <h2>Upcoming Reminders</h2>

        {reminders.map((reminder, index) => (
          <div className="reminder-card" key={index}>
            <div>
              <h3>{reminder.medicine}</h3>
              <p>Dosage: {reminder.dosage}</p>
            </div>

            <strong>{reminder.time}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;