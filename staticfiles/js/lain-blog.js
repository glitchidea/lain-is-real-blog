/* Lain-themed blog post effects */

document.addEventListener('DOMContentLoaded', function() {
    // Add glitch effect to post title
    const postTitle = document.querySelector('.post-title');
    if (postTitle) {
        addGlitchEffect(postTitle);
    }
    
    // Add terminal effect to code blocks
    enhanceCodeBlocks();
    
    // Add interactive effects to comments
    enhanceComments();
    
    // Add special effects to blockquotes
    enhanceBlockquotes();
    
    // Add random glitch effect to featured image
    const featuredImage = document.querySelector('.post-featured-image img');
    if (featuredImage) {
        featuredImage.addEventListener('mouseenter', function() {
            this.style.filter = 'hue-rotate(90deg) brightness(1.2) contrast(1.2)';
            setTimeout(() => {
                this.style.filter = '';
            }, 200);
        });
        
        // Random glitch effect
        setInterval(() => {
            if (Math.random() > 0.95) {
                featuredImage.style.filter = 'hue-rotate(90deg) brightness(1.2) contrast(1.2)';
                setTimeout(() => {
                    featuredImage.style.filter = '';
                }, 150);
            }
        }, 5000);
    }
    
    // Add hover effect to share buttons
    const shareButtons = document.querySelectorAll('.share-button');
    shareButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            const randomY = Math.random() * 5 - 2.5;
            this.style.transform = `translateY(${randomY}px)`;
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // Add special effect for future publish notice
    const futurePublishNotice = document.querySelector('.future-publish-notice');
    if (futurePublishNotice) {
        setInterval(() => {
            if (Math.random() > 0.7) {
                const timeLeft = futurePublishNotice.querySelector('.time-left');
                if (timeLeft) {
                    timeLeft.style.color = '#33ff33';
                    setTimeout(() => {
                        timeLeft.style.color = '#00b8d4';
                    }, 200);
                }
            }
        }, 3000);
    }
});

// Function to add glitch effect to elements
function addGlitchEffect(element) {
    // Store original content
    const originalText = element.textContent;
    
    // Add data attribute for glitch effect
    element.setAttribute('data-text', originalText);
    
    // Add event listener for hover
    element.addEventListener('mouseenter', function() {
        glitchElement(this);
    });
    
    // Occasionally glitch the element
    setInterval(() => {
        if (Math.random() > 0.95) {
            glitchElement(element);
        }
    }, 5000);
}

// Function to create glitch effect on an element
function glitchElement(element) {
    const originalText = element.getAttribute('data-text');
    const glitchChars = '!<>-_\\/[]{}—=+*^?#________';
    const duration = 1000; // Total duration in ms
    const intervals = 50;  // Number of intervals
    let intervalCounter = 0;
    
    const glitchInterval = setInterval(() => {
        intervalCounter++;
        
        if (intervalCounter < intervals) {
            // During glitch - randomly replace characters
            if (Math.random() < 0.3) { // Only glitch sometimes for better effect
                let glitchedText = '';
                for (let i = 0; i < originalText.length; i++) {
                    if (Math.random() < 0.1) {
                        glitchedText += glitchChars[Math.floor(Math.random() * glitchChars.length)];
                    } else {
                        glitchedText += originalText[i];
                    }
                }
                element.textContent = glitchedText;
            }
        } else {
            // End glitch
            element.textContent = originalText;
            clearInterval(glitchInterval);
        }
    }, duration / intervals);
}

// Function to enhance code blocks with terminal styling
function enhanceCodeBlocks() {
    const codeBlocks = document.querySelectorAll('.markdown-content pre');
    
    codeBlocks.forEach(block => {
        // Skip already enhanced blocks
        if (block.classList.contains('lain-enhanced')) return;
        block.classList.add('lain-enhanced');
        
        // Create terminal header
        const header = document.createElement('div');
        header.className = 'terminal-header';
        header.innerHTML = `
            <span class="terminal-title">terminal</span>
            <div class="terminal-buttons">
                <span class="terminal-button"></span>
                <span class="terminal-button"></span>
                <span class="terminal-button"></span>
            </div>
        `;
        
        // Style the header
        header.style.cssText = `
            background: rgba(0, 0, 0, 0.7);
            padding: 8px 10px;
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #333;
            margin: -15px -15px 10px -15px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 12px;
        `;
        
        header.querySelector('.terminal-title').style.color = '#aaa';
        
        const buttons = header.querySelectorAll('.terminal-button');
        buttons.forEach(btn => {
            btn.style.cssText = `
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #444;
                margin-left: 5px;
            `;
        });
        
        // Insert header before content
        block.insertBefore(header, block.firstChild);
        
        // Random blinking cursor at the end of code blocks
        if (Math.random() > 0.5) {
            const cursor = document.createElement('span');
            cursor.className = 'blinking-cursor';
            cursor.textContent = '|';
            cursor.style.cssText = `
                color: #33ff33;
                animation: blink 1s infinite;
                margin-left: 2px;
            `;
            block.appendChild(cursor);
            
            // Create CSS animation if not exists
            if (!document.querySelector('#blinking-cursor-animation')) {
                const style = document.createElement('style');
                style.id = 'blinking-cursor-animation';
                style.textContent = `
                    @keyframes blink {
                        0%, 100% { opacity: 1; }
                        50% { opacity: 0; }
                    }
                `;
                document.head.appendChild(style);
            }
        }
        
        // Add highlight-on-hover effect
        block.addEventListener('mouseenter', function() {
            this.style.borderColor = '#00b8d4';
            this.style.boxShadow = '0 0 15px rgba(0, 184, 212, 0.3)';
        });
        
        block.addEventListener('mouseleave', function() {
            this.style.borderColor = 'rgba(0, 184, 212, 0.3)';
            this.style.boxShadow = 'none';
        });
    });
}

// Function to enhance comments section
function enhanceComments() {
    // Add typing effects to comment textareas
    const commentTextareas = document.querySelectorAll('.comment-form textarea, .reply-form textarea');
    
    commentTextareas.forEach(textarea => {
        textarea.addEventListener('focus', function() {
            // Add subtle terminal style cursor color
            this.style.caretColor = '#33ff33';
            
            // Add a console-like placeholder
            if (!this.value) {
                this.setAttribute('data-original-placeholder', this.placeholder || '');
                this.placeholder = '> start typing...';
            }
        });
        
        textarea.addEventListener('blur', function() {
            // Reset placeholder
            if (this.getAttribute('data-original-placeholder')) {
                this.placeholder = this.getAttribute('data-original-placeholder');
            }
        });
        
        // Add keystroke sounds (minimal)
        textarea.addEventListener('keydown', function() {
            if (Math.random() > 0.9) {
                const container = this.closest('.comment-form-container, .reply-form-container');
                if (container) {
                    container.style.transform = `translateX(${(Math.random() - 0.5) * 2}px)`;
                    setTimeout(() => {
                        container.style.transform = 'translateX(0)';
                    }, 50);
                }
            }
        });
    });
    
    // Add effects to comment buttons
    const commentButtons = document.querySelectorAll('.comment-form button, .reply-form button');
    
    commentButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.textShadow = '0 0 5px rgba(51, 255, 51, 0.5)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.textShadow = 'none';
        });
    });
    
    // Add hover effect to reply and delete buttons
    const actionButtons = document.querySelectorAll('.reply-button, .delete-button, .cancel-reply');
    
    actionButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            const isDelete = this.classList.contains('delete-button');
            this.style.textShadow = isDelete ? 
                '0 0 5px rgba(255, 64, 64, 0.5)' :
                '0 0 5px rgba(0, 184, 212, 0.5)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.textShadow = 'none';
        });
    });
    
    // Add subtle focus effect to comments on hover
    const comments = document.querySelectorAll('.comment');
    
    comments.forEach(comment => {
        comment.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 0 15px rgba(0, 0, 0, 0.3)';
            this.style.backgroundColor = 'rgba(0, 0, 0, 0.6)';
            
            // Add scanline effect
            if (!this.querySelector('.comment-scanline')) {
                const scanline = document.createElement('div');
                scanline.className = 'comment-scanline';
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
                    opacity: 0.2;
                    z-index: 0;
                `;
                this.appendChild(scanline);
            }
        });
        
        comment.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'none';
            this.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            
            const scanline = this.querySelector('.comment-scanline');
            if (scanline) {
                scanline.remove();
            }
        });
    });
}

// Function to enhance blockquotes
function enhanceBlockquotes() {
    const blockquotes = document.querySelectorAll('.markdown-content blockquote');
    
    blockquotes.forEach(quote => {
        // Skip already enhanced blocks
        if (quote.classList.contains('lain-enhanced')) return;
        quote.classList.add('lain-enhanced');
        
        // Add terminal-style quote header
        const header = document.createElement('div');
        header.className = 'quote-header';
        header.textContent = '// message from the wired';
        header.style.cssText = `
            color: #00b8d4;
            font-family: 'Share Tech Mono', monospace;
            font-size: 12px;
            margin-bottom: 10px;
            opacity: 0.8;
        `;
        
        quote.insertBefore(header, quote.firstChild);
        
        // Add hover effect
        quote.addEventListener('mouseenter', function() {
            this.style.borderLeftColor = '#33ff33';
            this.style.boxShadow = '0 0 10px rgba(51, 255, 51, 0.2)';
            this.style.backgroundColor = 'rgba(0, 184, 212, 0.1)';
            header.style.color = '#33ff33';
        });
        
        quote.addEventListener('mouseleave', function() {
            this.style.borderLeftColor = '#00b8d4';
            this.style.boxShadow = 'none';
            this.style.backgroundColor = 'rgba(0, 184, 212, 0.05)';
            header.style.color = '#00b8d4';
        });
    });
} 