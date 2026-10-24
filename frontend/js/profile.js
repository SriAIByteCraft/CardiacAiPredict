/**
 * User Profile Management Controller.
 * Handles profile viewing, name updates, and secure password modifications.
 */

import { requireAuth } from './auth.js';
import { profileAPI, authAPI } from './api.js';
import { showToast, formatDateTime } from './ui.js';

export async function initProfilePage() {
  const user = await requireAuth();

  loadProfile(user);

  // Profile Update Form
  const profileForm = document.getElementById('profile-form');
  if (profileForm) {
    profileForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = profileForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;

      const newName = profileForm.name.value.trim();
      if (!newName) {
        showToast('Please provide your name.', 'error');
        return;
      }

      try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner"></span> Updating...';

        const res = await profileAPI.update({ name: newName });
        showToast(res.message || 'Profile updated successfully!', 'success');
        
        // Update header greeting if present
        const greetName = document.getElementById('profile-header-name');
        if (greetName) greetName.textContent = newName;

      } catch (err) {
        showToast(err.message, 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }

  // Password Change Form
  const passwordForm = document.getElementById('password-form');
  if (passwordForm) {
    passwordForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = passwordForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;

      const currentPassword = passwordForm.current_password.value;
      const newPassword = passwordForm.new_password.value;
      const confirmPassword = passwordForm.confirm_new_password.value;

      if (newPassword !== confirmPassword) {
        showToast('New passwords do not match.', 'error');
        return;
      }

      if (newPassword.length < 8) {
        showToast('New password must be at least 8 characters long.', 'error');
        return;
      }

      try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner"></span> Saving New Password...';

        const res = await profileAPI.changePassword({
          current_password: currentPassword,
          new_password: newPassword,
          confirm_new_password: confirmPassword
        });

        showToast(res.message || 'Password changed successfully!', 'success');
        passwordForm.reset();

      } catch (err) {
        showToast(err.message, 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }

  // Sign out button
  const logoutBtn = document.getElementById('profile-logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      try {
        await authAPI.logout();
        showToast('Signed out successfully.', 'info');
        setTimeout(() => {
          window.location.href = 'login.html';
        }, 500);
      } catch {
        window.location.href = 'login.html';
      }
    });
  }
}

function loadProfile(user) {
  const nameInput = document.getElementById('profile-name-input');
  if (nameInput) nameInput.value = user.name || '';

  const emailInput = document.getElementById('profile-email-input');
  if (emailInput) emailInput.value = user.email || '';

  const headerName = document.getElementById('profile-header-name');
  if (headerName) headerName.textContent = user.name || 'User';

  const memberSince = document.getElementById('profile-member-since');
  if (memberSince && user.created_at) {
    memberSince.textContent = `Member since ${formatDateTime(user.created_at)}`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('profile-view')) {
    initProfilePage();
  }
});
