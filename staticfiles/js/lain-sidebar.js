/* Lain-themed sidebar enhancer for search, categories, and filters */

document.addEventListener('DOMContentLoaded', function() {
    // Enhance the search container
    const searchContainer = document.querySelector('.search-container');
    if (searchContainer) {
        enhanceSearchInput(searchContainer);
    }
    
    // Enhance category and filter sections
    const filterSections = document.querySelectorAll('.filter-group');
    filterSections.forEach(section => {
        enhanceFilterSection(section);
    });
    
    // Enhance all links in the sidebar
    const links = document.querySelectorAll('.filter-list a, .tags-cloud a');
    links.forEach(link => {
        enhanceLinkWithTerminalEffect(link);
    });
    
    // Function to enhance search input with terminal style
    function enhanceSearchInput(container) {
        const searchInput = container.querySelector('input[type="text"]');
        if (!searchInput) return;
        
        // Mark as enhanced
        searchInput.classList.add('lain-enhanced');
        
        // Change the placeholder to terminal style
        searchInput.placeholder = 'grep -r "search_term" /wired';
        
        // Add focus effect
        searchInput.addEventListener('focus', function() {
            this.placeholder = '> search query...';
            
            // Create a glitch effect on focus
            const glitchOverlay = document.createElement('div');
            glitchOverlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 184, 212, 0.03);
                z-index: 9999;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.2s;
            `;
            document.body.appendChild(glitchOverlay);
            
            // Show the glitch
            setTimeout(() => {
                glitchOverlay.style.opacity = '1';
                setTimeout(() => {
                    glitchOverlay.style.opacity = '0';
                    setTimeout(() => {
                        glitchOverlay.remove();
                    }, 200);
                }, 100);
            }, 10);
        });
        
        searchInput.addEventListener('blur', function() {
            this.placeholder = 'grep -r "search_term" /wired';
        });
        
        // Add style to the search button
        const searchButton = container.querySelector('button');
        if (searchButton) {
            searchButton.title = "Execute search query";
            searchButton.addEventListener('mouseenter', function() {
                this.innerHTML = '<i class="fas fa-terminal"></i>';
            });
            
            searchButton.addEventListener('mouseleave', function() {
                this.innerHTML = '<i class="fas fa-search"></i>';
            });
        }
    }
    
    // Function to enhance filter sections
    function enhanceFilterSection(section) {
        const heading = section.querySelector('h3');
        if (!heading) return;
        
        // Skip if already enhanced
        if (heading.classList.contains('lain-enhanced')) return;
        heading.classList.add('lain-enhanced');
        
        // Add terminal style to headings
        const headingText = heading.textContent.trim();
        heading.innerHTML = '';
        
        // Create a prefix span
        const prefix = document.createElement('span');
        prefix.textContent = '> ';
        prefix.style.cssText = `
            color: #33ff33;
            margin-right: 2px;
            font-family: monospace;
        `;
        
        // Create the text span
        const text = document.createElement('span');
        text.textContent = headingText.toLowerCase();
        text.style.cssText = `
            color: #00b8d4;
            font-family: monospace;
            position: relative;
        `;
        
        heading.appendChild(prefix);
        heading.appendChild(text);
        
        // Add a blink effect occasionally
        setInterval(() => {
            if (Math.random() > 0.97) {
                text.style.opacity = '0.5';
                setTimeout(() => {
                    text.style.opacity = '1';
                }, 100);
            }
        }, 4000);
        
        // Add a terminal style to links
        const links = section.querySelectorAll('a');
        links.forEach(link => {
            enhanceLinkWithTerminalEffect(link);
        });
    }
    
    // Function to enhance links with terminal effect
    function enhanceLinkWithTerminalEffect(link) {
        // Skip if already enhanced
        if (link.classList.contains('lain-enhanced')) return;
        link.classList.add('lain-enhanced');
        
        // Save original text
        const originalText = link.textContent;
        
        // Add hover effect
        link.addEventListener('mouseenter', function() {
            // Add cyan text color and flashing effect
            this.style.color = '#00b8d4';
            this.style.textShadow = '0 0 5px rgba(0, 184, 212, 0.5)';
            
            // Add > prefix if not already present
            if (!this.querySelector('.prefix')) {
                const prefix = document.createElement('span');
                prefix.className = 'prefix';
                prefix.textContent = '> ';
                prefix.style.cssText = `
                    color: #33ff33;
                    font-family: monospace;
                    opacity: 0;
                    transition: opacity 0.2s;
                `;
                this.prepend(prefix);
                
                // Fade in the prefix
                setTimeout(() => {
                    prefix.style.opacity = '1';
                }, 10);
            }
            
            // Add occasional glitch effect to cursor
            const randomGlitch = Math.random() > 0.7;
            if (randomGlitch) {
                this.style.transform = `translateX(${(Math.random() - 0.5) * 3}px)`;
                setTimeout(() => {
                    this.style.transform = 'translateX(0)';
                }, 100);
            }
        });
        
        link.addEventListener('mouseleave', function() {
            // Reset style
            this.style.color = '';
            this.style.textShadow = '';
            
            // Remove prefix with fade out
            const prefix = this.querySelector('.prefix');
            if (prefix) {
                prefix.style.opacity = '0';
                setTimeout(() => {
                    prefix.remove();
                }, 200);
            }
        });
    }
    
    // Add special styling for active links
    const activeLinks = document.querySelectorAll('.filter-list a.active, .tags-cloud a.active');
    activeLinks.forEach(link => {
        // Add permanent prefix for active links
        if (!link.querySelector('.active-prefix')) {
            const prefix = document.createElement('span');
            prefix.className = 'active-prefix';
            prefix.textContent = '> ';
            prefix.style.cssText = `
                color: #33ff33;
                font-family: monospace;
            `;
            link.prepend(prefix);
            
            // Add a blinking effect to the active link
            link.style.color = '#00b8d4';
            
            // Add a subtle animation
            setInterval(() => {
                if (Math.random() > 0.9) {
                    link.style.textShadow = '0 0 8px rgba(0, 184, 212, 0.8)';
                    setTimeout(() => {
                        link.style.textShadow = '0 0 5px rgba(0, 184, 212, 0.5)';
                    }, 100);
                }
            }, 3000);
        }
    });
    
    // Special treatment for tags
    const tagLinks = document.querySelectorAll('.tags-cloud a');
    tagLinks.forEach(tag => {
        // Add a terminal-style look to tags
        tag.style.fontFamily = "'Share Tech Mono', monospace";
        
        // Add a small glitch effect on hover
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'glitch';
            this.style.textShadow = '0 0 5px rgba(0, 184, 212, 0.7), -1px 0 red, 1px 0 blue';
            
            setTimeout(() => {
                this.style.textShadow = '0 0 5px rgba(0, 184, 212, 0.5)';
            }, 100);
        });
    });
    
    // Add Lain-style to the "All Categories" link
    const allCategoriesLink = document.querySelector('.filter-list li:first-child a');
    if (allCategoriesLink) {
        allCategoriesLink.className += ' all-categories-link';
        if (allCategoriesLink.classList.contains('active')) {
            allCategoriesLink.classList.add('category-active');
        }
    }
}); 