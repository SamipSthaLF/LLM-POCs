const { spawn } = require("child_process");
const path = require("path");

function runPythonCommand(args, callback) {
  const script = path.join(__dirname, "../stylemail/cli.py");
  const proc = spawn("python3", [script, ...args]);

  let output = "";
  proc.stdout.on("data", (data) => (output += data.toString()));
  proc.stderr.on("data", (data) => console.error(data.toString()));
  proc.on("close", () => callback(output.trim()));
}

function seedUserStyle(userId, samples, callback) {
  runPythonCommand(["seed", userId, ...samples], callback);
}

function generateEmail(userId, prompt, callback) {
  runPythonCommand(["generate", userId, prompt], callback);
}

module.exports = { seedUserStyle, generateEmail };
