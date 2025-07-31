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
  let lastDirection = 0;
  let currentAngle = 0;
  let currentY = -50;

  document.addEventListener('mousemove', (e) => {
    window.targetX = e.clientX;
    window.cursorY = e.clientY;

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
  spacecat.style.bottom = '-20px';
  spacecat.style.zIndex = '1000';

  animateCat();
});


document.addEventListener('DOMContentLoaded', () => {
  const email = document.getElementById('email');
  const login = document.getElementById('login');
  const password = document.getElementById('password');
  const repeatPassword = document.getElementById('repeat-password');
  const surname = document.getElementById('surname');
  const name = document.getElementById('name');
  const agreeFinal = document.getElementById('agree-final');
  const nextArrow = document.getElementById('next-arrow');
  const backArrow = document.getElementById('back-arrow');
  const step1 = document.getElementById('step-1');
  const step2 = document.getElementById('step-2');
  const submitBtn = document.getElementById('final-submit');

  function validateStep1() {
  const filled = email.value && login.value && password.value;
  const nextArrow = document.getElementById('next-arrow');
  if (filled) {
    nextArrow.disabled = false;
    nextArrow.classList.add('enabled');
  } else {
    nextArrow.disabled = true;
    nextArrow.classList.remove('enabled');
  }
}


  function validateStep2() {
    const valid =
      repeatPassword.value === password.value &&
      surname.value.trim() &&
      name.value.trim() &&
      agreeFinal.checked;

    submitBtn.disabled = !valid;
    submitBtn.classList.toggle('inactive', !valid);
  }

  [email, login, password].forEach(el =>
    el.addEventListener('input', validateStep1)
  );

  [repeatPassword, surname, name, agreeFinal].forEach(el =>
    el.addEventListener('input', validateStep2)
  );
  agreeFinal.addEventListener('change', validateStep2);

  nextArrow.addEventListener('click', () => {
    step1.classList.remove('visible');
    setTimeout(() => {
      step1.style.display = 'none';
      step2.style.display = 'block';
      requestAnimationFrame(() => step2.classList.add('visible'));
    }, 300);
  });

  backArrow.addEventListener('click', () => {
  step2.classList.remove('visible');
  setTimeout(() => {
    step2.style.display = 'none';
    step1.style.display = 'block';
    requestAnimationFrame(() => step1.classList.add('visible'));
  }, 300);
});


  validateStep1();
  validateStep2();

  const loginInput = document.querySelector('#login-form input[name="login"]');
  const passwordInput = document.querySelector('#login-form input[name="password"]');
  const loginButton = document.getElementById('login-button');

  function validateLoginForm() {
    const filled = loginInput.value.trim() && passwordInput.value.trim();
    loginButton.disabled = !filled;
    loginButton.classList.toggle('inactive', !filled);
  }

  [loginInput, passwordInput].forEach(el =>
    el.addEventListener('input', validateLoginForm)
  );

  validateLoginForm(); // Проверка при загрузке
});

document.getElementById('register-form').addEventListener('submit', function (event) {
  event.preventDefault(); // остановим обычную отправку

  const modal = document.getElementById('success-modal');
  modal.style.display = 'flex'; // покажем окно

  setTimeout(() => {
    this.submit(); // отправим форму через 3 секунды
  }, 3000);
});


document.addEventListener('DOMContentLoaded', () => {
  const phrase = "чтобы прокачать себя";
  const typedText = document.getElementById("typed-text");
  let index = 0;

  function type() {
    if (index <= phrase.length) {
      typedText.textContent = phrase.slice(0, index);
      index++;
      setTimeout(type, 90);
    }
  }

  type();
});
