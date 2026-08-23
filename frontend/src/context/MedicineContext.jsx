import { createContext, useContext, useEffect, useState } from "react";

const MedicineContext = createContext();

export function MedicineProvider({ children }) {
  const [medicines, setMedicines] = useState([]);

  useEffect(() => {
    async function loadMedicines() {
      try {
        const response = await fetch("http://127.0.0.1:8000/medicines");

        if (!response.ok) {
          throw new Error("Failed to load medicines");
        }

        const data = await response.json();

        const formattedMedicines = data.map((medicine) => ({
          id: medicine.MedicineID,
          UserID: medicine.UserID,
          name: medicine.MedicineName,
          MedicineName: medicine.MedicineName,
          expiry: medicine.ExpiryDate,
          ExpiryDate: medicine.ExpiryDate,
          quantity: medicine.Quantity,
          Quantity: medicine.Quantity,
          dailyDose: medicine.DailyDose,
          DailyDose: medicine.DailyDose,
          reminderTime: medicine.ReminderTime,
          ReminderTime: medicine.ReminderTime,
          startDate: medicine.StartDate,
          StartDate: medicine.StartDate,
        }));

        setMedicines(formattedMedicines);
      } catch (error) {
        console.error("Could not load medicines:", error);
      }
    }

    loadMedicines();
  }, []);

  function addMedicine(medicine) {
    setMedicines((previousMedicines) => [
      ...previousMedicines,
      medicine,
    ]);
  }

  return (
    <MedicineContext.Provider
      value={{
        medicines,
        addMedicine,
      }}
    >
      {children}
    </MedicineContext.Provider>
  );
}

export function useMedicines() {
  return useContext(MedicineContext);
}