import { useEffect, useState } from "react";
import "./Reminder.css";

function Reminder() {
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [taken, setTaken] = useState({});

  async function loadReminders() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/reminders"
      );

      if (!response.ok) {
        throw new Error("Failed to load reminders");
      }

      const data = await response.json();
      setReminders(data);
    } catch (error) {
      console.error("Could not load reminders:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadReminders();
  }, []);

  async function markAsTaken(reminder) {
    try {
      const medicinesResponse = await fetch(
        "http://127.0.0.1:8000/medicines"
      );

      const medicines = await medicinesResponse.json();

      const medicine = medicines.find(
        (item) =>
          item.MedicineName === reminder.MedicineName
      );

      if (!medicine) {
        alert("Medicine not found.");
        return;
      }

      const now = new Date();

      const response = await fetch(
        "http://127.0.0.1:8000/medicinelog",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            MedicineID: medicine.MedicineID,
            TakenDate: now.toISOString().split("T")[0],
            TakenTime: now.toTimeString().slice(0, 8),
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to record dose");
      }

      setTaken((previous) => ({
        ...previous,
        [medicine.MedicineID]: true,
      }));

      alert(`${reminder.MedicineName} marked as taken.`);
    } catch (error) {
      console.error(error);
      alert("Could not record the dose.");
    }
  }

  if (loading) {
    return (
      <div className="reminders-page">
        <div className="page-header">
          <h1>Reminders</h1>
          <p>Loading your reminders...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="reminders-page">
      <div className="page-header">
        <h1>Reminders</h1>
        <p>Manage your medicine reminders.</p>
      </div>

      <div className="reminders-list">
        {reminders.length === 0 ? (
          <p>No medicines added yet.</p>
        ) : (
          reminders.map((reminder) => (
            <div
              className="reminder-item"
              key={reminder.MedicineName}
            >
              <div>
                <h2>{reminder.MedicineName}</h2>
                <p>Daily Dose: {reminder.DailyDose}</p>
                <p>Frequency: Daily</p>
              </div>

              <div className="reminder-time">
                {reminder.ReminderTime}
              </div>

              <button
                onClick={() => markAsTaken(reminder)}
                disabled={taken[reminder.MedicineID]}
              >
                {taken[reminder.MedicineID]
                  ? "Taken ✓"
                  : "Mark as Taken"}
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Reminder;