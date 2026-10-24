/**
 * Authentication Controllers and Route Guards.
 */

import { authAPI } from './api.js';
import { showToast } from './ui.js';

/**
 * Route guard: Redirects unauthenticated visitors to login.html.
 */
export async function requireAuth() {
  try {
    const res = await authAPI.getMe();
    return res.data?.user;
  } catch (err) {
    // Store current page for post-login redirect
    const currentPath = window.location.pathname.split('/').pop();
    window.location.href = `login.html?redirect=${encodeURIComponent(currentPath)}`;
    throw new Error('Unauthorized');
  }
}

/**
 * Redirects already logged in users away from login/register to dashboard.html.
 */
export async function redirectIfAuthenticated() {
  try {
    const res = await authAPI.getMe();
    if (res.data?.user) {
      window.location.href = 'dashboard.html';
    }
  } catch {
    // User not authenticated, remain on login/register page
  }
}

/**
 * Initialize Register Form
 */
export function initRegisterForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;

    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const password = form.password.value;
    const confirmPassword = form.confirm_password.value;

    if (password !== confirmPassword) {
      showToast('Passwords do not match.', 'error');
      return;
    }

    if (password.length < 8) {
      showToast('Password must be at least 8 characters long.', 'error');
      return;
    }

    try {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner"></span> Creating Account...';

      const res = await authAPI.register({
        name,
        email,
        password,
        confirm_password: confirmPassword
      });

      showToast('Account registered successfully! Redirecting...', 'success');
      setTimeout(() => {
        window.location.href = 'dashboard.html';
      }, 1000);
    } catch (err) {
      showToast(err.message, 'error');
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });
}

/**
 * Initialize Login Form
 */
export function initLoginForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;

    const email = form.email.value.trim();
    const password = form.password.value;

    try {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner"></span> Signing in...';

      const res = await authAPI.login({ email, password });
      showToast('Login successful! Redirecting...', 'success');

      const params = new URLSearchParams(window.location.search);
      const redirect = params.get('redirect') || 'dashboard.html';

      setTimeout(() => {
        window.location.href = redirect;
      }, 800);
    } catch (err) {
      showToast(err.message, 'error');
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });
}
