import { useState } from "react";
import "./MedicineDetails.css";

function MedicineDetails() {
  const [medicines] = useState([
    {
      name: "Paracetamol",
      dosage: "500 mg",
      expiry: "December 2027",
      manufacturer: "Example Pharma",
      status: "Active",
    },
    {
      name: "Vitamin D",
      dosage: "1000 IU",
      expiry: "August 2026",
      manufacturer: "Health Pharma",
      status: "Active",
    },
  ]);

  return (
    <div className="medicine-details">
      <div className="page-header">
        <h1>My Medicines</h1>
        <p>View and manage your saved medicines.</p>
      </div>

      <div className="medicine-list">
        {medicines.map((medicine, index) => (
          <div className="medicine-card" key={index}>
            <div>
              <h2>{medicine.name}</h2>

              <p>Dosage: {medicine.dosage}</p>

              <p>Expiry: {medicine.expiry}</p>

              <p>Manufacturer: {medicine.manufacturer}</p>
            </div>

            <span className="medicine-status">
              {medicine.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MedicineDetails;