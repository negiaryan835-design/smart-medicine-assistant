import { useState } from "react";
import { useMedicines } from "../context/MedicineContext";
import "./ScanMedicine.css";

function ScanMedicine() {
  const { addMedicine } = useMedicines();

  const [selectedImage, setSelectedImage] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [medicineResult, setMedicineResult] = useState(null);

  const [quantity, setQuantity] = useState("");
  const [dailyDose, setDailyDose] = useState("");
  const [startDate, setStartDate] = useState(
    new Date().toISOString().split("T")[0]
  );
  const [expiryDate, setExpiryDate] = useState("");
  const [reminderTime, setReminderTime] = useState("");

  function handleImageChange(event) {
    const file = event.target.files[0];

    if (file) {
      setImageFile(file);
      setSelectedImage(URL.createObjectURL(file));
      setMedicineResult(null);
    }
  }

  async function handleAnalyze() {
    if (!imageFile) return;

    setIsAnalyzing(true);

    const formData = new FormData();
    formData.append("file", imageFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      const data = await response.json();

      setMedicineResult({
        name: data.medicine,
        confidence: data.confidence,
        dosage: data.ocr?.strength || "Not available",
        manufacturer: data.ocr?.manufacturer || "Not available",
      });
    } catch (error) {
      console.error(error);
      alert("Could not analyze the medicine.");
    } finally {
      setIsAnalyzing(false);
    }
  }

  async function handleSaveMedicine() {
  if (!medicineResult) return;

  if (!quantity || !dailyDose || !expiryDate || !reminderTime) {
    alert("Please fill all medicine details.");
    return;
  }

  const medicineData = {
    UserID: 1,
    MedicineName: medicineResult.name,
    ExpiryDate: expiryDate,
    Quantity: Number(quantity),
    DailyDose: Number(dailyDose),
    ReminderTime: reminderTime,
    StartDate: startDate,
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/medicines", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(medicineData),
    });

    if (!response.ok) {
      throw new Error("Failed to save medicine");
    }

    const refillResponse = await fetch(
      "http://127.0.0.1:8000/refill-prediction",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          quantity_left: Number(quantity),
          daily_dose: Number(dailyDose),
          adherence_rate: 1.0,
          missed_doses: 0,
        }),
      }
    );

    if (!refillResponse.ok) {
      throw new Error("Refill prediction failed");
    }

    const refillData = await refillResponse.json();

    const savedMedicine = {
      ...medicineResult,
      ...medicineData,
      predictedDaysUntilRefill:
        refillData.predicted_days_until_refill,
      predictedRefillDate:
        refillData.predicted_refill_date,
    };

    addMedicine(savedMedicine);

    setMedicineResult(savedMedicine);

    alert("Medicine saved and refill prediction calculated!");
  } catch (error) {
    console.error(error);
    alert("Could not save medicine.");
  }
}

  function handleScanAgain() {
    setSelectedImage(null);
    setImageFile(null);
    setMedicineResult(null);
    setQuantity("");
    setDailyDose("");
    setExpiryDate("");
    setReminderTime("");
    setStartDate(new Date().toISOString().split("T")[0]);
  }

  return (
    <div className="scan-page">
      <div className="scan-header">
        <h1>Scan Medicine</h1>
        <p>Upload an image of your medicine to identify it.</p>
      </div>

      <div className="upload-card">
        <h2>Upload Medicine Image</h2>

        <p>
          Take a clear photo of the medicine strip, bottle, or packaging.
        </p>

        <label className="upload-box">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />

          {selectedImage ? (
            <img
              src={selectedImage}
              alt="Selected medicine"
            />
          ) : (
            <>
              <span>📷</span>
              <p>Click here to upload an image</p>
            </>
          )}
        </label>

        {selectedImage && (
          <button
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={isAnalyzing}
          >
            {isAnalyzing ? "Analyzing..." : "Analyze Medicine"}
          </button>
        )}

        {medicineResult && (
          <div className="medicine-result-card">
            <h2>Medicine Details</h2>

            <div className="result-item">
              <strong>Medicine Name:</strong>
              <span>{medicineResult.name}</span>
            </div>

            <div className="result-item">
              <strong>Confidence:</strong>
              <span>
                {(medicineResult.confidence * 100).toFixed(2)}%
              </span>
            </div>

            <div className="result-item">
              <strong>Strength:</strong>
              <span>{medicineResult.dosage}</span>
            </div>

            <div className="result-item">
              <strong>Manufacturer:</strong>
              <span>{medicineResult.manufacturer}</span>
            </div>

            <div className="result-item">
              <strong>Quantity:</strong>
              <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                placeholder="e.g. 14"
              />
            </div>

            <div className="result-item">
              <strong>Daily Dose:</strong>
              <input
                type="number"
                min="1"
                value={dailyDose}
                onChange={(e) => setDailyDose(e.target.value)}
                placeholder="e.g. 2"
              />
            </div>

            <div className="result-item">
              <strong>Start Date:</strong>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>

            <div className="result-item">
              <strong>Expiry Date:</strong>
              <input
                type="date"
                value={expiryDate}
                onChange={(e) => setExpiryDate(e.target.value)}
              />
            </div>

            <div className="result-item">
              <strong>Reminder Time:</strong>
              <input
                type="time"
                value={reminderTime}
                onChange={(e) => setReminderTime(e.target.value)}
              />
            </div>
            {medicineResult.predictedDaysUntilRefill !== undefined && (
  <>
    <div className="result-item">
      <strong>Refill In:</strong>
      <span>
        {medicineResult.predictedDaysUntilRefill} days
      </span>
    </div>

    <div className="result-item">
      <strong>Predicted Refill Date:</strong>
      <span>
        {medicineResult.predictedRefillDate}
      </span>
    </div>
  </>
)}

            <button
              className="save-medicine-button"
              onClick={handleSaveMedicine}
            >
              Save Medicine
            </button>

            <button
              className="scan-again-button"
              onClick={handleScanAgain}
            >
              Scan Another Medicine
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ScanMedicine;  