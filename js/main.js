/**
 * Anniversary Website - Main JavaScript
 * Features: Loading, Music, Timeline, Gallery, Counter, Easter Egg
 */

// ========================================
// Configuration
// ========================================
const CONFIG = {
    startDate: new Date('2020-12-31'),
    coupleNames: ['我们', '的'],
    musicVolume: 0.35,
    easterEggClicks: 0,
    easterEggTarget: 5,
    easterEggMessage: '我爱你，比昨天多一点，比明天少一点。'
};

// ========================================
// DOM Elements
// ========================================
const elements = {
    loadingScreen: document.getElementById('loading-screen'),
    loadingProgress: document.querySelector('.loading-progress'),
    loadingPercent: document.querySelector('.loading-percent'),
    progressBar: document.querySelector('.progress-bar'),
    progressFill: document.querySelector('.progress-fill'),
    mainContent: document.getElementById('main-content'),
    musicBtn: document.getElementById('music-btn'),
    bgm: document.getElementById('bgm'),
    daysCount: document.getElementById('days-count'),
    hoursCount: document.getElementById('hours-count'),
    minutesCount: document.getElementById('minutes-count'),
    secondsCount: document.getElementById('seconds-count'),
    timeline: document.querySelector('.timeline'),
    galleryGrid: document.getElementById('gallery-grid'),
    lightbox: document.getElementById('lightbox'),
    lightboxImage: document.querySelector('.lightbox-image'),
    lightboxCaption: document.querySelector('.lightbox-caption'),
    lightboxClose: document.querySelector('.lightbox-close'),
    easterEgg: document.getElementById('easter-egg'),
    surpriseModal: document.getElementById('surprise-modal'),
    surpriseText: document.querySelector('.surprise-text'),
    surpriseClose: document.querySelector('.surprise-close'),
    filterBtns: document.querySelectorAll('.filter-btn')
};

// ========================================
// Loading Screen
// ========================================
function initLoading() {
    let progress = 0;
    const loadingInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 100) progress = 100;
        
        elements.loadingProgress.style.width = `${progress}%`;
        elements.loadingPercent.textContent = `${Math.round(progress)}%`;
        
        if (progress >= 100) {
            clearInterval(loadingInterval);
            setTimeout(() => {
                elements.loadingScreen.classList.add('hidden');
            }, 500);
        }
    }, 200);
}

// ========================================
// Day Counter
// ========================================
function updateCounter() {
    const now = new Date();
    const diff = now - CONFIG.startDate;
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    
    elements.daysCount.textContent = days;
    elements.hoursCount.textContent = String(hours).padStart(2, '0');
    elements.minutesCount.textContent = String(minutes).padStart(2, '0');
    elements.secondsCount.textContent = String(seconds).padStart(2, '0');
}

// ========================================
// Progress Bar
// ========================================
function updateProgressBar() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    elements.progressFill.style.width = `${progress}%`;
}

// ========================================
// Music Control
// ========================================
function initMusic() {
    elements.bgm.volume = CONFIG.musicVolume;
    
    // Auto-play on first user interaction
    const enableAutoplay = () => {
        elements.bgm.play().then(() => {
            elements.musicBtn.classList.add('playing');
        }).catch(err => {
            console.log('Auto-play blocked by browser, waiting for user interaction');
        });
        document.removeEventListener('click', enableAutoplay);
        document.removeEventListener('touchstart', enableAutoplay);
    };
    document.addEventListener('click', enableAutoplay);
    document.addEventListener('touchstart', enableAutoplay);
    
    // Toggle play/pause on button click
    elements.musicBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (elements.bgm.paused) {
            elements.bgm.play();
            elements.musicBtn.classList.add('playing');
        } else {
            elements.bgm.pause();
            elements.musicBtn.classList.remove('playing');
        }
    });
    
    elements.bgm.addEventListener('error', () => {
        console.log('Background music file not found. Add bgm.mp3 to the media folder.');
        elements.musicBtn.style.display = 'none';
    });
}

// ========================================
// Timeline
// ========================================
async function initTimeline() {
    if (!elements.timeline) return;
    
    try {
        const response = await fetch('images/timeline_data.json');
        const events = await response.json();
        
        const fragment = document.createDocumentFragment();
        
        events.forEach((event, index) => {
            const item = document.createElement('div');
            item.className = 'timeline-item';
            item.dataset.index = index;
            
            const date = new Date(event.date);
            const formattedDate = `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
            
            let imagesHTML = '';
            if (event.images && event.images.length > 0) {
                imagesHTML = '<div class="timeline-images">';
                event.images.forEach(img => {
                    imagesHTML += `<img src="images/${img}" alt="${event.title}" loading="lazy" data-caption="${event.description}">`;
                });
                imagesHTML += '</div>';
            }
            
            item.innerHTML = `
                <div class="timeline-date">${formattedDate}</div>
                <div class="timeline-title">${event.title}</div>
                <div class="timeline-text">${event.description}</div>
                ${imagesHTML}
            `;
            
            // Add click handler for images
            item.querySelectorAll('.timeline-images img').forEach(img => {
                img.addEventListener('click', () => openLightbox(img.src, img.dataset.caption));
            });
            
            fragment.appendChild(item);
        });
        
        elements.timeline.appendChild(fragment);
        
        // Intersection Observer for animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, {
            threshold: 0.2,
            rootMargin: '0px 0px -50px 0px'
        });
        
        document.querySelectorAll('.timeline-item').forEach(item => {
            observer.observe(item);
        });
        
    } catch (error) {
        console.log('Error loading timeline data:', error);
    }
}

// ========================================
// Gallery
// ========================================
async function initGallery() {
    if (!elements.galleryGrid) return;
    
    try {
        const response = await fetch('images/gallery_data.json');
        const photos = await response.json();
        
        const fragment = document.createDocumentFragment();
        
        photos.forEach((photo, index) => {
            const item = document.createElement('div');
            item.className = 'gallery-item';
            item.dataset.category = photo.category || 'daily';
            item.dataset.src = photo.src;
            item.dataset.caption = photo.caption;
            
            item.innerHTML = `
                <img src="images/${photo.src}" alt="${photo.caption}" loading="lazy">
                <div class="gallery-item-overlay">
                    <span class="gallery-item-caption">${photo.caption}</span>
                </div>
            `;
            
            item.addEventListener('click', () => openLightbox(`images/${photo.src}`, photo.caption));
            fragment.appendChild(item);
        });
        
        elements.galleryGrid.appendChild(fragment);
        
        // Filter functionality
        elements.filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                elements.filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const filter = btn.dataset.filter;
                const items = document.querySelectorAll('.gallery-item');
                
                items.forEach(item => {
                    if (filter === 'all' || item.dataset.category === filter) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                // Re-initialize masonry
                if (window.masonryInstance) {
                    window.masonryInstance.destroy();
                }
                initMasonry();
            });
        });
        
        initMasonry();
        
    } catch (error) {
        console.log('Error loading gallery data:', error);
    }
}

function initMasonry() {
    if (typeof Masonry !== 'undefined' && elements.galleryGrid) {
        window.masonryInstance = new Masonry(elements.galleryGrid, {
            itemSelector: '.gallery-item',
            columnWidth: '.gallery-item',
            percentPosition: true,
            gutter: 16
        });
    }
}

// ========================================
// Lightbox
// ========================================
function openLightbox(src, caption = '') {
    elements.lightboxImage.src = src;
    elements.lightboxCaption.textContent = caption;
    elements.lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    elements.lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

function initLightbox() {
    elements.lightboxClose.addEventListener('click', closeLightbox);
    elements.lightbox.addEventListener('click', (e) => {
        if (e.target === elements.lightbox) {
            closeLightbox();
        }
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeLightbox();
            closeSurprise();
        }
    });
}

// ========================================
// Easter Egg
// ========================================
function initEasterEgg() {
    if (!elements.easterEgg) return;
    
    elements.easterEgg.addEventListener('click', () => {
        CONFIG.easterEggClicks++;
        
        if (CONFIG.easterEggClicks >= CONFIG.easterEggTarget) {
            showSurprise();
            CONFIG.easterEggClicks = 0;
        }
    });
}

function showSurprise() {
    elements.surpriseText.textContent = CONFIG.easterEggMessage;
    elements.surpriseModal.classList.add('active');
}

function closeSurprise() {
    elements.surpriseModal.classList.remove('active');
}

function initSurprise() {
    elements.surpriseClose.addEventListener('click', closeSurprise);
    elements.surpriseModal.addEventListener('click', (e) => {
        if (e.target === elements.surpriseModal) {
            closeSurprise();
        }
    });
}

// ========================================
// AOS Animation
// ========================================
function initAOS() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            delay: 100,
            once: true,
            offset: 50,
            disable: window.innerWidth < 768 ? true : false
        });
    }
}

// ========================================
// Smooth Scroll
// ========================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ========================================
// Image Error Handling
// ========================================
function initImageFallbacks() {
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            this.style.background = 'linear-gradient(135deg, #E8C4C4, #D4A5A5)';
            this.style.minHeight = '150px';
            this.alt = '图片加载中...';
        });
    });
}

// ========================================
// Initialize Everything
// ========================================
async function init() {
    initLoading();
    
    setTimeout(async () => {
        initAOS();
        initMusic();
        initLightbox();
        initEasterEgg();
        initSurprise();
        initSmoothScroll();
        initImageFallbacks();
        
        await initTimeline();
        await initGallery();
        
        updateCounter();
        setInterval(updateCounter, 1000);
        
        window.addEventListener('scroll', () => {
            updateProgressBar();
            if (typeof AOS !== 'undefined') {
                AOS.refresh();
            }
        });
        
        window.addEventListener('resize', () => {
            if (typeof AOS !== 'undefined') {
                AOS.refresh();
            }
        });
        
        console.log('🎉 纪念日网站已加载完成！');
        console.log(`📅 从 ${CONFIG.startDate.toLocaleDateString('zh-CN')} 开始`);
        console.log('💡 提示：请将你的背景音乐放入 media/bgm.mp3');
        
    }, 100);
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
