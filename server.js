import "dotenv/config";
import path from "path";
import express from "express";
import cors from "cors";
import fileUpload from "express-fileupload";


import authRoute from "./routes/auth.js";
import { ensureFolders } from "./utils/paths.js";
import processMultiRoute from "./routes/processMulti.js";
import processSingleRoute from "./routes/processSingle.js";


const app = express();
const PORT = process.env.PORT || 5000;

// CORS (allow your CRA frontend at 3000)
app.use(cors({ origin: [
  'http://localhost:3000',
  'http://192.168.1.165:3000',
  "http://DESKTOP-GELE1R0:3000",
  "https://f25b3e0067f9.ngrok-free.app"
],
  methods: ["GET", "POST"],       // allow methods you need
  credentials: true               // if you send cookies/auth
}));






app.use(express.json());

// fileupload: use temp files so Python can read by path
app.use(
  fileUpload({
    useTempFiles: true,
    tempFileDir: path.join(process.cwd(), "uploads"),
    limits: { fileSize: 100 * 1024 * 1024 } // 100 MB per file (adjust)
  })
);

// make sure folders exist
ensureFolders();

// routes
app.use("/api/auth", authRoute);
app.use("/api/process-multi", processMultiRoute);
app.use("/api/process-single", processSingleRoute);

app.get("/", (_req, res) => res.send("Backend running"));

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server listening on http://0.0.0.0:${PORT}`);
});
