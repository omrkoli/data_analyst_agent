from fastapi import FastAPI, File, UploadFile
import pandas as pd
import numpy as np

app = FastAPI()

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    # Read the uploaded CSV file
    df = pd.read_csv(file.file)

    # Example analysis: Get numeric column statistics
    summary = df.describe(include=[np.number]).to_dict()

    # Convert numpy types to native Python for JSON serialization
    summary_clean = {
        col: {stat: float(val) if isinstance(val, (np.float64, np.int64)) else val
              for stat, val in stats.items()}
        for col, stats in summary.items()
    }

    return {"summary": summary_clean}
