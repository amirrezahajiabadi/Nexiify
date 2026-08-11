# Modern Web Design Systems

## Design Categories

### 1. Minimalist Professional

#### Color Palette
```css
/* Primary Colors */
--primary-50: #f8fafc;
--primary-100: #f1f5f9;
--primary-500: #64748b;
--primary-900: #0f172a;

/* Accent Colors */
--accent-500: #3b82f6;
--accent-600: #2563eb;

/* Semantic Colors */
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
```

#### Typography Scale
```css
/* Font Family */
--font-sans: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

#### Spacing System
```css
--space-1: 0.25rem;    /* 4px */
--space-2: 0.5rem;     /* 8px */
--space-4: 1rem;       /* 16px */
--space-6: 1.5rem;     /* 24px */
--space-8: 2rem;       /* 32px */
--space-12: 3rem;      /* 48px */
--space-16: 4rem;      /* 64px */
--space-20: 5rem;      /* 80px */
```

### 2. Modern SaaS

#### Color Palette
```css
/* Primary Gradient */
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--primary-500: #667eea;
--primary-600: #5a67d8;

/* Background Colors */
--bg-primary: #ffffff;
--bg-secondary: #f7fafc;
--bg-tertiary: #edf2f7;

/* Interactive Colors */
--interactive-hover: #e2e8f0;
--interactive-active: #cbd5e0;
```

#### Component Elevation
```css
/* Shadow System */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);
```

#### Animation Timing
```css
--duration-fast: 150ms;
--duration-normal: 250ms;
--duration-slow: 350ms;
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

### 3. Creative Portfolio

#### Experimental Color Scheme
```css
/* Vibrant Palette */
--primary-pink: #ec4899;
--primary-purple: #8b5cf6;
--primary-blue: #06b6d4;
--primary-green: #10b981;

/* Dark Mode */
--dark-bg: #0f0f23;
--dark-surface: #1a1a3e;
--dark-text: #e2e8f0;
```

#### Creative Typography
```css
/* Display Fonts */
--font-display: 'Playfair Display', serif;
--font-creative: 'Space Grotesk', sans-serif;

/* Font Weights */
--weight-light: 300;
--weight-normal: 400;
--weight-medium: 500;
--weight-bold: 700;
--weight-black: 900;
```

### 4. E-commerce Optimized

#### Trust & Conversion Colors
```css
/* Primary Brand */
--brand-primary: #059669;
--brand-secondary: #0d9488;

/* Conversion Elements */
--cta-primary: #dc2626;
--cta-secondary: #ea580c;
--trust-green: #059669;
--urgency-orange: #ea580c;
```

#### Product Display
```css
/* Product Card */
--product-bg: #ffffff;
--product-border: #e5e7eb;
--product-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

/* Price Display */
--price-primary: #1f2937;
--price-sale: #dc2626;
--price-original: #9ca3af;
```

## Layout Systems

### Grid Patterns

#### 12-Column Grid
```css
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}

.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
}
```

#### Card Grid System
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}
```

### Responsive Breakpoints
```css
/* Mobile First */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

## Component Patterns

### Button Variants
```css
/* Primary Button */
.btn-primary {
  background: var(--primary-500);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  transition: all var(--duration-normal) var(--ease-in-out);
}

.btn-primary:hover {
  background: var(--primary-600);
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}
```

### Card Components
```css
.card {
  background: var(--bg-primary);
  border-radius: 0.75rem;
  box-shadow: var(--shadow-md);
  overflow: hidden;
  transition: all var(--duration-normal) var(--ease-in-out);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}
```

### Input Styling
```css
.input-field {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--gray-200);
  border-radius: 0.5rem;
  font-size: var(--text-base);
  transition: border-color var(--duration-fast);
}

.input-field:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}
```

## Animation Library

### Micro-interactions
```css
/* Hover Lift */
.hover-lift {
  transition: transform var(--duration-normal) var(--ease-in-out);
}
.hover-lift:hover {
  transform: translateY(-2px);
}

/* Scale on Hover */
.hover-scale {
  transition: transform var(--duration-normal) var(--ease-in-out);
}
.hover-scale:hover {
  transform: scale(1.05);
}
```

### Loading States
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

### Scroll Animations
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}
```

## Accessibility Standards

### Color Contrast
- AA Standard: 4.5:1 for normal text
- AA Standard: 3:1 for large text
- AAA Standard: 7:1 for normal text

### Focus States
```css
.focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

### Screen Reader Support
- Use semantic HTML elements
- Include ARIA labels where needed
- Maintain logical heading hierarchy
- Provide alt text for images