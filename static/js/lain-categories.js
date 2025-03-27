/* Lain-themed category browsing effects */

document.addEventListener('DOMContentLoaded', function() {
    // Set a flag to indicate JavaScript is loaded and running
    document.body.classList.add('js-loaded');
    
    // Ensure headers are visible by default
    const allHeaders = document.querySelectorAll('.category-title, .category-list-title, .son-yazilar-title, .tags-title');
    allHeaders.forEach(header => {
        // Make sure headers are visible immediately
        header.style.opacity = '1';
        header.style.visibility = 'visible';
        
        // Add a fallback mechanism
        if (header.textContent.trim() === '') {
            header.textContent = header.getAttribute('data-default-text') || 'Title';
        }
    });

    // Delay the typing effect slightly to ensure text is visible first
    setTimeout(() => {
        // Add terminal typing effect to page titles
        const categoryTitles = document.querySelectorAll('.category-title, .category-list-title, .son-yazilar-title, .tags-title');
        categoryTitles.forEach(title => {
            addTypingEffect(title);
        });
    }, 300);

    // Add hover effects to category cards
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        addCategoryCardEffects(card);
    });

    // Add effects to son yazılar cards
    const sonYazilarCards = document.querySelectorAll('.son-yazılar-card');
    sonYazilarCards.forEach(card => {
        addSonYazilarCardEffects(card);
    });

    // Terminal effect for empty state containers
    enhanceEmptyStates();
});

// Function to add typing effect to titles
function addTypingEffect(element) {
    const originalText = element.textContent.trim();
    
    // Skip if already processed or empty
    if (element.getAttribute('data-processed') === 'true' || !originalText) return;
    element.setAttribute('data-processed', 'true');
    
    // Store the original text in a data attribute
    element.setAttribute('data-original-text', originalText);
    
    // Create overlay elements without removing the original text
    const overlayContainer = document.createElement('div');
    overlayContainer.className = 'typing-effect-overlay';
    overlayContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        z-index: 10;
        pointer-events: none;
    `;
    
    const typedTextSpan = document.createElement('span');
    typedTextSpan.className = 'typed-text';
    typedTextSpan.style.cssText = `
        color: #00b8d4;
        text-shadow: 0 0 5px rgba(0, 184, 212, 0.5);
        position: relative;
    `;
    
    const cursorSpan = document.createElement('span');
    cursorSpan.className = 'typing-cursor';
    cursorSpan.textContent = '|';
    cursorSpan.style.cssText = `
        color: #33ff33;
        animation: blink 1s infinite step-end;
    `;
    
    overlayContainer.appendChild(typedTextSpan);
    overlayContainer.appendChild(cursorSpan);
    
    // Add a background behind the typing effect to hide the original text
    const backgroundDiv = document.createElement('div');
    backgroundDiv.className = 'typing-effect-background';
    backgroundDiv.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 0%; /* Start at 0% and animate to 100% */
        height: 100%;
        background-color: #000;
        z-index: 5;
        transition: width 0.05s ease;
    `;
    
    element.style.position = 'relative';
    element.appendChild(backgroundDiv);
    element.appendChild(overlayContainer);
    
    // Add typing animation CSS if not already present
    if (!document.getElementById('typing-animation-css')) {
        const style = document.createElement('style');
        style.id = 'typing-animation-css';
        style.textContent = `
            @keyframes blink {
                from, to { opacity: 1; }
                50% { opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Type out the text
    let i = 0;
    const typeNextChar = () => {
        if (i < originalText.length) {
            // Expand background to cover the typed portion
            backgroundDiv.style.width = ((i + 1) / originalText.length * 100) + '%';
            
            typedTextSpan.textContent += originalText.charAt(i);
            i++;
            
            // Random typing speed for more realistic effect
            setTimeout(typeNextChar, Math.random() * 50 + 30);
        } else {
            // Animation complete
            setTimeout(() => {
                cursorSpan.style.animation = 'none';
                cursorSpan.style.opacity = '0';
                
                // Clean up - remove the overlay elements
                setTimeout(() => {
                    if (element.contains(overlayContainer)) {
                        element.removeChild(overlayContainer);
                    }
                    if (element.contains(backgroundDiv)) {
                        element.removeChild(backgroundDiv);
                    }
                }, 1000);
            }, 1000);
        }
    };
    
    // Start typing after a short delay
    setTimeout(typeNextChar, 300);
}

// Function to add effects to category cards
function addCategoryCardEffects(card) {
    // Glitch effect on hover
    card.addEventListener('mouseenter', function() {
        const title = this.querySelector('h3');
        if (title) {
            glitchText(title);
        }
        
        // Add scanline effect
        if (!this.querySelector('.scanline-effect')) {
            const scanline = document.createElement('div');
            scanline.className = 'scanline-effect';
            scanline.style.cssText = `
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(
                    transparent 0%,
                    transparent 50%,
                    rgba(0, 184, 212, 0.03) 50%,
                    rgba(0, 184, 212, 0.03) 100%
                );
                background-size: 100% 4px;
                pointer-events: none;
                opacity: 0;
                z-index: 1;
                transition: opacity 0.3s ease;
            `;
            this.appendChild(scanline);
            
            // Fade in the scanline effect
            setTimeout(() => {
                scanline.style.opacity = '0.5';
            }, 50);
        }
    });
    
    // Remove scanline effect on mouse leave
    card.addEventListener('mouseleave', function() {
        const scanline = this.querySelector('.scanline-effect');
        if (scanline) {
            scanline.style.opacity = '0';
            setTimeout(() => {
                scanline.remove();
            }, 300);
        }
    });
    
    // Random glitch effect occasionally
    setInterval(() => {
        if (Math.random() > 0.97) {
            const icon = card.querySelector('.category-icon');
            if (icon) {
                // Brief color change
                const originalColor = window.getComputedStyle(icon).color;
                icon.style.color = '#33ff33';
                icon.style.textShadow = '0 0 10px rgba(51, 255, 51, 0.7)';
                
                setTimeout(() => {
                    icon.style.color = originalColor;
                    icon.style.textShadow = '';
                }, 200);
            }
        }
    }, 5000);
}

// Function to add effects to son yazılar cards
function addSonYazilarCardEffects(card) {
    // Add hover effect to read more links
    const readMoreLink = card.querySelector('.read-more');
    if (readMoreLink) {
        readMoreLink.addEventListener('mouseenter', function() {
            this.style.letterSpacing = '1px';
        });
        
        readMoreLink.addEventListener('mouseleave', function() {
            this.style.letterSpacing = 'normal';
        });
    }
    
    // Add random effect to card occasionally
    setInterval(() => {
        if (Math.random() > 0.98) {
            // Brief border flash
            const originalBorder = card.style.borderColor;
            card.style.borderColor = '#33ff33';
            card.style.boxShadow = '0 0 15px rgba(51, 255, 51, 0.3)';
            
            setTimeout(() => {
                card.style.borderColor = originalBorder;
                card.style.boxShadow = '';
            }, 200);
        }
    }, 8000);
}

// Function to glitch text temporarily
function glitchText(element) {
    const originalText = element.textContent;
    const glitchChars = '!<>-_\\/[]{}—=+*^?#________';
    let iterations = 0;
    const maxIterations = 5;
    
    const glitchInterval = setInterval(() => {
        if (iterations >= maxIterations) {
            clearInterval(glitchInterval);
            element.textContent = originalText;
            return;
        }
        
        // Create glitched text by randomly replacing characters
        let glitchedText = '';
        for (let i = 0; i < originalText.length; i++) {
            if (Math.random() < 0.2) { // 20% chance to glitch each character
                glitchedText += glitchChars[Math.floor(Math.random() * glitchChars.length)];
            } else {
                glitchedText += originalText[i];
            }
        }
        
        element.textContent = glitchedText;
        iterations++;
    }, 100);
}

// Function to enhance empty states with terminal-like displays
function enhanceEmptyStates() {
    const emptyStates = document.querySelectorAll('.empty-state');
    
    emptyStates.forEach(container => {
        // Skip if already enhanced
        if (container.classList.contains('lain-enhanced')) return;
        container.classList.add('lain-enhanced');
        
        // Create terminal header
        const header = document.createElement('div');
        header.className = 'connection-status';
        header.innerHTML = `<span>connection-status</span>••`;
        
        // Create terminal content with blinking cursor
        const content = document.createElement('div');
        content.className = 'terminal-content';
        
        // Add terminal lines
        const lines = [
            '$ fetch data --from-layer 7',
            'Error: data unreachable • connection timeout',
            'Protocol error • | Şu anda kullanılabilir etiket bulunmamaktadır.',
            '$ retry --connection',
            '$'
        ];
        
        // Add lines with typing effect
        content.innerHTML = '';
        lines.forEach((line, index) => {
            const terminalLine = document.createElement('div');
            terminalLine.className = 'terminal-line';
            
            // Last line gets blinking cursor
            if (index === lines.length - 1) {
                terminalLine.innerHTML = line + ' <span class="blinking-cursor">█</span>';
            } else {
                terminalLine.textContent = line;
            }
            
            content.appendChild(terminalLine);
        });
        
        // Clear and add new elements
        container.innerHTML = '';
        container.appendChild(header);
        container.appendChild(content);
        
        // Add warning icon if appropriate
        if (!container.querySelector('.warning-icon')) {
            const warningIcon = document.createElement('div');
            warningIcon.className = 'warning-icon';
            warningIcon.innerHTML = `<i class="fas fa-exclamation-triangle"></i>`;
            warningIcon.style.cssText = `
                color: #ffcc00;
                font-size: 2rem;
                margin: 1rem auto;
                text-align: center;
                text-shadow: 0 0 10px rgba(255, 204, 0, 0.5);
            `;
            
            // Insert after header
            container.insertBefore(warningIcon, content);
        }
    });
} 