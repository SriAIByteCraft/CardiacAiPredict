/**
 * UI Utilities, Toast Notifications, Modal Helper, and Navigation Sync.
 */

import { authAPI } from './api.js';

/**
 * Toast Notification System
 */
export function showToast(message, type = 'info', duration = 4000) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  const textNode = document.createElement('span');
  textNode.textContent = message;
  toast.appendChild(textNode);

  const closeBtn = document.createElement('button');
  closeBtn.innerHTML = '&times;';
  closeBtn.style.background = 'none';
  closeBtn.style.border = 'none';
  closeBtn.style.fontSize = '1.25rem';
  closeBtn.style.cursor = 'pointer';
  closeBtn.style.color = '#64748b';
  closeBtn.onclick = () => toast.remove();
  toast.appendChild(closeBtn);

  container.appendChild(toast);

  setTimeout(() => {
    if (toast.parentElement) {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }
  }, duration);
}

/**
 * Updates navigation links based on user authentication state.
 */
export async function initNavigation() {
  const navContainer = document.querySelector('.navbar');
  if (!navContainer) return;

  // Setup mobile menu toggle
  const toggleBtn = navContainer.querySelector('.navbar-toggle');
  const navMenu = navContainer.querySelector('.navbar-nav');
  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      navMenu.classList.toggle('show');
    });
  }

  // Active page link highlight
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = navContainer.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // Check authentication session
  try {
    const res = await authAPI.getMe();
    const user = res.data?.user;
    updateNavForAuthUser(user);
  } catch (err) {
    updateNavForGuest();
  }
}

function updateNavForAuthUser(user) {
  const authLinksContainer = document.getElementById('nav-auth-container');
  if (!authLinksContainer) return;

  authLinksContainer.innerHTML = '';

  // Profile link
  const profileLink = document.createElement('a');
  profileLink.href = 'profile.html';
  profileLink.className = 'nav-link';
  profileLink.textContent = user.name ? `👤 ${user.name.split(' ')[0]}` : 'Profile';
  authLinksContainer.appendChild(profileLink);

  // Logout button
  const logoutBtn = document.createElement('button');
  logoutBtn.className = 'btn btn-outline btn-sm';
  logoutBtn.textContent = 'Sign Out';
  logoutBtn.onclick = async () => {
    try {
      await authAPI.logout();
      showToast('Signed out successfully.', 'info');
      setTimeout(() => {
        window.location.href = 'login.html';
      }, 500);
    } catch (e) {
      window.location.href = 'login.html';
    }
  };
  authLinksContainer.appendChild(logoutBtn);
}

function updateNavForGuest() {
  const authLinksContainer = document.getElementById('nav-auth-container');
  if (!authLinksContainer) return;

  authLinksContainer.innerHTML = `
    <a href="login.html" class="btn btn-outline btn-sm">Sign In</a>
    <a href="register.html" class="btn btn-primary btn-sm">Register</a>
  `;
}

/**
 * Modal dialog controller
 */
export function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('show');
  }
}

export function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('show');
  }
}

/**
 * Format ISO datetime to localized string
 */
export function formatDateTime(isoString) {
  if (!isoString) return 'N/A';
  try {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch {
    return isoString;
  }
}

// Auto-run navigation initialization on DOM ready
document.addEventListener('DOMContentLoaded', initNavigation);
