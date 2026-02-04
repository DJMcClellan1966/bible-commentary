/**
 * Deep Bible Study - Client-side JavaScript
 * Handles UI interactions, API calls, and state management
 */

// API Base URL
const API_BASE = window.location.origin;

// State
let currentView = 'today';
let dailyReading = null;
let twinStats = null;

// DOM Elements
const views = {
    today: document.getElementById('today-view'),
    explore: document.getElementById('explore-view'),
    twin: document.getElementById('twin-view'),
    progress: document.getElementById('progress-view')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initNavigation();
    initEventListeners();
    loadTodaysReading();
    loadTwinStats();
});

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Navigation
function initNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const view = link.getAttribute('data-view');
            switchView(view);
        });
    });
}

function switchView(viewName) {
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.getAttribute('data-view') === viewName);
    });
    
    // Update views
    Object.entries(views).forEach(([name, element]) => {
        element.classList.toggle('active', name === viewName);
    });
    
    currentView = viewName;
    
    // Load view-specific data
    if (viewName === 'twin') {
        loadTwinStats();
    } else if (viewName === 'progress') {
        loadProgress();
    }
}

// Event Listeners
function initEventListeners() {
    // Ask button
    document.getElementById('askButton').addEventListener('click', handleAskQuestion);
    
    // Enter key in question input
    document.getElementById('questionInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            handleAskQuestion();
        }
    });
    
    // Explore search
    document.getElementById('searchButton').addEventListener('click', handleExploreSearch);
    document.getElementById('themeAskButton').addEventListener('click', handleThemeQuestion);
    document.getElementById('verseSearch').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            handleExploreSearch();
        }
    });
    document.getElementById('themeQuestionInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            handleThemeQuestion();
        }
    });
}

// Load Today's Reading (use client's local date so timezone doesn't show wrong day)
async function loadTodaysReading() {
    try {
        const today = new Date();
        const dateParam = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
        const response = await fetch(`${API_BASE}/api/daily-reading/today?client_date=${encodeURIComponent(dateParam)}`);
        if (response.ok) {
            dailyReading = await response.json();
            renderDailyReading(dailyReading);
        } else {
            // Use fallback data for demo
            renderDailyReadingFallback();
        }
    } catch (error) {
        console.log('Using fallback reading data');
        renderDailyReadingFallback();
    }
}

function renderDailyReading(reading) {
    // Basic info
    document.getElementById('dayNumber').textContent = reading.day_number || 1;
    document.getElementById('currentDate').textContent = formatDate(reading.date);
    document.getElementById('monthlyTheme').textContent = reading.monthly_theme?.name || 'Beginnings';
    
    // Progress
    const progress = reading.progress_percentage || 0;
    document.getElementById('progressFill').style.width = `${progress}%`;
    document.getElementById('progressPercent').textContent = Math.round(progress);
    
    // Passage
    document.getElementById('passageRef').textContent = reading.passages?.join(', ') || 'Genesis 1:1-2:3';
    document.getElementById('passageTitle').textContent = reading.title || 'In the Beginning';
    document.getElementById('salvationContext').textContent = reading.salvation_history_context || '';
    document.getElementById('passageText').innerHTML = formatPassageText(reading.passage_text);
    document.getElementById('keyVerse').textContent = reading.key_verse || '';
    
    // The Fathers' explanation (single narrative: themes, interconnections, Christ, reflection)
    const patristicEl = document.getElementById('patristicSummary');
    const patristicSection = document.getElementById('patristicSummarySection');
    if (reading.patristic_summary && patristicEl && patristicSection) {
        patristicEl.textContent = reading.patristic_summary;
        patristicSection.classList.remove('hidden');
    } else if (patristicSection) {
        patristicSection.classList.add('hidden');
    }

    // Church Fathers quotes
    renderChurchFathers(reading.church_fathers);
}

function renderDailyReadingFallback() {
    // Fallback data for demo/offline mode
    const fallback = {
        day_number: getDayOfYear(),
        date: new Date().toISOString(),
        passages: ['Genesis 1:1-2:3'],
        title: 'In the Beginning',
        passage_text: 'In the beginning God created the heaven and the earth. And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters. And God said, Let there be light: and there was light.',
        salvation_history_context: 'Creation establishes God as the sovereign Creator and humanity as His image-bearers.',
        key_verse: 'Genesis 1:1 - In the beginning God created the heaven and the earth.',
        connection_to_christ: 'John 1:1-3 reveals Christ was present at creation - "All things were made through him."',
        patristic_summary: 'This portion of Holy Scripture—In the Beginning—finds its place in the divine economy as creation establishes God as the sovereign Creator and humanity as His image-bearers. Here the great themes of Covenant, Creation are woven together. It points forward to John 1:1-3: John echoes Genesis, revealing Christ as the creative Word. As Creation finds its fulfillment in New Creation, so as God created the world, He creates us anew in Christ (2 Cor 5:17). Above all, this word touches the life and ministry of our Lord: John 1:1-3 reveals Christ was present at creation—"All things were made through him." Let us therefore receive this word as the Fathers did—as one that shapes both belief and life, and that draws us into the same story of redemption.',
        progress_percentage: (getDayOfYear() / 365) * 100,
        monthly_theme: { name: getMonthTheme() },
        backward_links: [],
        forward_links: [
            { reference: 'John 1:1-3', text: 'In the beginning was the Word...', explanation: 'John echoes Genesis, revealing Christ as the creative Word.' }
        ],
        typological: [
            { type_name: 'Creation', antitype_name: 'New Creation', connection_explanation: 'As God created the world, so He creates us anew in Christ (2 Cor 5:17).' }
        ],
        church_fathers: [
            { author: 'Augustine', quote: 'In the beginning God made heaven and earth. How, O God, didst Thou make heaven and earth?', work: 'Confessions' }
        ],
        reflection_questions: [
            'What is God creating or recreating in your life right now?',
            'How does knowing God is the Creator give you confidence?',
            'How does this passage point to Christ?'
        ]
    };
    
    renderDailyReading(fallback);
}

function renderConnections(containerId, connections, label) {
    const container = document.getElementById(containerId);
    const listEl = container.querySelector('.connection-list');
    
    if (!connections || connections.length === 0) {
        container.classList.add('hidden');
        return;
    }
    
    container.classList.remove('hidden');
    listEl.innerHTML = connections.map(conn => `
        <div class="connection-item">
            <div class="connection-ref">${conn.reference}</div>
            ${conn.text ? `<div class="connection-text">"${truncate(conn.text, 120)}"</div>` : ''}
            <div class="connection-explanation">${conn.explanation}</div>
            ${conn.church_fathers && conn.church_fathers.length ? `<div class="connection-fathers">Church Fathers: ${conn.church_fathers.map(f => `${f.author}${f.work ? `, <em>${f.work}</em>` : ''}`).join('; ')}</div>` : ''}
        </div>
    `).join('');
}

function renderTypology(typological) {
    const section = document.getElementById('typologySection');
    const listEl = section.querySelector('.typology-list');
    
    if (!typological || typological.length === 0) {
        section.classList.add('hidden');
        return;
    }
    
    section.classList.remove('hidden');
    listEl.innerHTML = typological.map(typ => `
        <div class="typology-item">
            <div class="typology-pair">
                <div class="typology-type">${typ.type_name}</div>
                <span class="typology-arrow">→</span>
                <div class="typology-antitype">${typ.antitype_name}</div>
            </div>
            <p>${truncate(typ.connection_explanation, 150)}</p>
        </div>
    `).join('');
}

function renderChurchFathers(fathers) {
    const section = document.getElementById('churchFathersSection');
    const listEl = document.getElementById('fathersList');
    
    if (!fathers || fathers.length === 0) {
        section.classList.add('hidden');
        return;
    }
    
    section.classList.remove('hidden');
    listEl.innerHTML = fathers.map(f => `
        <div class="father-quote">
            <blockquote>"${f.quote}"</blockquote>
            <div class="father-attribution">— ${f.author}${f.work ? `, ${f.work}` : ''}</div>
        </div>
    `).join('');
}

function renderReflectionQuestions(questions) {
    const container = document.getElementById('reflectionQuestions');
    
    if (!questions || questions.length === 0) {
        container.innerHTML = '<p class="placeholder-text">Reflect on what you\'ve read.</p>';
        return;
    }
    
    container.innerHTML = questions.map((q, i) => `
        <div class="reflection-question">
            <span class="question-number">${i + 1}.</span>
            <span>${q}</span>
        </div>
    `).join('');
}

// Ask Question
async function handleAskQuestion() {
    const input = document.getElementById('questionInput');
    const question = input.value.trim();
    
    if (!question) return;
    
    const responseDiv = document.getElementById('twinResponse');
    responseDiv.classList.remove('hidden');
    responseDiv.innerHTML = '<p class="thinking">Searching Scripture and Church Fathers...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/api/twin/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        
        if (response.ok) {
            const result = await response.json();
            responseDiv.innerHTML = formatTwinAnswer(result);
        } else {
            throw new Error('API error');
        }
    } catch (error) {
        // Fallback response
        responseDiv.innerHTML = `
            <div class="twin-answer">
                <p><strong>AI Twin:</strong> That's a thoughtful question. I notice you're exploring this topic - 
                it seems to be drawing your attention. Let me help you dig deeper into Scripture to find understanding.</p>
            </div>
        `;
    }
    
    input.value = '';
}

function formatTwinAnswer(result) {
    let html = '<div class="twin-answer">';
    
    // Main answer
    if (result.answer) {
        html += `<div class="answer-text">${result.answer.replace(/\n/g, '<br>')}</div>`;
    } else if (result.personal_response) {
        html += `<div class="answer-text">${result.personal_response.replace(/\n/g, '<br>')}</div>`;
    }
    
    // Key verses
    if (result.key_verses && result.key_verses.length > 0) {
        html += '<div class="answer-verses"><h4>Key Scriptures</h4><ul>';
        for (const verse of result.key_verses.slice(0, 4)) {
            html += `<li><strong>${verse.reference}</strong>`;
            if (verse.text) {
                html += `<br><em>"${truncate(verse.text, 150)}"</em>`;
            }
            html += '</li>';
        }
        html += '</ul></div>';
    }
    
    // Church Fathers
    if (result.church_fathers && result.church_fathers.length > 0) {
        html += '<div class="answer-fathers"><h4>Church Fathers</h4>';
        for (const father of result.church_fathers.slice(0, 2)) {
            html += `<blockquote>"${truncate(father.quote, 200)}"<br>— ${father.author}${father.work ? `, <em>${father.work}</em>` : ''}</blockquote>`;
        }
        html += '</div>';
    }
    
    // Typology
    if (result.typology) {
        html += `<div class="answer-typology">
            <h4>Typological Connection</h4>
            <p><strong>${result.typology.type}</strong> → <strong>${result.typology.antitype}</strong></p>
            <p>${truncate(result.typology.connection, 150)}</p>
        </div>`;
    }
    
    // Related interests
    if (result.related_interests && result.related_interests.length > 0) {
        html += `<p class="related-note"><em>This connects to your interests in: ${result.related_interests.map(i => i.topic).join(', ')}</em></p>`;
    }
    
    html += '</div>';
    return html;
}

// Explore
async function handleExploreSearch() {
    const input = document.getElementById('verseSearch');
    const verse = input.value.trim();
    
    if (!verse) return;
    
    const resultsDiv = document.getElementById('exploreResults');
    resultsDiv.innerHTML = '<p>Searching...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/api/interconnections/${encodeURIComponent(verse)}`);
        
        if (response.ok) {
            const result = await response.json();
            renderExploreResults(result);
        } else {
            throw new Error('Not found');
        }
    } catch (error) {
        resultsDiv.innerHTML = `
            <p>Searching for: <strong>${verse}</strong></p>
            <p class="placeholder-text">Deep interconnections for this verse are being prepared. 
            Try John 3:16, Genesis 3:15, or Romans 8:28.</p>
        `;
    }
}

function renderExploreResults(data) {
    const resultsDiv = document.getElementById('exploreResults');
    
    resultsDiv.innerHTML = `
        <h3>${data.reference}</h3>
        <p class="passage-text">${data.text || ''}</p>
        
        ${data.themes?.length > 0 ? `
            <div class="themes">
                <strong>Themes:</strong> ${data.themes.join(', ')}
            </div>
        ` : ''}
        
        ${data.backward_links?.length > 0 ? `
            <div class="connection-group">
                <h4>← Looking Back</h4>
                ${data.backward_links.map(link => `
                    <div class="connection-item">
                        <div class="connection-ref">${link.reference}</div>
                        ${link.text ? `<div class="connection-text">"${truncate(link.text, 120)}"</div>` : ''}
                        <div class="connection-explanation">${link.explanation}</div>
                        ${link.church_fathers && link.church_fathers.length ? `<div class="connection-fathers">Church Fathers: ${link.church_fathers.map(f => `${f.author}${f.work ? `, <em>${f.work}</em>` : ''}`).join('; ')}</div>` : ''}
                    </div>
                `).join('')}
            </div>
        ` : ''}
        
        ${data.forward_links?.length > 0 ? `
            <div class="connection-group">
                <h4>→ Looking Forward</h4>
                ${data.forward_links.map(link => `
                    <div class="connection-item">
                        <div class="connection-ref">${link.reference}</div>
                        ${link.text ? `<div class="connection-text">"${truncate(link.text, 120)}"</div>` : ''}
                        <div class="connection-explanation">${link.explanation}</div>
                        ${link.church_fathers && link.church_fathers.length ? `<div class="connection-fathers">Church Fathers: ${link.church_fathers.map(f => `${f.author}${f.work ? `, <em>${f.work}</em>` : ''}`).join('; ')}</div>` : ''}
                    </div>
                `).join('')}
            </div>
        ` : ''}
        
        ${data.church_fathers?.length > 0 ? `
            <div class="fathers-section">
                <h4>Church Fathers</h4>
                ${data.church_fathers.map(f => `
                    <div class="father-quote">
                        <blockquote>"${f.quote}"</blockquote>
                        <div class="father-attribution">— ${f.author}</div>
                    </div>
                `).join('')}
            </div>
        ` : ''}
    `;
}

// Theme & Symbolism (Explore)
async function handleThemeQuestion() {
    const input = document.getElementById('themeQuestionInput');
    const question = input?.value?.trim();
    if (!question) return;

    const answerDiv = document.getElementById('themeAnswer');
    const bodyEl = document.getElementById('themeAnswerBody');
    const versesEl = document.getElementById('themeAnswerVerses');
    const fathersEl = document.getElementById('themeAnswerFathers');
    const errEl = document.getElementById('themeAnswerError');

    answerDiv?.classList.add('hidden');
    errEl?.classList.add('hidden');
    bodyEl.textContent = 'Searching...';
    versesEl.innerHTML = '';
    fathersEl.innerHTML = '';

    try {
        const response = await fetch(`${API_BASE}/api/explore/theme`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        const data = await response.json();

        if (!response.ok) throw new Error(data.detail || 'Request failed');

        bodyEl.textContent = data.answer || '';
        if (data.key_verses?.length) {
            versesEl.innerHTML = '<h4>Key verses</h4>' + data.key_verses.map(v =>
                `<div class="theme-verse"><strong>${v.reference}</strong> ${v.text ? `— ${truncate(v.text, 120)}` : ''}</div>`
            ).join('');
        }
        if (data.church_fathers?.length) {
            fathersEl.innerHTML = '<h4>Church Fathers</h4>' + data.church_fathers.map(f =>
                `<blockquote class="theme-father-quote">"${truncate(f.quote, 180)}"<br><cite>— ${f.author}${f.work ? `, ${f.work}` : ''}</cite></blockquote>`
            ).join('');
        }
        answerDiv?.classList.remove('hidden');
    } catch (error) {
        if (errEl) {
            errEl.textContent = error.message || 'Could not get an answer. Try rephrasing or another theme.';
            errEl.classList.remove('hidden');
        }
    }
}

// Twin Stats
async function loadTwinStats() {
    try {
        const response = await fetch(`${API_BASE}/api/twin/stats`);
        if (response.ok) {
            twinStats = await response.json();
            renderTwinStats(twinStats);
        } else {
            renderTwinStatsFallback();
        }
    } catch (error) {
        renderTwinStatsFallback();
    }
}

function renderTwinStats(stats) {
    document.getElementById('daysOnJourney').textContent = stats.profile_summary?.days_on_journey || 1;
    document.getElementById('versesRead').textContent = stats.profile_summary?.verses_read || 0;
    document.getElementById('questionsAsked').textContent = stats.questions_asked || 0;
    
    // Top interests
    const interestsList = document.getElementById('topInterests');
    if (stats.top_interests?.length > 0) {
        interestsList.innerHTML = stats.top_interests.map(i => `
            <div class="interest-item">
                <strong>${i.topic}</strong> - explored ${i.times_explored} times
            </div>
        `).join('');
    }
    
    // Active struggles
    const strugglesList = document.getElementById('activeStruggles');
    if (stats.active_struggles?.length > 0) {
        strugglesList.innerHTML = stats.active_struggles.map(s => `
            <div class="struggle-item">
                <strong>${s.topic}</strong>
                <p>Questions asked: ${s.questions_asked?.length || 0}</p>
            </div>
        `).join('');
    }
}

function renderTwinStatsFallback() {
    document.getElementById('daysOnJourney').textContent = '1';
    document.getElementById('versesRead').textContent = '0';
    document.getElementById('questionsAsked').textContent = '0';
}

// Progress
async function loadProgress() {
    try {
        const response = await fetch(`${API_BASE}/api/reading-plan/progress`);
        if (response.ok) {
            const progress = await response.json();
            renderProgress(progress);
        } else {
            renderProgressFallback();
        }
    } catch (error) {
        renderProgressFallback();
    }
}

function renderProgress(progress) {
    const percentage = progress.percentage || 0;
    
    // Update circle
    const ring = document.getElementById('progressRing');
    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (percentage / 100) * circumference;
    ring.style.strokeDashoffset = offset;
    
    document.getElementById('progressNumber').textContent = `${Math.round(percentage)}%`;
    
    // Render periods
    const periodsList = document.getElementById('periodsList');
    if (progress.periods) {
        periodsList.innerHTML = progress.periods.map(p => `
            <div class="period-item">
                <span class="period-name">${p.name}</span>
                <span class="period-status ${p.status}">${p.status}</span>
            </div>
        `).join('');
    }
}

function renderProgressFallback() {
    const dayOfYear = getDayOfYear();
    const percentage = (dayOfYear / 365) * 100;
    
    const ring = document.getElementById('progressRing');
    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (percentage / 100) * circumference;
    ring.style.strokeDashoffset = offset;
    
    document.getElementById('progressNumber').textContent = `${Math.round(percentage)}%`;
}

// Utility Functions
function formatDate(dateStr) {
    if (!dateStr) return new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
}

function formatPassageText(text) {
    if (!text) return '<p>Loading passage text...</p>';
    // Split into paragraphs and wrap
    return text.split('\n').map(p => `<p>${p}</p>`).join('');
}

function truncate(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

function getDayOfYear() {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 0);
    const diff = now - start;
    const oneDay = 1000 * 60 * 60 * 24;
    return Math.floor(diff / oneDay);
}

function getMonthTheme() {
    const themes = [
        'Beginnings', 'Love and Covenant', 'Wilderness and Testing',
        'Redemption and New Life', 'Law and Wisdom', 'Prophetic Voice',
        'Kingdom and Power', 'Exile and Return', 'Work and Calling',
        'Community and Church', 'Gratitude and Provision', 'Promise and Fulfillment'
    ];
    return themes[new Date().getMonth()];
}
