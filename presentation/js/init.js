// Initialize Reveal.js with custom configuration
Reveal.initialize({
    // Display settings - responsive
    width: 1280,
    height: 720,
    margin: 0.1,
    minScale: 0.2,
    maxScale: 2.0,

    // Navigation
    controls: true,
    controlsLayout: 'bottom-right',
    controlsBackArrows: 'faded',
    progress: true,
    slideNumber: false, // Hide slide numbers
    hash: true,
    keyboard: true,
    overview: true,
    center: true,
    touch: true,
    loop: false,
    rtl: false,
    navigationMode: 'linear',

    // Transitions
    transition: 'slide', // none/fade/slide/convex/concave/zoom
    transitionSpeed: 'default', // default/fast/slow
    backgroundTransition: 'fade',

    // Plugins
    plugins: [
        RevealHighlight,
        RevealNotes,
        RevealZoom
    ],

    // Code highlighting settings
    highlight: {
        highlightOnLoad: true,
        escapeHTML: true
    },

    // Auto-animate settings
    autoAnimateEasing: 'ease',
    autoAnimateDuration: 0.6,
    autoAnimateUnmatched: true,

    // Fragment settings
    fragmentInURL: false,

    // View distance
    viewDistance: 3,
    mobileViewDistance: 2
});

// Custom event listeners
Reveal.on('ready', event => {
    console.log('🚀 AI Workshop Presentation Ready!');
    console.log('📊 Total slides:', Reveal.getTotalSlides());

    // Initialize fullscreen button
    const button = createFullscreenButton();

    // Click event
    button.addEventListener('click', toggleFullscreen);

    // Listen for fullscreen changes
    document.addEventListener('fullscreenchange', updateFullscreenButton);
    document.addEventListener('webkitfullscreenchange', updateFullscreenButton);
    document.addEventListener('mozfullscreenchange', updateFullscreenButton);
    document.addEventListener('MSFullscreenChange', updateFullscreenButton);
});

// Slide change event
Reveal.on('slidechanged', event => {
    // Log slide number
    console.log('Current slide:', event.indexh + 1);

    // Add smooth animation class to current slide
    const currentSlide = event.currentSlide;
    currentSlide.style.animation = 'fadeIn 0.5s ease-out';
});

// Fragment shown event
Reveal.on('fragmentshown', event => {
    // Add custom animations for specific fragments
    const fragment = event.fragment;

    // Add pulse animation to hand icons
    if (fragment.querySelector('.hand-icon')) {
        const handIcon = fragment.querySelector('.hand-icon');
        handIcon.style.animation = 'pulse 0.5s ease-out';
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Press 'B' to toggle background color (for testing)
    if (e.key === 'b' || e.key === 'B') {
        document.body.style.background =
            document.body.style.background === 'black' ? '' : 'black';
    }

    // Press 'G' to toggle grid (for testing)
    if (e.key === 'g' || e.key === 'G') {
        const currentSlide = Reveal.getCurrentSlide();
        currentSlide.classList.toggle('show-grid');
    }
});

// Smooth code typing animation (optional enhancement)
function typeCode(element, speed = 50) {
    const code = element.textContent;
    element.textContent = '';
    let i = 0;

    const interval = setInterval(() => {
        if (i < code.length) {
            element.textContent += code.charAt(i);
            i++;
        } else {
            clearInterval(interval);
        }
    }, speed);
}

// Add pulse animation for hand icons
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.2);
        }
    }
`;
document.head.appendChild(style);

// Console styling
console.log(
    '%c AI Workshop Presentation ',
    'background: #1a1d2e; color: #00ff87; font-size: 20px; font-weight: bold; padding: 10px; font-family: monospace;'
);
console.log(
    '%c Powered by Reveal.js ',
    'background: #00ff87; color: #1a1d2e; font-size: 14px; padding: 5px; font-family: monospace;'
);

// ============================================
// FULLSCREEN BUTTON
// ============================================

// Create fullscreen button
function createFullscreenButton() {
    const button = document.createElement('button');
    button.id = 'fullscreen-btn';
    button.className = 'fullscreen-button';
    button.innerHTML = `
        <svg class="fullscreen-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
        </svg>
        <svg class="exit-fullscreen-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
            <path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"></path>
        </svg>
    `;
    button.title = 'Toggle Fullscreen (F)';
    document.body.appendChild(button);
    return button;
}

// Toggle fullscreen function
function toggleFullscreen() {
    const elem = document.documentElement;
    const button = document.getElementById('fullscreen-btn');
    const enterIcon = button.querySelector('.fullscreen-icon');
    const exitIcon = button.querySelector('.exit-fullscreen-icon');

    if (!document.fullscreenElement && !document.webkitFullscreenElement &&
        !document.mozFullScreenElement && !document.msFullscreenElement) {
        // Enter fullscreen
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.webkitRequestFullscreen) {
            elem.webkitRequestFullscreen();
        } else if (elem.mozRequestFullScreen) {
            elem.mozRequestFullScreen();
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        }
    } else {
        // Exit fullscreen
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
}

// Update button icon based on fullscreen state
function updateFullscreenButton() {
    const button = document.getElementById('fullscreen-btn');
    if (!button) return;

    const enterIcon = button.querySelector('.fullscreen-icon');
    const exitIcon = button.querySelector('.exit-fullscreen-icon');

    if (document.fullscreenElement || document.webkitFullscreenElement ||
        document.mozFullScreenElement || document.msFullscreenElement) {
        enterIcon.style.display = 'none';
        exitIcon.style.display = 'block';
        button.title = 'Exit Fullscreen (F or Esc)';
    } else {
        enterIcon.style.display = 'block';
        exitIcon.style.display = 'none';
        button.title = 'Toggle Fullscreen (F)';
    }
}

// Add keyboard shortcut (F key) for fullscreen
document.addEventListener('keydown', (e) => {
    if (e.key === 'f' || e.key === 'F') {
        e.preventDefault();
        toggleFullscreen();
    }
});
