// Main.js - Markdown Blog

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileNavToggle) {
        mobileNavToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            this.setAttribute('aria-expanded', 
                this.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
            );
        });
    }
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        setTimeout(function() {
            messages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 300);
            });
        }, 5000);
    }
    
    // Handle image modal for post content images
    const postContent = document.querySelector('.markdown-content');
    if (postContent) {
        const images = postContent.querySelectorAll('img:not(.emoji)');
        
        images.forEach(image => {
            image.addEventListener('click', function() {
                const modal = document.createElement('div');
                modal.classList.add('image-modal');
                
                const modalContent = document.createElement('div');
                modalContent.classList.add('modal-content');
                
                const closeBtn = document.createElement('span');
                closeBtn.classList.add('close-modal');
                closeBtn.innerHTML = '&times;';
                closeBtn.addEventListener('click', function() {
                    document.body.removeChild(modal);
                    document.body.classList.remove('modal-open');
                });
                
                const modalImage = document.createElement('img');
                modalImage.src = this.src;
                modalImage.alt = this.alt || 'Image';
                
                modalContent.appendChild(closeBtn);
                modalContent.appendChild(modalImage);
                modal.appendChild(modalContent);
                
                document.body.appendChild(modal);
                document.body.classList.add('modal-open');
                
                modal.addEventListener('click', function(event) {
                    if (event.target === modal) {
                        document.body.removeChild(modal);
                        document.body.classList.remove('modal-open');
                    }
                });
            });
            
            // Add indicator that image is clickable
            image.classList.add('zoomable');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Table of contents generator for posts
    const generateTOC = () => {
        const toc = document.getElementById('table-of-contents');
        const content = document.querySelector('.markdown-content');
        
        if (toc && content) {
            const headings = content.querySelectorAll('h2, h3, h4');
            
            if (headings.length > 2) {
                const ul = document.createElement('ul');
                ul.className = 'toc-list';
                
                headings.forEach((heading, index) => {
                    // Add ID to heading if it doesn't have one
                    if (!heading.id) {
                        heading.id = `heading-${index}`;
                    }
                    
                    const li = document.createElement('li');
                    li.className = `toc-item toc-${heading.tagName.toLowerCase()}`;
                    
                    const a = document.createElement('a');
                    a.href = `#${heading.id}`;
                    a.textContent = heading.textContent;
                    
                    li.appendChild(a);
                    ul.appendChild(li);
                });
                
                toc.appendChild(ul);
                document.querySelector('.toc-container').style.display = 'block';
            } else {
                document.querySelector('.toc-container').style.display = 'none';
            }
        }
    };
    
    // Run TOC generator if we're on a post page
    if (document.querySelector('.post-detail') && document.getElementById('table-of-contents')) {
        generateTOC();
    }
    
    // Reading progress indicator
    const progressBar = document.querySelector('.reading-progress');
    if (progressBar) {
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progressBar.style.width = scrolled + '%';
        });
    }
    
    // Add 'active' class to current nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-links a').forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath || (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });
    
    // Lazy loading images with Intersection Observer
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    image.src = image.dataset.src;
                    image.classList.remove('lazy');
                    imageObserver.unobserve(image);
                }
            });
        });
        
        document.querySelectorAll('img.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for browsers that don't support Intersection Observer
        document.querySelectorAll('img.lazy').forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}); 