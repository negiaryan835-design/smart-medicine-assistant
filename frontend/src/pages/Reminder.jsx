import { useState } from "react";
import "./Reminder.css";

function Reminder() {
  const [reminders] = useState([
    {
      medicine: "Paracetamol",
      dosage: "500 mg",
      time: "10:00 AM",
      frequency: "Daily",
    },
    {
      medicine: "Vitamin D",
      dosage: "1000 IU",
      time: "8:00 PM",
      frequency: "Daily",
    },
  ]);

  return (
    <div className="reminders-page">
      <div className="page-header">
        <h1>Reminders</h1>
        <p>Manage your medicine reminders.</p>
      </div>

      <div className="reminders-list">
        {reminders.map((reminder, index) => (
          <div className="reminder-item" key={index}>
            <div>
              <h2>{reminder.medicine}</h2>
              <p>Dosage: {reminder.dosage}</p>
              <p>Frequency: {reminder.frequency}</p>
            </div>

            <div className="reminder-time">
              {reminder.time}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Reminder;