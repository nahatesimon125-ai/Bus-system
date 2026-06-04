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

// 2. Start Django server spawning a live process. Respect environment PORT if provided (e.g., Vercel).
const PORT = process.env.PORT || '3000';
const HOST = '0.0.0.0';

console.log(`Starting Django development server at http://${HOST}:${PORT}`);

// Prefer running via gunicorn in production/docker, but fallback to runserver for local dev
let serverCmd, serverArgs;
if (process.env.VERCEL || process.env.NODE_ENV === 'production') {
  serverCmd = 'gunicorn';
  serverArgs = ['nts_project.wsgi:application', '--bind', `${HOST}:${PORT}`, '--workers', '2'];
} else {
  serverCmd = 'python3';
  serverArgs = ['manage.py', 'runserver', `${HOST}:${PORT}`];
}

const server = spawn(serverCmd, serverArgs, {
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
