# AI Workshop Presentation

**From AI User to AI Builder** - A 2-hour workshop presentation built with Reveal.js

## Design System

### Colors
- **Dark Navy:** `#1a1d2e` - Main dark background
- **Deep Navy:** `#0f1419` - Secondary dark background
- **Neon Green:** `#00ff87` - Primary accent color
- **Neon Green Alt:** `#39ff14` - Alternative accent
- **White:** `#ffffff` - Default slide background
- **Light Gray:** `#a0a0a0` - Secondary text

### Typography
- **Headings:** Montserrat (Bold, 700-900)
- **Body Text:** Inter (Regular, 400-700)
- **Code:** JetBrains Mono (400-600)

### Design Principles
- ✅ Solid colors only (no gradients)
- ✅ Sharp edges (no border radius)
- ✅ Modern, minimal aesthetic
- ✅ Grid patterns for dark backgrounds
- ✅ Smooth animations
- ✅ High contrast

## Project Structure

```
presentation/
├── index.html          # Main presentation file
├── css/
│   └── theme.css       # Custom theme styles
├── js/
│   └── init.js         # Reveal.js configuration
├── assets/             # Images, icons, etc.
└── README.md          # This file
```

## How to Use

### 1. Open the Presentation

Simply open `index.html` in a web browser:

```bash
cd presentation
open index.html  # macOS
# or
start index.html # Windows
# or
xdg-open index.html # Linux
```

### 2. Local Server (Recommended)

For better performance, run a local server:

```bash
# Using Python 3
python3 -m http.server 8000

# Using Python 2
python -m SimpleHTTPServer 8000

# Using Node.js
npx serve

# Then open: http://localhost:8000
```

### 3. Navigation

- **Arrow Keys / Space:** Navigate slides
- **F:** Enter fullscreen
- **S:** Open speaker notes
- **O:** Overview mode (see all slides)
- **B:** Pause (black screen)
- **?:** Show keyboard shortcuts
- **Esc:** Exit overview/zoom

### 4. Presenter Mode

Press `S` to open speaker notes view (shows current slide, next slide, and notes)

## Slide Types Included

### 1. Title Slide (Dark Background)
- Full-screen impact
- Animated geometric shapes
- Grid pattern background
- Green glow effects

### 2. Interactive Question Slide (White Background)
- Question boxes with hover effects
- Fragment animations
- Hand emoji icons with glow

### 3. App Grid Slide (White Background)
- 3x3 grid layout
- Dark card design with green borders
- Hover animations
- Quote highlights

### 4. Impact Slide (Dark Background)
- Staged text reveal
- Large typography
- Question mark background
- Dramatic zoom effect

### 5. Code Example Slide (White Background)
- Syntax-highlighted code block
- Line number highlighting
- Dark code editor theme
- Caption with highlights

### 6. Design System Slide (White Background)
- Grid layout demonstrating brand elements
- Color swatches
- Typography samples
- Interactive element showcase

## Customization

### Adding New Slides

Add new `<section>` elements inside `.slides`:

```html
<!-- White background slide (default) -->
<section class="white-bg">
    <h2 class="dark-heading">Your Heading</h2>
    <p>Your content...</p>
</section>

<!-- Dark background slide -->
<section class="dark-bg">
    <h2>Your Heading</h2>
    <p>Your content...</p>
</section>
```

### Using Fragments (Animated Reveals)

```html
<div class="fragment fade-up">This appears first</div>
<div class="fragment fade-up">This appears second</div>
```

### Code Blocks with Highlighting

```html
<pre class="code-block"><code class="language-python" data-trim data-line-numbers="|1-2|4-5">
# Your code here
print("Hello World")
</code></pre>
```

### Transitions

Add to any `<section>`:
- `data-transition="zoom"`
- `data-transition="slide"`
- `data-transition="convex"`
- `data-transition="fade"`

## Features

✅ Fully responsive design
✅ Smooth animations and transitions
✅ Syntax highlighting for code
✅ Speaker notes support
✅ PDF export capability
✅ Keyboard navigation
✅ Touch/swipe support
✅ Progress bar
✅ Slide numbers
✅ Overview mode

## Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Export to PDF

1. Add `?print-pdf` to URL: `index.html?print-pdf`
2. Open print dialog (Cmd/Ctrl + P)
3. Select "Save as PDF"
4. Adjust margins to "None"
5. Enable "Background graphics"

## Tips

- Use `B` key to pause/blackout during discussions
- Use `S` for speaker view with notes and timer
- Use `O` for overview to jump to specific slides
- Add `data-notes="Your notes"` to any slide for speaker notes

## Next Steps

This is a sample presentation with 6 slides demonstrating the brand guidelines. To build the full 56-slide workshop:

1. Follow the slide layouts established here
2. Reference `Docs/ai_workshop_slide_deck.md` for content
3. Maintain consistent design system
4. Add more fragment animations for engagement
5. Include speaker notes for each slide

## Credits

- Built with [Reveal.js](https://revealjs.com/)
- Fonts: Google Fonts
- Code highlighting: Highlight.js

---

**Created for:** B.Tech CSE AI Workshop
**By:** Arjit | @codewitharjit
**Date:** November 2025
