import { useEffect, useState } from "react";
import { useMedicines } from "../context/MedicineContext";
import "./MedicineDetails.css";

function MedicineDetails() {
  const { medicines } = useMedicines();
  const [predictions, setPredictions] = useState({});

  useEffect(() => {
    async function loadPredictions() {
      const results = {};

      for (const medicine of medicines) {
        if (!medicine.id) continue;

        try {
          const response = await fetch(
            `http://127.0.0.1:8000/medicines/${medicine.id}/refill-prediction`
          );

          if (!response.ok) continue;

          const data = await response.json();

          results[medicine.id] = data;
        } catch (error) {
          console.error(
            `Could not load refill prediction for ${medicine.name}:`,
            error
          );
        }
      }

      setPredictions(results);
    }

    if (medicines.length > 0) {
      loadPredictions();
    }
  }, [medicines]);

  return (
    <div className="medicine-details">
      <div className="page-header">
        <h1>My Medicines</h1>
        <p>View and manage your saved medicines.</p>
      </div>

      {medicines.length === 0 ? (
        <div className="empty-state">
          <h2>No medicines saved yet</h2>
          <p>Scan a medicine to add it to your collection.</p>
        </div>
      ) : (
        <div className="medicine-list">
          {medicines.map((medicine) => {
            const prediction = predictions[medicine.id];

            return (
              <div className="medicine-card" key={medicine.id}>
                <div>
                  <h2>{medicine.name}</h2>

                  <p>
                    Dosage:{" "}
                    {medicine.dosage || medicine.DailyDose || "Not available"}
                  </p>

                  <p>
                    Quantity:{" "}
                    {medicine.Quantity ?? medicine.quantity ?? "Not available"}
                  </p>

                  <p>
                    Expiry:{" "}
                    {medicine.ExpiryDate ||
                      medicine.expiry ||
                      "Not available"}
                  </p>

                  <p>
                    Manufacturer:{" "}
                    {medicine.manufacturer || "Not available"}
                  </p>

                  {prediction && !prediction.error && (
                    <>
                      <p>
                        <strong>Quantity Left:</strong>{" "}
                        {prediction.quantity_left}
                      </p>

                      <p>
                        <strong>Adherence:</strong>{" "}
                        {(prediction.adherence_rate * 100).toFixed(0)}%
                      </p>

                      <p>
                        <strong>Missed Doses:</strong>{" "}
                        {prediction.missed_doses}
                      </p>

                      <p>
                        <strong>Refill In:</strong>{" "}
                        {prediction.predicted_days_until_refill} days
                      </p>

                      <p>
                        <strong>Predicted Refill Date:</strong>{" "}
                        {prediction.predicted_refill_date}
                      </p>
                    </>
                  )}

                  {!prediction && (
                    <p>Loading refill prediction...</p>
                  )}
                </div>

                <span className="medicine-status">
                  Active
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default MedicineDetails;