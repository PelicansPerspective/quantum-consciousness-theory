// Hyperchronal Explorer - Interactive Application
// Global state management and visualization

// Global parameters
let globalParams = {
    m: 1.0,
    g: 0.5,
    k: 0.05,
    kappa_c: 0.7
};

// Chart instances
let potentialChart = null;
let couplingChart = null;
let entropyChart = null;

// Navigation functionality - Make available immediately
window.scrollToSection = function(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        // Account for fixed navbar height
        const navbarHeight = 72;
        const elementTop = element.offsetTop - navbarHeight;
        window.scrollTo({
            top: elementTop,
            behavior: 'smooth'
        });
    }
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize interface elements first
    initializeInterface();
    
    // Setup event listeners
    setupPotentialSection();
    setupCosmologySection();
    setupKernelSection();
    
    // Initialize all calculations
    updatePotentialChart();
    updateSolitonValues();
    updateCosmologyValues();
    updateKernelCharts();
    
    // MathJax rendering
    if (window.MathJax) {
        MathJax.typesetPromise();
    }
});

// Initialize interface with current values
function initializeInterface() {
    document.getElementById('m-value').textContent = globalParams.m.toFixed(1);
    document.getElementById('g-value').textContent = globalParams.g.toFixed(2);
    document.getElementById('k-value').textContent = globalParams.k.toFixed(2);
    document.getElementById('kappa-c-value').textContent = globalParams.kappa_c.toFixed(2);
    
    // Set initial slider values
    document.getElementById('m-slider').value = globalParams.m;
    document.getElementById('m-input').value = globalParams.m;
    document.getElementById('g-slider').value = globalParams.g;
    document.getElementById('g-input').value = globalParams.g;
    document.getElementById('k-slider').value = globalParams.k;
    document.getElementById('kappa-c-slider').value = globalParams.kappa_c;
}

// POTENTIAL SECTION
function setupPotentialSection() {
    const mSlider = document.getElementById('m-slider');
    const mInput = document.getElementById('m-input');
    const gSlider = document.getElementById('g-slider');
    const gInput = document.getElementById('g-input');
    
    function updateMParameter(value) {
        globalParams.m = parseFloat(value);
        mSlider.value = globalParams.m;
        mInput.value = globalParams.m;
        document.getElementById('m-value').textContent = globalParams.m.toFixed(1);
        updatePotentialChart();
        updateSolitonValues();
    }
    
    function updateGParameter(value) {
        globalParams.g = parseFloat(value);
        gSlider.value = globalParams.g;
        gInput.value = globalParams.g;
        document.getElementById('g-value').textContent = globalParams.g.toFixed(2);
        updatePotentialChart();
        updateSolitonValues();
    }
    
    // Sync sliders and inputs
    mSlider.addEventListener('input', (e) => {
        updateMParameter(e.target.value);
    });
    
    mInput.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        if (value >= 0.1 && value <= 10) {
            updateMParameter(value);
        }
    });
    
    gSlider.addEventListener('input', (e) => {
        updateGParameter(e.target.value);
    });
    
    gInput.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        if (value >= 0.01 && value <= 5) {
            updateGParameter(value);
        }
    });
}

function updatePotentialChart() {
    const canvas = document.getElementById('potential-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Calculate potential function V(φ) = -m²φ² + gφ⁴
    const m = globalParams.m;
    const g = globalParams.g;
    const v = m * m / (2 * g); // vacuum expectation value
    
    // Range for φ: [-3m/g, 3m/g]
    const phiRange = 3 * m / g;
    const phiData = [];
    const vData = [];
    
    for (let phi = -phiRange; phi <= phiRange; phi += phiRange / 100) {
        const V = -m * m * phi * phi + g * phi * phi * phi * phi;
        phiData.push(phi);
        vData.push(V);
    }
    
    const chartData = phiData.map((phi, i) => ({ x: phi, y: vData[i] }));
    
    // Add markers for vacuum expectation values
    const vevMarkers = [
        { x: v, y: -m * m * v * v + g * v * v * v * v },
        { x: -v, y: -m * m * v * v + g * v * v * v * v }
    ];
    
    if (potentialChart) {
        potentialChart.destroy();
    }
    
    potentialChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'V(φ)',
                data: chartData,
                borderColor: '#00b5e2',
                backgroundColor: 'rgba(0, 181, 226, 0.1)',
                fill: true,
                tension: 0.4
            }, {
                label: 'Vacuum states (±v)',
                data: vevMarkers,
                borderColor: '#ff6b6b',
                backgroundColor: '#ff6b6b',
                pointRadius: 8,
                pointHoverRadius: 10,
                showLine: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Mexican-Hat Potential: V(φ) = -m²φ² + gφ⁴',
                    color: '#fff'
                },
                legend: {
                    labels: {
                        color: '#fff'
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'φ',
                        color: '#fff'
                    },
                    ticks: {
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'V(φ)',
                        color: '#fff'
                    },
                    ticks: {
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
    
    // Update VEV display
    const vevDisplay = document.getElementById('vev-display');
    if (vevDisplay) {
        vevDisplay.textContent = v.toFixed(3);
    }
}

// VACUUM & SOLITON SECTION - Enhanced with better error handling
function updateSolitonValues() {
    const m = globalParams.m;
    const g = globalParams.g;
    
    // Vacuum expectation value: v = m²/(2g)
    const v = m * m / (2 * g);
    
    // Soliton mass: M = 8π²v²/g
    const M = 8 * Math.PI * Math.PI * v * v / g;
    
    // Soliton size: ≈ 1/√(gv²)
    const size = 1 / Math.sqrt(g * v * v);
    
    // Update display with 3 significant figures
    const solitonVevEl = document.getElementById('soliton-vev');
    const solitonMassEl = document.getElementById('soliton-mass');
    const solitonSizeEl = document.getElementById('soliton-size');
    
    if (solitonVevEl) {
        solitonVevEl.textContent = v.toPrecision(3);
    }
    if (solitonMassEl) {
        solitonMassEl.textContent = M.toPrecision(3);
    }
    if (solitonSizeEl) {
        solitonSizeEl.textContent = size.toPrecision(3);
    }
}

// COSMOLOGY SECTION
function setupCosmologySection() {
    const kSlider = document.getElementById('k-slider');
    
    kSlider.addEventListener('input', (e) => {
        globalParams.k = parseFloat(e.target.value);
        document.getElementById('k-value').textContent = globalParams.k.toFixed(2);
        updateCosmologyValues();
    });
}

function updateCosmologyValues() {
    const k = globalParams.k;
    
    // Equation of state: w = (k - 1)/(k + 1)
    const w = (k - 1) / (k + 1);
    
    const wValueEl = document.getElementById('w-value');
    if (wValueEl) {
        wValueEl.textContent = w.toFixed(3);
    }
    
    // Update acceleration indicator
    const indicator = document.getElementById('w-indicator');
    if (indicator) {
        if (w < -1/3) {
            indicator.textContent = 'ACCELERATING';
            indicator.style.backgroundColor = 'rgba(0, 181, 226, 0.3)';
            indicator.style.color = '#00b5e2';
            indicator.style.border = '1px solid #00b5e2';
        } else {
            indicator.textContent = 'DECELERATING';
            indicator.style.backgroundColor = 'rgba(255, 107, 107, 0.3)';
            indicator.style.color = '#ff6b6b';
            indicator.style.border = '1px solid #ff6b6b';
        }
    }
}

// KERNEL TIME ARROW SECTION
function setupKernelSection() {
    const kappaSlider = document.getElementById('kappa-c-slider');
    
    kappaSlider.addEventListener('input', (e) => {
        globalParams.kappa_c = parseFloat(e.target.value);
        document.getElementById('kappa-c-value').textContent = globalParams.kappa_c.toFixed(2);
        updateKernelCharts();
    });
}

function updateKernelCharts() {
    updateCouplingChart();
    updateEntropyChart();
}

function updateCouplingChart() {
    const canvas = document.getElementById('coupling-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    const kappa_c = globalParams.kappa_c;
    const kappa_a = 1 - kappa_c;
    
    if (couplingChart) {
        couplingChart.destroy();
    }
    
    couplingChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['κ_c (Coherence)', 'κ_a (Arrow)'],
            datasets: [{
                data: [kappa_c, kappa_a],
                backgroundColor: ['#00b5e2', '#ff6b6b'],
                borderColor: ['#00b5e2', '#ff6b6b'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 1,
                    title: {
                        display: true,
                        text: 'Coupling Value',
                        color: '#fff'
                    },
                    ticks: {
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}

function updateEntropyChart() {
    const canvas = document.getElementById('entropy-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    const kappa_c = globalParams.kappa_c;
    const kappa_a = 1 - kappa_c;
    
    // Generate entropy data: S_rec(τ) = S0 + (1 - κ_c) * τ
    // S0 = 0, A = 1, τ ∈ [0, 10]
    const tauData = [];
    const entropyData = [];
    
    for (let tau = 0; tau <= 10; tau += 0.1) {
        const S_rec = 0 + kappa_a * tau; // S0 = 0, A = 1
        tauData.push(tau);
        entropyData.push(S_rec);
    }
    
    const chartData = tauData.map((tau, i) => ({ x: tau, y: entropyData[i] }));
    
    if (entropyChart) {
        entropyChart.destroy();
    }
    
    entropyChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'S_rec(τ)',
                data: chartData,
                borderColor: '#00b5e2',
                backgroundColor: 'rgba(0, 181, 226, 0.1)',
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#fff'
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'τ (time)',
                        color: '#fff'
                    },
                    ticks: {
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'S_rec(τ)',
                        color: '#fff'
                    },
                    ticks: {
                        color: '#fff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}