/* Lain-inspired effects for Cyber Nexus */

document.addEventListener('DOMContentLoaded', function() {
    // Create glitch overlay
    const glitchOverlay = document.createElement('div');
    glitchOverlay.className = 'glitch-overlay';
    document.body.appendChild(glitchOverlay);
    
    // Random glitch effect
    setInterval(() => {
        if (Math.random() > 0.9) {
            glitchOverlay.classList.add('active');
            setTimeout(() => {
                glitchOverlay.classList.remove('active');
            }, 200);
        }
    }, 3000);
    
    // Add scanlines overlay
    const scanlines = document.createElement('div');
    scanlines.className = 'scanlines';
    scanlines.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, rgba(0,0,0,0) 50%, rgba(0,0,0,0.02) 50%);
        background-size: 100% 4px;
        z-index: 9998;
        pointer-events: none;
        opacity: 0.2;
    `;
    document.body.appendChild(scanlines);
    
    // Terminal typing effect for headings
    const headings = document.querySelectorAll('h1:not(.typed), h2:not(.typed), h3:not(.typed), .section-title:not(.typed)');
    
    headings.forEach(heading => {
        // Skip already processed headings
        if (heading.classList.contains('typed')) return;
        
        const text = heading.innerText;
        heading.innerText = '';
        heading.classList.add('typed');
        
        // Create a span to hold the typed text
        const typedSpan = document.createElement('span');
        typedSpan.className = 'typed-text';
        heading.appendChild(typedSpan);
        
        // Create cursor element
        const cursor = document.createElement('span');
        cursor.className = 'cursor';
        cursor.innerHTML = '|';
        cursor.style.animation = 'blink 1s infinite';
        heading.appendChild(cursor);
        
        // Type out the text
        let i = 0;
        const typeInterval = setInterval(() => {
            if (i < text.length) {
                typedSpan.innerHTML += text.charAt(i);
                i++;
            } else {
                clearInterval(typeInterval);
                // Remove cursor after typing is done
                setTimeout(() => {
                    cursor.style.display = 'none';
                }, 1500);
            }
        }, 50);
    });
    
    // Enhance empty state messages
    enhanceEmptyStates();
    
    // Add Lain quotes that randomly appear
    const lainQuotes = [
        "Present day, present time...",
        "In the Wired, all are connected.",
        "You don't seem to understand...",
        "The border between the real and virtual is disappearing.",
        "No matter where you go, everyone's connected.",
        "If you're not remembered, you never existed.",
        "I am God.",
        "Let's all love Lain."
    ];
    
    function showRandomQuote() {
        if (Math.random() > 0.95) {
            const quote = lainQuotes[Math.floor(Math.random() * lainQuotes.length)];
            
            const quoteElement = document.createElement('div');
            quoteElement.className = 'lain-quote';
            quoteElement.textContent = quote;
            quoteElement.style.cssText = `
                position: fixed;
                color: rgba(0, 184, 212, 0.8);
                font-family: monospace;
                font-size: 12px;
                z-index: 9997;
                text-shadow: 0 0 5px rgba(0, 184, 212, 0.5);
                pointer-events: none;
                opacity: 0;
                transition: opacity 2s;
            `;
            
            // Random position
            quoteElement.style.left = Math.random() * 80 + 10 + '%';
            quoteElement.style.top = Math.random() * 80 + 10 + '%';
            
            document.body.appendChild(quoteElement);
            
            // Fade in
            setTimeout(() => {
                quoteElement.style.opacity = '1';
            }, 100);
            
            // Remove after some time
            setTimeout(() => {
                quoteElement.style.opacity = '0';
                setTimeout(() => {
                    quoteElement.remove();
                }, 2000);
            }, 5000);
        }
    }
    
    // Check periodically for showing a random quote
    setInterval(showRandomQuote, 8000);
    
    // Add binary digits that float up randomly
    function createBinaryDigit() {
        if (Math.random() > 0.9) {
            const digit = document.createElement('div');
            digit.className = 'binary-digit';
            digit.textContent = Math.round(Math.random()).toString();
            
            // Set position at the bottom of the screen
            digit.style.cssText = `
                position: fixed;
                bottom: -20px;
                color: rgba(51, 255, 51, 0.5);
                font-family: monospace;
                font-size: ${Math.random() * 14 + 10}px;
                z-index: 9996;
                pointer-events: none;
                animation: float-up ${Math.random() * 15 + 10}s linear forwards;
            `;
            
            // Random horizontal position
            digit.style.left = Math.random() * 100 + '%';
            
            document.body.appendChild(digit);
            
            // Remove after animation
            setTimeout(() => {
                digit.remove();
            }, 25000);
        }
    }
    
    // Add keyframe animation for floating digits
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes float-up {
            0% {
                transform: translateY(0);
                opacity: 0.5;
            }
            80% {
                opacity: 0.2;
            }
            100% {
                transform: translateY(-100vh);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Create binary digits periodically
    setInterval(createBinaryDigit, 300);
    
    // Add static noise effect on hover for links
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('mouseover', () => {
            if (Math.random() > 0.7) {
                glitchOverlay.classList.add('active');
                setTimeout(() => {
                    glitchOverlay.classList.remove('active');
                }, 150);
            }
        });
    });
    
    // Function to enhance empty state messages
    function enhanceEmptyStates() {
        // Find all empty state messages
        const emptyElements = document.querySelectorAll('.empty-state, [class*="No Posts"], [class*="No Featured Posts"], [class*="No Posts Found"]');
        
        emptyElements.forEach(element => {
            // Skip already processed elements
            if (element.classList.contains('lain-enhanced')) return;
            
            // Mark as enhanced
            element.classList.add('lain-enhanced');
            
            // Original text
            const originalText = element.textContent.trim();
            
            // Clear the content
            element.innerHTML = '';
            
            // Add terminal style header
            const header = document.createElement('div');
            header.className = 'empty-terminal-header';
            header.style.cssText = `
                background-color: rgba(0, 0, 0, 0.7);
                padding: 8px;
                margin: -15px -15px 15px -15px;
                border-bottom: 1px solid var(--lain-accent);
                display: flex;
                justify-content: space-between;
                align-items: center;
            `;
            
            const headerTitle = document.createElement('span');
            headerTitle.textContent = 'connection-status';
            headerTitle.style.cssText = `
                color: var(--lain-accent);
                font-family: monospace;
                font-size: 12px;
            `;
            
            const headerButtons = document.createElement('div');
            headerButtons.style.cssText = `
                display: flex;
                gap: 5px;
            `;
            
            for (let i = 0; i < 3; i++) {
                const btn = document.createElement('span');
                btn.style.cssText = `
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    background-color: #444;
                `;
                headerButtons.appendChild(btn);
            }
            
            header.appendChild(headerTitle);
            header.appendChild(headerButtons);
            element.appendChild(header);
            
            // Create content container
            const content = document.createElement('div');
            content.className = 'empty-terminal-content';
            content.style.cssText = `
                padding: 15px;
                min-height: 100px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            `;
            
            // Create icon (or use existing)
            const iconElement = document.createElement('div');
            iconElement.className = 'empty-icon';
            iconElement.innerHTML = '<i class="fas fa-exclamation-triangle" style="font-size: 2rem; color: var(--lain-accent); margin-bottom: 1rem;"></i>';
            
            // Create message with terminal-style
            const messageContainer = document.createElement('div');
            messageContainer.style.cssText = `
                text-align: left;
                width: 100%;
                max-width: 400px;
                margin: 0 auto;
            `;
            
            // Line 1: Command
            const line1 = document.createElement('div');
            line1.className = 'terminal-line';
            line1.innerHTML = '<span style="color: var(--lain-green); margin-right: 8px;">$</span> <span style="color: #f0f0f0;">fetch data --from-layer 7</span>';
            
            // Line 2: Error
            const line2 = document.createElement('div');
            line2.className = 'terminal-line';
            line2.innerHTML = '<span style="color: #ff00a5;">Error:</span> <span style="color: #aaa;">data unreachable • connection timeout</span>';
            
            // Line 3: Details
            const line3 = document.createElement('div');
            line3.className = 'terminal-line';
            line3.innerHTML = `<span style="color: #aaa;">Protocol error • ${originalText}</span>`;
            
            // Line 4: Status
            const line4 = document.createElement('div');
            line4.className = 'terminal-line';
            line4.innerHTML = '<span style="color: var(--lain-green); margin-right: 8px;">$</span> <span style="color: #f0f0f0;">retry --connection</span>';
            
            // Line 5: Waiting cursor
            const line5 = document.createElement('div');
            line5.className = 'terminal-line';
            line5.innerHTML = '<span style="color: var(--lain-green); margin-right: 8px;">$</span> <span style="color: #f0f0f0;"></span><span class="cursor" style="animation: blink 1s infinite;">|</span>';
            
            // Add lines to message container
            messageContainer.appendChild(line1);
            messageContainer.appendChild(line2);
            messageContainer.appendChild(line3);
            messageContainer.appendChild(line4);
            messageContainer.appendChild(line5);
            
            // Add all elements to content
            content.appendChild(iconElement);
            content.appendChild(messageContainer);
            
            // Add content to main element
            element.appendChild(content);
            
            // Add occasional glitch
            setInterval(() => {
                if (Math.random() > 0.9) {
                    element.style.transform = `translateX(${(Math.random() - 0.5) * 3}px)`;
                    setTimeout(() => {
                        element.style.transform = 'translateX(0)';
                    }, 100);
                }
            }, 3000);
        });
        
        // Enhance headers for section titles
        const specialHeaders = document.querySelectorAll('[class*="latest_posts"], [class*="View All"], [class*="Categories"], [class*="Popular Tags"]');
        
        specialHeaders.forEach(header => {
            if (header.classList.contains('lain-enhanced')) return;
            
            header.classList.add('lain-enhanced');
            const text = header.textContent.trim();
            
            // Convert to lowercase and add cyberpunk style prefix
            header.textContent = '//' + text.toLowerCase();
        });
    }
}); 