import { useMedicines } from "../context/MedicineContext";
import "./MedicineDetails.css";

function MedicineDetails() {
  const { medicines } = useMedicines();

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
          {medicines.map((medicine, index) => (
            <div className="medicine-card" key={index}>
              <div>
                <h2>{medicine.name}</h2>
                <p>Dosage: {medicine.dosage}</p>
                <p>Expiry: {medicine.expiry}</p>
                <p>Manufacturer: {medicine.manufacturer}</p>
              </div>

              <span className="medicine-status">
                Active
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MedicineDetails;