// Create floating gradient elements
function createFloatingGradients() {
    const count = 8;
    for (let i = 0; i < count; i++) {
        const gradient = document.createElement('div');
        gradient.className = 'floating-gradient';
        gradient.style.left = `${Math.random() * 100}%`;
        gradient.style.width = `${100 + Math.random() * 200}px`;
        gradient.style.height = gradient.style.width;
        gradient.style.animationDuration = `${10 + Math.random() * 20}s`;
        gradient.style.animationDelay = `${Math.random() * 5}s`;
        document.body.appendChild(gradient);
    }
}
function openZoom(src) {
    document.getElementById('zoomedImage').src = src;
    document.getElementById('zoomModal').classList.remove('hidden');
    }

function closeZoom() {
    document.getElementById('zoomModal').classList.add('hidden');
    document.getElementById('zoomModal').onclick = closeZoom;
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', createFloatingGradients);

function toggleSection(element) {
    const isExpanding = !element.classList.contains('expanded');
    const overlay = document.querySelector('.overlay');
    
    if (isExpanding) {
        // Start zoom animation
        element.classList.add('zooming');
        overlay.classList.add('active');
        
        // After a short delay, expand the section
        setTimeout(() => {
            element.classList.remove('zooming');
            element.classList.add('expanded');
            
            // Close all other expanded sections
            document.querySelectorAll('.section-box.expanded').forEach(box => {
                if (box !== element) {
                    box.classList.remove('expanded');
                }
            });
            
            document.body.style.overflow = 'hidden';
        }, 200);
    } else {
        // Start closing animation
        element.classList.add('zooming');
        overlay.classList.remove('active');
        
        // After animation completes, remove expanded state
        setTimeout(() => {
            element.classList.remove('zooming');
            element.classList.remove('expanded');
            document.body.style.overflow = '';
            
            // Toggle chevron icon
            const icon = element.querySelector('.fa-chevron-down, .fa-chevron-up');
            if (icon) {
                icon.classList.toggle('fa-chevron-down');
                icon.classList.toggle('fa-chevron-up');
            }
        }, 200);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // About Section
    const aboutSection = document.getElementById('about-section');
    const aboutCloseBtn = document.getElementById('about-close-btn');
    aboutSection.addEventListener('click', function(e) {
        if (!aboutSection.classList.contains('expanded')) {
            toggleSection(aboutSection);
        }
    });
    aboutCloseBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (aboutSection.classList.contains('expanded')) {
            toggleSection(aboutSection);
        }
    });

    // Projects Section
    const projectsSection = document.getElementById('projects-section');
    const projectsCloseBtn = document.getElementById('projects-close-btn');
    projectsSection.addEventListener('click', function(e) {
        if (!projectsSection.classList.contains('expanded')) {
            toggleSection(projectsSection);
        }
    });
    projectsCloseBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (projectsSection.classList.contains('expanded')) {
            toggleSection(projectsSection);
        }
    });

    // Contact Section
    const contactSection = document.getElementById('contact-section');
    const contactCloseBtn = document.getElementById('contact-close-btn');
    contactSection.addEventListener('click', function(e) {
        if (!contactSection.classList.contains('expanded')) {
            toggleSection(contactSection);
        }
    });
    contactCloseBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (contactSection.classList.contains('expanded')) {
            toggleSection(contactSection);
        }
    });

    // Virtual Avatar Section
    const avatarSection = document.getElementById('avatar-section');
    const avatarCloseBtn = document.getElementById('avatar-close-btn');
    avatarSection.addEventListener('click', function(e) {
        if (!avatarSection.classList.contains('expanded')) {
            toggleSection(avatarSection);
        }
    });
    avatarCloseBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (avatarSection.classList.contains('expanded')) {
            toggleSection(avatarSection);
        }
    });
    document.querySelectorAll('img.zoomable').forEach(img => {
        img.addEventListener('click', function() {
            const dialog = document.getElementById('zoomDialog');
            const dialogImg = document.getElementById('zoomDialogImg');
            dialogImg.src = this.src;
            dialog.showModal();
        });
    });
    document.getElementById('zoomDialog').addEventListener('click', function() {
        this.close();
    });
});

fetch('/latest-tweet')
    .then(res => res.json())
    .then(tweet => {
        const tweetDiv = document.getElementById('latest-tweet');
        let tweets = JSON.parse(localStorage.getItem('tweets') || '[]');
        if (tweet && tweet.text) {
            // Add new tweet to the top if it's not already present
            if (!tweets.find(t => t.text === tweet.text)) {
                tweets.unshift({ text: tweet.text });
                // Keep only the latest 10 tweets (optional)
                tweets = tweets.slice(0, 10);
                localStorage.setItem('tweets', JSON.stringify(tweets));
            }
            tweetDiv.innerHTML =
                `<span class="block mb-1"><i class="fab fa-twitter text-blue-400"></i> Latest Tweets:</span>
                 <ul class="space-y-2">
                    ${tweets.map(t => `<li class="border-b border-gray-700 pb-2">${t.text}</li>`).join('')}
                 </ul>`;
        } else {
            tweetDiv.textContent = tweet.error || 'No tweet found.';
        }
    })
    .catch((err) => {
        document.getElementById('latest-tweet').textContent = 'Could not load tweet.';
        console.error(err);
    });

fetch('/latest-spotify-embed')
  .then(res => res.json())
  .then(data => {
    const embedHtml = data.embed_html.replace(
      '<iframe ',
      '<iframe style="border-radius:16px; box-shadow:0 2px 8px #0003; width:100%; height:80px;" '
    );
    document.getElementById('spotify-song').innerHTML = embedHtml;
  });



const chatbox = document.getElementById('chatbox');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');
const chatClear = document.getElementById('chat-clear');

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = sender === 'user' ? 'text-right mb-2' : 'text-left mb-2';
    msgDiv.innerHTML = `<span class="inline-block px-3 py-2 rounded-lg ${sender === 'user' ? 'bg-purple-600 text-white' : 'bg-gray-700 text-purple-200'}">${text}</span>`;
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

chatSend.addEventListener('click', () => {
    const message = chatInput.value.trim();
    if (!message) return;
    appendMessage('user', message);
    chatInput.value = '';
    fetch('/virtual-avatar-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage('ai', data.reply);
    })
    .catch(() => {
        appendMessage('ai', "Sorry, I couldn't process your request.");
    });
});

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') chatSend.click();
});
chatClear.addEventListener('click', () => {
    document.getElementById('chatbox').innerHTML = '';
});

document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = this.querySelector('input[type="text"]').value.trim();
    const email = this.querySelector('input[type="email"]').value.trim();
    const message = this.querySelector('textarea').value.trim();

    fetch('/send-contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, message })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert('Message sent! Thank you.');
            this.reset();
        } else {
            alert('Error: ' + (data.error || 'Could not send message.'));
        }
    })
    .catch(() => alert('Could not send message. Please try again later.'));
});