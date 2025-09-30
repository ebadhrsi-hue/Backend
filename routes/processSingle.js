import express from "express";
import fs from "fs";
import path from "path";
import { spawn } from "child_process";
import { getOutputPath } from "../utils/paths.js";

const router = express.Router();

// Path to your Python executable
const PYTHON_PATH = path.join(".", "venv", "Scripts", "python.exe"); // Adjust if needed

router.post("/", async (req, res) => {
  try {
    if (!req.files || !req.files.file) {
      return res.status(400).send("Please upload a file with key 'file'.");
    }

    const file = req.files.file;
    const inputPath = file.tempFilePath; // temp file path from express-fileupload
    const outputPath = getOutputPath("processed_single.xlsx");

    const scriptPath = path.join("python_scripts", "process_single.py");

    const py = spawn(PYTHON_PATH, [scriptPath, inputPath, outputPath]);

    let stderr = "";
    let responded = false;

    // Timeout safeguard
    const timeout = setTimeout(() => {
      if (!responded) {
        responded = true;
        py.kill("SIGKILL");
        res.status(504).send("Processing timed out.");
      }
    }, 60000);

    py.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    py.on("close", (code) => {
      clearTimeout(timeout);
      if (responded) return;
      responded = true;

      // Clean up uploaded input file
      fs.existsSync(inputPath) && fs.unlinkSync(inputPath);

      if (code !== 0) {
        console.error("Python error:", stderr);
        return res.status(500).send("Processing failed.");
      }

      res.setHeader(
        "Content-Type",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      );
      res.setHeader(
        "Content-Disposition",
        'attachment; filename="processed_single.xlsx"'
      );

      const stream = fs.createReadStream(outputPath);
      stream.pipe(res);

      stream.on("close", () => {
        fs.existsSync(outputPath) && fs.unlinkSync(outputPath);
      });

      stream.on("error", (err) => {
        console.error("Stream error:", err);
        fs.existsSync(outputPath) && fs.unlinkSync(outputPath);
        if (!res.headersSent) {
          res.status(500).send("Failed to stream file.");
        }
      });
    });
  } catch (err) {
    console.error("Server error:", err);
    if (!res.headersSent) {
      res.status(500).send("Server error.");
    }
  }
});

export default router;
