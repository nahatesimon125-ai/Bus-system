import { spawn, execSync } from 'child_process';
import path from 'path';

console.log("=== LAUNCHING DJANGO SYSTEM DEPLOYMENT ===");

// 1. Run migrations/installs first to make sure database is solid on startup
try {
  console.log("Running prep hook...");
  execSync('node prepare-django.js', { stdio: 'inherit' });
} catch (err) {
  console.error("Prep hook failed, proceeding anyway...", err.message);
}

// 2. Start Django server spawning a live process binding to port 3000
const PORT = '3000';
const HOST = '0.0.0.0';

console.log(`Starting Django development server at http://${HOST}:${PORT}`);

const server = spawn('python3', ['manage.py', 'runserver', `${HOST}:${PORT}`], {
  stdio: 'inherit',
  shell: true
});

server.on('close', (code) => {
  console.log(`Django server exited with code ${code}`);
  process.exit(code);
});

process.on('SIGTERM', () => {
  console.log("Stopping server due to SIGTERM...");
  server.kill('SIGTERM');
});

process.on('SIGINT', () => {
  console.log("Stopping server due to SIGINT...");
  server.kill('SIGINT');
});
