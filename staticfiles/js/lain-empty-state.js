/* Lain-themed empty state enhancer */

document.addEventListener('DOMContentLoaded', function() {
    // Find all the empty state containers from the screenshots
    const featuredArticlesSection = document.querySelector('[class*="Featured Article"]');
    const sonYazilarSection = document.querySelector('[class*="Son Yazılar"]');
    
    // Process featured articles section if it exists
    if (featuredArticlesSection) {
        const featuredContainer = featuredArticlesSection.closest('section') || featuredArticlesSection.parentElement;
        const emptyFeatured = featuredContainer.querySelector('[class*="No Featured Posts"]');
        
        if (emptyFeatured) {
            enhanceEmptyContainer(emptyFeatured, 'featured_posts');
        }
    }
    
    // Process son yazilar section if it exists
    if (sonYazilarSection) {
        const sonYazilarContainer = sonYazilarSection.closest('section') || sonYazilarSection.parentElement;
        const emptySonYazilar = sonYazilarContainer.querySelector('[class*="No Posts"]');
        
        if (emptySonYazilar) {
            enhanceEmptyContainer(emptySonYazilar, 'recent_posts');
        }
    }
    
    // Process no posts found section in search results
    const searchResultsContainer = document.querySelector('[class*="No Posts Found"]');
    if (searchResultsContainer) {
        enhanceEmptyContainer(searchResultsContainer, 'search_results');
    }
    
    // Special handling for the All Articles empty state
    const emptyStateInArticlesPage = document.querySelector('.empty-state');
    if (emptyStateInArticlesPage) {
        enhanceEmptyContainer(emptyStateInArticlesPage, 'all_articles');
    }
    
    // Function to enhance empty state containers
    function enhanceEmptyContainer(container, type) {
        // Skip if already enhanced
        if (container.classList.contains('lain-enhanced')) return;
        
        // Mark as enhanced
        container.classList.add('lain-enhanced');
        
        // Store original text and clear container
        const originalText = container.textContent.trim();
        container.innerHTML = '';
        
        // Create terminal-like container
        const terminal = document.createElement('div');
        terminal.className = 'lain-terminal';
        terminal.style.cssText = `
            background-color: rgba(0, 0, 0, 0.7);
            border: 1px solid #00b8d4;
            box-shadow: 0 0 15px rgba(0, 184, 212, 0.3);
            width: 100%;
            max-width: 100%;
            height: 100%;
            min-height: 200px;
            overflow: hidden;
            position: relative;
        `;
        
        // Terminal header
        const header = document.createElement('div');
        header.className = 'terminal-header';
        header.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: rgba(0, 0, 0, 0.8);
            padding: 8px 12px;
            border-bottom: 1px solid #00b8d4;
        `;
        
        // Header title based on type
        let headerTitle = 'connection-status';
        switch(type) {
            case 'featured_posts':
                headerTitle = 'wired:://featured-nodes';
                break;
            case 'recent_posts':
                headerTitle = 'wired:://recent-nodes';
                break;
            case 'search_results':
                headerTitle = 'wired:://search-results';
                break;
            case 'all_articles':
                headerTitle = 'wired:://all-articles';
                break;
        }
        
        const titleElement = document.createElement('span');
        titleElement.textContent = headerTitle;
        titleElement.style.cssText = `
            color: #00b8d4;
            font-family: monospace, "Courier New", Courier;
            font-size: 12px;
        `;
        
        // Terminal control buttons
        const controls = document.createElement('div');
        controls.style.cssText = `
            display: flex;
            gap: 5px;
        `;
        
        ['#444', '#444', '#444'].forEach(color => {
            const button = document.createElement('span');
            button.style.cssText = `
                width: 10px;
                height: 10px;
                background-color: ${color};
                border-radius: 50%;
                display: inline-block;
            `;
            controls.appendChild(button);
        });
        
        // Add elements to header
        header.appendChild(titleElement);
        header.appendChild(controls);
        
        // Terminal content
        const content = document.createElement('div');
        content.className = 'terminal-content';
        content.style.cssText = `
            padding: 15px;
            font-family: monospace, "Courier New", Courier;
            color: #f0f0f0;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        `;
        
        // Create warning icon for all articles page
        if (type === 'all_articles') {
            const warningIcon = document.createElement('div');
            warningIcon.style.cssText = `
                text-align: center;
                margin-bottom: 20px;
                color: #00b8d4;
                font-size: 32px;
            `;
            warningIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
            content.appendChild(warningIcon);
        }
        
        // Create lines based on type
        const lines = [];
        
        // Different terminal output based on type
        switch(type) {
            case 'featured_posts':
                lines.push({
                    prompt: true,
                    text: 'access --featured-nodes'
                });
                lines.push({
                    prompt: false,
                    error: true,
                    text: 'Connection to featured layer blocked'
                });
                lines.push({
                    prompt: false,
                    text: `${originalText}`
                });
                lines.push({
                    prompt: false,
                    text: 'Waiting for new connections...'
                });
                lines.push({
                    prompt: true,
                    cursor: true
                });
                break;
                
            case 'recent_posts':
                lines.push({
                    prompt: true,
                    text: 'ls -la ~/posts/recent/'
                });
                lines.push({
                    prompt: false,
                    error: true,
                    text: 'Directory empty: No recent nodes found'
                });
                lines.push({
                    prompt: false,
                    text: `${originalText}`
                });
                lines.push({
                    prompt: false,
                    text: 'System will auto-refresh when posts are available'
                });
                lines.push({
                    prompt: true,
                    cursor: true
                });
                break;
                
            case 'search_results':
                lines.push({
                    prompt: true,
                    text: 'grep -r "query" --include="*.post" /var/www/node/'
                });
                lines.push({
                    prompt: false,
                    error: true,
                    text: 'No matches found in the current layer'
                });
                lines.push({
                    prompt: false,
                    text: `${originalText}`
                });
                lines.push({
                    prompt: true,
                    text: 'ping -c 3 deeper.layer'
                });
                lines.push({
                    prompt: false,
                    text: 'Request timed out'
                });
                lines.push({
                    prompt: true,
                    cursor: true
                });
                break;
                
            case 'all_articles':
                lines.push({
                    prompt: true,
                    text: 'fetch data --from-layer 7'
                });
                lines.push({
                    prompt: false,
                    error: true,
                    text: 'Error: data unreachable • connection timeout'
                });
                lines.push({
                    prompt: false, 
                    error: true,
                    text: 'Protocol error • | ' + `${originalText}`
                });
                lines.push({
                    prompt: true,
                    text: 'retry --connection'
                });
                lines.push({
                    prompt: true,
                    cursor: true
                });
                break;
        }
        
        // Add all lines to content
        lines.forEach(line => {
            const lineElement = document.createElement('div');
            lineElement.className = 'terminal-line';
            lineElement.style.cssText = `
                margin-bottom: 8px;
                line-height: 1.3;
                font-size: 13px;
            `;
            
            // Add prompt if needed
            if (line.prompt) {
                const promptElement = document.createElement('span');
                promptElement.textContent = '$ ';
                promptElement.style.cssText = `
                    color: #33ff33;
                    margin-right: 8px;
                `;
                lineElement.appendChild(promptElement);
                
                // Add text content if any
                if (line.text) {
                    const textElement = document.createElement('span');
                    textElement.textContent = line.text;
                    textElement.style.color = '#f0f0f0';
                    lineElement.appendChild(textElement);
                }
                
                // Add cursor if specified
                if (line.cursor) {
                    const cursorElement = document.createElement('span');
                    cursorElement.innerHTML = '|';
                    cursorElement.style.cssText = `
                        animation: blink 1s infinite;
                    `;
                    lineElement.appendChild(cursorElement);
                }
            } else {
                // Regular text or error
                const textElement = document.createElement('span');
                textElement.textContent = line.text;
                textElement.style.cssText = `
                    color: ${line.error ? '#ff00a5' : '#aaaaaa'};
                    padding-left: ${line.error ? '0' : '16px'};
                `;
                lineElement.appendChild(textElement);
            }
            
            content.appendChild(lineElement);
        });
        
        // Add scanlines effect
        const scanlines = document.createElement('div');
        scanlines.className = 'scanlines';
        scanlines.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(to bottom, rgba(0,0,0,0) 50%, rgba(0,0,0,0.02) 50%);
            background-size: 100% 4px;
            pointer-events: none;
            opacity: 0.15;
            z-index: 1;
        `;
        
        // Add glitch effect that occurs randomly
        const glitchEffect = document.createElement('div');
        glitchEffect.className = 'terminal-glitch';
        glitchEffect.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 184, 212, 0.05);
            pointer-events: none;
            z-index: 2;
            opacity: 0;
        `;
        
        // Add all elements to terminal
        terminal.appendChild(header);
        terminal.appendChild(content);
        terminal.appendChild(scanlines);
        terminal.appendChild(glitchEffect);
        
        // Add terminal to container
        container.appendChild(terminal);
        
        // Add random glitch animation
        setInterval(() => {
            if (Math.random() > 0.85) {
                glitchEffect.style.opacity = '0.2';
                setTimeout(() => {
                    glitchEffect.style.opacity = '0';
                }, 150);
                
                // Also add a slight position shift
                terminal.style.transform = `translateX(${(Math.random() - 0.5) * 3}px)`;
                setTimeout(() => {
                    terminal.style.transform = 'translateX(0)';
                }, 100);
            }
        }, 3000);
    }

    // Add keyframe animation for cursor blink if not already defined
    if (!document.querySelector('#lain-keyframes')) {
        const keyframes = document.createElement('style');
        keyframes.id = 'lain-keyframes';
        keyframes.innerHTML = `
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
        `;
        document.head.appendChild(keyframes);
    }
}); 