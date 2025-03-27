// Lain Profile Page Effects

document.addEventListener('DOMContentLoaded', () => {
    // Apply glitch effect to article titles on hover
    const articleTitles = document.querySelectorAll('.profile-article-title a');
    articleTitles.forEach(title => {
        title.addEventListener('mouseenter', () => {
            applyGlitchEffect(title);
        });
    });

    // Apply typing effect to section headers
    const sectionHeaders = document.querySelectorAll('.profile-articles-header');
    sectionHeaders.forEach(header => {
        applyTypingEffect(header);
    });

    // Add dynamic focus effect on profile stats
    const statItems = document.querySelectorAll('.profile-stat');
    statItems.forEach(stat => {
        stat.addEventListener('mouseenter', () => {
            stat.querySelector('.number').style.textShadow = '0 0 10px rgba(0, 184, 212, 0.8)';
            stat.style.transform = 'scale(1.05)';
            stat.style.transition = 'all 0.3s ease';
        });
        
        stat.addEventListener('mouseleave', () => {
            stat.querySelector('.number').style.textShadow = '0 0 5px rgba(0, 184, 212, 0.5)';
            stat.style.transform = 'scale(1)';
        });
    });

    // Add connection-style effect for tabs
    const tabs = document.querySelectorAll('.profile-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Add connection animation
            const tabContent = document.querySelector('.tab-content');
            tabContent.style.opacity = '0';
            setTimeout(() => {
                tabContent.style.opacity = '1';
            }, 300);
            
            // Console-style message in browser console
            console.log(`%c[LAIN]%c Accessing ${tab.textContent.trim()} data...`, 
                'color: #33ff33; font-weight: bold;', 
                'color: #00b8d4;');
        });
    });
});

// Function to apply glitch effect to elements
function applyGlitchEffect(element) {
    const originalText = element.textContent;
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
                    if (Math.random() < 0.2) {
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

// Function to apply typing effect to elements
function applyTypingEffect(element) {
    const text = element.textContent;
    element.textContent = '';
    element.style.borderRight = '2px solid #00b8d4';
    element.style.display = 'inline-block';
    element.style.whiteSpace = 'nowrap';
    
    let i = 0;
    const typingSpeed = 70; // ms per character
    
    function typeChar() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(typeChar, typingSpeed + Math.random() * 50);
        } else {
            // Remove cursor effect when done
            setTimeout(() => {
                element.style.borderRight = 'none';
            }, 500);
        }
    }
    
    setTimeout(typeChar, 500); // Small delay before starting
}

// Add occasional glitch effect to the entire page
function addRandomPageGlitch() {
    const glitchDuration = 200;
    const body = document.body;
    
    // Create and add glitch overlay
    const glitchOverlay = document.createElement('div');
    glitchOverlay.style.position = 'fixed';
    glitchOverlay.style.top = '0';
    glitchOverlay.style.left = '0';
    glitchOverlay.style.width = '100%';
    glitchOverlay.style.height = '100%';
    glitchOverlay.style.backgroundColor = 'rgba(0, 184, 212, 0.03)';
    glitchOverlay.style.mixBlendMode = 'difference';
    glitchOverlay.style.pointerEvents = 'none';
    glitchOverlay.style.zIndex = '9999';
    glitchOverlay.style.transform = 'translateX(-5px)';
    body.appendChild(glitchOverlay);
    
    // Remove after duration
    setTimeout(() => {
        body.removeChild(glitchOverlay);
    }, glitchDuration);
    
    // Set random timeout for next glitch
    setTimeout(addRandomPageGlitch, Math.random() * 20000 + 10000); // Between 10-30 seconds
}

// Start occasional glitch effect
setTimeout(addRandomPageGlitch, 5000); // First glitch after 5 seconds 