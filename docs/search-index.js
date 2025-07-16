// Search Index for Hyperchronal Framework Website
const searchIndex = {
    pages: [
        {
            id: "home",
            title: "Hyperchronal Framework | Consciousness as Fundamental Field",
            url: "/",
            description: "Revolutionary physics framework proposing consciousness as fundamental scalar field Ψ. Explore quantum field theory, 4-qubit simulations, and testable predictions.",
            keywords: ["consciousness", "quantum field theory", "hyperchronal framework", "scalar field", "physics theory", "theoretical physics"],
            content: "consciousness universal field matter ripple fundamental phenomena emerge brain activity backwards physical revolutionary proposition traditional science byproduct consciousness field equations mathematical heart waves ocean interact patterns minds quantum foundations particle interactions field fluctuations corrections standard physics cosmic evidence early universe fingerprints conscious influence dark energy cosmic structure formation fine-tuning hyperchronal field cosmic evolution biological interfaces living systems evolved harness quantum coherence consciousness extended 4-qubit simulations colored noise biological structures maintain coherent states resonant coupling hyperchronal field subjective experience emerges neural networks"
        },
        {
            id: "theory",
            title: "Core Theory - The Mathematical Heart",
            url: "#theory",
            description: "The fundamental mathematics and concepts behind consciousness as a universal field. Complete field equations and philosophical implications.",
            keywords: ["field equations", "mathematical framework", "consciousness field", "quantum mechanics", "physics theory"],
            content: "core theory mathematical heart revolutionary proposition traditional science complex brains generate consciousness purely physical processes framework consciousness fundamental field gravity electromagnetism physical phenomena emerge everyday terms instead asking brain create consciousness ask consciousness create appearance separate brains discovering thought individual whirlpools actually patterns vast ocean mathematical heart hyperchronal field equation del squared psi minus m squared psi plus lambda psi cubed plus integral psi times green function equals consciousness source term simple terms consciousness waves ocean equation describes waves flow interact create stable patterns experience individual minds"
        },
        {
            id: "research",
            title: "Testing Framework - Can We Prove It?",
            url: "#research",
            description: "Concrete experimental predictions for particle physics, cosmic observations, and biological quantum systems to test the hyperchronal framework.",
            keywords: ["experimental predictions", "particle physics", "cosmic observations", "biological quantum systems", "testing framework"],
            content: "prove testing framework seems untestable actually yields concrete predictions consciousness subjective unmeasurable mathematical framework makes precise predictions tested cutting-edge physics experiments quantum foundations consciousness shapes quantum fields specific signatures particle interactions field fluctuations quantum corrections explained standard physics alone cosmic evidence early universe bear fingerprints conscious influence dark energy cosmic structure formation universe fine-tuning reflect hyperchronal field role cosmic evolution biological interfaces living systems evolved harness quantum coherence consciousness extended 4-qubit simulations colored noise reveal biological structures maintain coherent states resonant coupling hyperchronal field explaining subjective experience emerges neural networks"
        },
        {
            id: "breakthrough",
            title: "4-Qubit Consciousness Models - Breakthrough Simulations",
            url: "#breakthrough",
            description: "Latest quantum biological simulations providing computational evidence for consciousness emergence through resonant coupling with the hyperchronal field.",
            keywords: ["4-qubit simulations", "quantum biological", "consciousness models", "resonant coupling", "computational evidence"],
            content: "breakthrough 4-qubit consciousness models latest quantum biological simulations compelling computational evidence consciousness emerge resonant coupling biological quantum systems hyperchronal field key results coherence decay 4.0 0.376 stabilized oscillations optimal tuning gamma 0.01 consciousness window pink noise alpha 0.262 psi-field signature quantum system tuned specific frequencies gamma 0.01 maintained organization longer random noise allow suggesting biological systems achieve stable consciousness precisely tuned coupling hyperchronal field"
        },
        {
            id: "faq",
            title: "Frequently Asked Questions",
            url: "#faq",
            description: "Common questions and concerns about the hyperchronal framework, addressing scientific rigor and philosophical implications.",
            keywords: ["FAQ", "pseudoscience", "rocks conscious", "AI consciousness", "scientific methodology"],
            content: "frequently asked questions pseudoscience provide testable mathematical predictions established quantum field theory propose specific experiments framework follows scientific methodology speculative mathematically rigorous early relativity quantum mechanics rocks conscious framework suggests matter primitive field fluctuations consciousness know requires complex organization think temperature everything thermal motion organized systems exhibit complex thermal behaviors AI consciousness framework correct truly conscious AI need interface hyperchronal field process information suggests consciousness detection AI safety require understanding field coupling computational complexity"
        },
        {
            id: "interactive",
            title: "Interactive Explorer",
            url: "/app/",
            description: "Live mathematical visualizations: Mexican-hat potentials, consciousness solitons, and cosmic evolution simulations.",
            keywords: ["interactive explorer", "mathematical visualizations", "mexican-hat potentials", "consciousness solitons", "cosmic evolution"],
            content: "interactive explorer live mathematical visualizations mexican-hat potentials consciousness solitons cosmic evolution simulations"
        }
    ],
    
    // Search function
    search: function(query) {
        if (!query || query.trim().length < 2) return [];
        
        const terms = query.toLowerCase().split(/\s+/).filter(term => term.length > 1);
        const results = [];
        
        this.pages.forEach(page => {
            let score = 0;
            const titleLower = page.title.toLowerCase();
            const descLower = page.description.toLowerCase();
            const contentLower = page.content.toLowerCase();
            const keywordsLower = page.keywords.join(' ').toLowerCase();
            
            terms.forEach(term => {
                // Title matches (highest weight)
                if (titleLower.includes(term)) score += 10;
                
                // Keyword matches (high weight)
                if (keywordsLower.includes(term)) score += 8;
                
                // Description matches (medium weight)
                if (descLower.includes(term)) score += 5;
                
                // Content matches (low weight)
                const contentMatches = (contentLower.match(new RegExp(term, 'g')) || []).length;
                score += contentMatches * 2;
            });
            
            if (score > 0) {
                results.push({
                    ...page,
                    score: score,
                    matchedTerms: terms.filter(term => 
                        titleLower.includes(term) || 
                        descLower.includes(term) || 
                        contentLower.includes(term) ||
                        keywordsLower.includes(term)
                    )
                });
            }
        });
        
        return results.sort((a, b) => b.score - a.score);
    },
    
    // Get suggestions for autocomplete
    getSuggestions: function(query) {
        if (!query || query.length < 2) return [];
        
        const suggestions = new Set();
        const queryLower = query.toLowerCase();
        
        this.pages.forEach(page => {
            page.keywords.forEach(keyword => {
                if (keyword.toLowerCase().includes(queryLower)) {
                    suggestions.add(keyword);
                }
            });
            
            // Add title words as suggestions
            page.title.split(/\s+/).forEach(word => {
                if (word.toLowerCase().includes(queryLower) && word.length > 2) {
                    suggestions.add(word.replace(/[^\w\s]/g, ''));
                }
            });
        });
        
        return Array.from(suggestions).slice(0, 8);
    }
};
