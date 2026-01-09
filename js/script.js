document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.textContent = navMenu.classList.contains('active') ? '×' : '☰';
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });

                if (navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    hamburger.textContent = '☰';
                }
            }
        });
    });

    const fontSizeBtn = document.querySelector('.font-size-btn');
    const contrastBtn = document.querySelector('.contrast-btn');
    const screenReaderBtn = document.querySelector('.screen-reader-btn');

    if (fontSizeBtn) {
        fontSizeBtn.addEventListener('click', function() {
            const currentSize = document.body.style.fontSize || '16px';
            const newSize = currentSize === '16px' ? '18px' : currentSize === '18px' ? '20px' : '16px';
            document.body.style.fontSize = newSize;
            this.setAttribute('aria-label', `Font size: ${newSize}`);
        });
    }

    if (contrastBtn) {
        contrastBtn.addEventListener('click', function() {
            document.body.classList.toggle('high-contrast');
            const isHighContrast = document.body.classList.contains('high-contrast');
            this.setAttribute('aria-label', `High contrast mode: ${isHighContrast ? 'on' : 'off'}`);
        });
    }

    if (screenReaderBtn) {
        screenReaderBtn.addEventListener('click', function() {
            const announcement = document.createElement('div');
            announcement.className = 'sr-only';
            announcement.setAttribute('aria-live', 'polite');
            announcement.textContent = 'Navigation assistance activated. Use arrow keys to navigate between interactive elements.';
            document.body.appendChild(announcement);

            setTimeout(() => {
                announcement.remove();
            }, 3000);
        });
    }

    const style = document.createElement('style');
    style.innerHTML = `
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }
        
        .high-contrast {
            background-color: #000 !important;
            color: #fff !important;
        }
        
        .high-contrast * {
            background-color: #000 !important;
            color: #fff !important;
            border-color: #fff !important;
        }
        
        .high-contrast .btn {
            background-color: #fff !important;
            color: #000 !important;
        }
    `;
    document.head.appendChild(style);

    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.feature-card, .bot-card');

        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;

            if (elementPosition < screenPosition) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    document.querySelectorAll('.feature-card, .bot-card').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    });

    window.addEventListener('scroll', animateOnScroll);
    setTimeout(animateOnScroll, 500);
});

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.button');

    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.zIndex = '10';
        });

        button.addEventListener('mouseleave', function() {
            this.style.zIndex = '1';
        });

        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = `${e.clientX - this.getBoundingClientRect().left}px`;
            ripple.style.top = `${e.clientY - this.getBoundingClientRect().top}px`;
            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});