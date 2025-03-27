/* Lain-themed form effects for profile and other forms */

document.addEventListener('DOMContentLoaded', function() {
    // Enhance form containers with terminal-like effects
    const formContainers = document.querySelectorAll('.form-container');
    
    formContainers.forEach(container => {
        enhanceFormContainer(container);
    });
    
    // Add scanlines effect
    const scanlines = document.createElement('div');
    scanlines.className = 'form-scanlines';
    scanlines.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, 
            rgba(0, 0, 0, 0), 
            rgba(0, 0, 0, 0) 50%, 
            rgba(0, 184, 212, 0.03) 50%, 
            rgba(0, 184, 212, 0.03));
        background-size: 100% 4px;
        z-index: 9998;
        pointer-events: none;
        opacity: 0.2;
    `;
    document.body.appendChild(scanlines);
    
    // Function to enhance the form container with terminal effects
    function enhanceFormContainer(container) {
        // Skip already enhanced containers
        if (container.classList.contains('lain-enhanced')) return;
        container.classList.add('lain-enhanced');
        
        // Add glitch effect
        const glitchOverlay = document.createElement('div');
        glitchOverlay.className = 'form-glitch-overlay';
        glitchOverlay.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 184, 212, 0.05);
            z-index: 5;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s ease;
        `;
        container.appendChild(glitchOverlay);
        
        // Random glitch effect
        setInterval(() => {
            if (Math.random() > 0.9) {
                glitchOverlay.style.opacity = '0.2';
                setTimeout(() => {
                    glitchOverlay.style.opacity = '0';
                }, 100);
            }
        }, 3000);
        
        // Add terminal-style cursor to inputs on focus
        const inputs = container.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="url"], textarea');
        
        inputs.forEach(input => {
            // Add focus effect
            input.addEventListener('focus', function() {
                // Add a subtle glitch effect
                glitchOverlay.style.opacity = '0.1';
                setTimeout(() => {
                    glitchOverlay.style.opacity = '0';
                }, 150);
                
                // Add terminal cursor if not readonly
                if (!this.hasAttribute('readonly')) {
                    this.style.caretColor = '#33ff33';
                }
            });
            
            // Add typing sound effect
            input.addEventListener('keydown', function(e) {
                // Skip if it's a modifier key or if field is readonly
                if (e.ctrlKey || e.altKey || e.metaKey || this.hasAttribute('readonly')) return;
                
                // Add a subtle transform effect
                if (Math.random() > 0.7) {
                    container.style.transform = `translateX(${(Math.random() - 0.5) * 2}px)`;
                    setTimeout(() => {
                        container.style.transform = 'translateX(0)';
                    }, 50);
                }
            });
        });
        
        // Enhance avatar section if it exists
        const avatarSection = container.querySelector('.avatar-section');
        if (avatarSection) {
            enhanceAvatarSection(avatarSection);
        }
        
        // Add form header terminal effect
        const formHeader = container.querySelector('.form-header');
        if (formHeader) {
            const title = formHeader.querySelector('h1, h2, h3');
            if (title && !title.classList.contains('terminal-typed')) {
                title.classList.add('terminal-typed');
                
                // Store original text
                const originalText = title.textContent;
                title.textContent = '';
                
                // Create typed text container
                const typedTextSpan = document.createElement('span');
                typedTextSpan.className = 'typed-text';
                title.appendChild(typedTextSpan);
                
                // Create cursor
                const cursorSpan = document.createElement('span');
                cursorSpan.className = 'cursor';
                cursorSpan.innerHTML = '|';
                cursorSpan.style.animation = 'blink 1s infinite';
                title.appendChild(cursorSpan);
                
                // Start typing effect
                let charIndex = 0;
                const typeInterval = setInterval(() => {
                    if (charIndex < originalText.length) {
                        typedTextSpan.textContent += originalText.charAt(charIndex);
                        charIndex++;
                    } else {
                        clearInterval(typeInterval);
                        setTimeout(() => {
                            cursorSpan.style.display = 'none';
                        }, 1500);
                    }
                }, 70);
            }
        }
        
        // Enhance submit button
        const submitButton = container.querySelector('.form-submit button');
        if (submitButton) {
            submitButton.addEventListener('mouseenter', function() {
                const randomGlitch = Math.random() > 0.5;
                if (randomGlitch) {
                    glitchOverlay.style.opacity = '0.15';
                    setTimeout(() => {
                        glitchOverlay.style.opacity = '0';
                    }, 100);
                }
            });
            
            submitButton.addEventListener('click', function() {
                // Add loading effect
                this.disabled = true;
                const originalText = this.textContent;
                this.textContent = "Processing...";
                
                // Add loading animation
                const loadingInterval = setInterval(() => {
                    if (this.textContent.endsWith('...')) {
                        this.textContent = this.textContent.replace('...', '');
                    } else {
                        this.textContent += '.';
                    }
                }, 300);
                
                // Reset after 2 seconds if form doesn't submit (for demo)
                setTimeout(() => {
                    clearInterval(loadingInterval);
                    this.textContent = originalText;
                    this.disabled = false;
                }, 10000); // Long timeout as form should actually submit
            });
        }
    }
    
    // Function to enhance avatar section
    function enhanceAvatarSection(section) {
        // Add terminal-style effect to the file input
        const fileInput = section.querySelector('input[type="file"]');
        const avatarPreview = section.querySelector('.avatar-preview');
        
        if (fileInput && avatarPreview) {
            fileInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    
                    // Add a glitch effect during loading
                    avatarPreview.style.filter = 'hue-rotate(90deg) brightness(1.2)';
                    setTimeout(() => {
                        avatarPreview.style.filter = '';
                    }, 300);
                    
                    reader.onload = function(e) {
                        // Check if preview contains image or text
                        const existingImg = avatarPreview.querySelector('img');
                        
                        if (existingImg) {
                            existingImg.src = e.target.result;
                        } else {
                            // Clear content and add image
                            avatarPreview.innerHTML = '';
                            const img = document.createElement('img');
                            img.src = e.target.result;
                            avatarPreview.appendChild(img);
                        }
                    }
                    
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }
    }
    
    // Add keyframe animation for blinking cursor if not already defined
    if (!document.querySelector('#lain-form-keyframes')) {
        const styleSheet = document.createElement('style');
        styleSheet.id = 'lain-form-keyframes';
        styleSheet.innerHTML = `
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
        `;
        document.head.appendChild(styleSheet);
    }
}); 