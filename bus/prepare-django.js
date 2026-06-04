import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

console.log("=== DJANGO PRE-BUILD PREPARATION START ===");

const runCommand = (cmd) => {
  try {
    console.log(`Running: ${cmd}`);
    const out = execSync(cmd, { encoding: 'utf-8', stdio: 'inherit' });
    return true;
  } catch (err) {
    console.error(`FAILED: ${cmd} - Error: ${err.message}`);
    return false;
  }
};

// 1. Ensure get-pip.py is available if pip is missing
try {
  execSync('python3 -m pip --version', { stdio: 'ignore' });
  console.log("Pip is already installed.");
} catch {
  console.log("Pip is missing. Fetching pip...");
  if (!fs.existsSync('get-pip.py')) {
    runCommand('curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py');
  }
  runCommand('python3 get-pip.py --user');
}

// 2. Ensure django package is installed
try {
  execSync('python3 -m django --version', { stdio: 'ignore' });
  console.log("Django is already installed.");
} catch {
  console.log("Django package is missing. Installing...");
  runCommand('python3 -m pip install django');
}

// 3. Make and run migrations
console.log("Creating Django application database migrations...");
runCommand('python3 manage.py makemigrations tickets');

console.log("Executing SQLite migrations...");
runCommand('python3 manage.py migrate');

console.log("=== DJANGO PRE-BUILD PREPARATION COMPLETE ===");
