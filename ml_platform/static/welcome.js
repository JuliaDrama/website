function showForm(formType) {
  const registerForm = document.getElementById('register-form');
  const loginForm = document.getElementById('login-form');
  const tabs = document.querySelectorAll('.tab');

  if (formType === 'register') {
    registerForm.style.display = 'block';
    loginForm.style.display = 'none';
    tabs[0].classList.add('active');
    tabs[1].classList.remove('active');
  } else {
    registerForm.style.display = 'none';
    loginForm.style.display = 'block';
    tabs[1].classList.add('active');
    tabs[0].classList.remove('active');
  }
}


document.querySelectorAll('.module-title').forEach(title => {
  title.addEventListener('click', () => {
    const next = title.nextElementSibling;
    if (next.style.display === 'block') {
      next.style.display = 'none';
    } else {
      next.style.display = 'block';
    }
  });
});


document.addEventListener('DOMContentLoaded', () => {
  const spacecat = document.getElementById('spacecat');
  if (!spacecat) return;

  let currentX = window.innerWidth / 2;
  let lastMouseX = currentX;
  let lastMoveTime = Date.now();
  let floatAngle = 0;
  let lastDirection = 0; // -1 = влево, 1 = вправо, 0 = нет движения
  let currentAngle = 0;

  document.addEventListener('mousemove', (e) => {
    window.targetX = e.clientX;

    const dx = e.clientX - lastMouseX;
    if (Math.abs(dx) > 1) {
      lastDirection = dx > 0 ? 1 : -1;
      lastMouseX = e.clientX;
      lastMoveTime = Date.now();
    }
  });

function animateCat() {
  const targetX = typeof window.targetX === 'number' ? window.targetX : currentX;
  const clampedX = Math.max(30, Math.min(targetX, window.innerWidth - 130));

  // Плавное движение по оси X
  currentX += (clampedX - currentX) * 0.002;
  spacecat.style.left = `${currentX}px`;

  const now = Date.now();
  const idle = now - lastMoveTime > 1000;

  if (idle) {
    // Постепенно возвращаемся в ноль
    currentAngle += (0 - currentAngle) * 0.02;

    // Когда угол почти выровнялся, начинаем покачиваться
    if (Math.abs(currentAngle) < 0.5) {
      floatAngle += 0.03;
      currentAngle = Math.sin(floatAngle) * 5;
    }
  } else {
    // Активное движение: поворот влево/вправо
    const targetAngle = lastDirection * 12; // до ±12 градусов
    currentAngle += (targetAngle - currentAngle) * 0.05;
  }

  spacecat.style.transform = `rotate(${currentAngle}deg)`;
  requestAnimationFrame(animateCat);
}



  spacecat.style.position = 'fixed';
  spacecat.style.bottom = '20px';
  spacecat.style.zIndex = '1000';

  animateCat();
});
