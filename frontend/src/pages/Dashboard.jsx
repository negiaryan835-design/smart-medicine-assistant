import { useEffect, useState } from "react";
import "./Dashboard.css";

function Dashboard() {
  const [stats, setStats] = useState({
    totalMedicines: 0,
    activeReminders: 0,
    medicinesScanned: 0,
  });

  const [reminders, setReminders] = useState([]);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const dashboardResponse = await fetch(
          "http://127.0.0.1:8000/dashboard"
        );

        if (!dashboardResponse.ok) {
          throw new Error("Failed to load dashboard");
        }

        const dashboardData = await dashboardResponse.json();
        setStats(dashboardData);

        const remindersResponse = await fetch(
          "http://127.0.0.1:8000/reminders"
        );

        if (!remindersResponse.ok) {
          throw new Error("Failed to load reminders");
        }

        const remindersData = await remindersResponse.json();
        setReminders(remindersData);
      } catch (error) {
        console.error("Could not load dashboard:", error);
      }
    }

    loadDashboard();
  }, []);

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

        {reminders.length === 0 ? (
          <p>No reminders available.</p>
        ) : (
          reminders.map((reminder, index) => (
            <div className="reminder-card" key={index}>
              <div>
                <h3>{reminder.MedicineName}</h3>
                <p>Daily Dose: {reminder.DailyDose}</p>
              </div>

              <strong>{reminder.ReminderTime}</strong>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Dashboard;