document.addEventListener('DOMContentLoaded', () => {
    const observerOptions = {
        threshold: 0.1,
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('section').forEach((section) => {
        observer.observe(section);
    });

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            const target = document.querySelector(href);
            if (!target) return;
            e.preventDefault();
            const header = document.querySelector('.header-nav');
            const headerHeight = header ? header.getBoundingClientRect().height + 12 : 12;
            const top = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });

    const text = 'Senior Python Developer | Linux Specialist | Software Engineering Student';
    let i = 0;
    const typingElement = document.getElementById('typing-text');

    function type() {
        if (typingElement && i < text.length) {
            typingElement.innerHTML += text.charAt(i);
            i += 1;
            setTimeout(type, 50);
        }
    }

    if (typingElement) {
        typingElement.innerHTML = '';
        type();
    }
});
