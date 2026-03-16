# 🎿 Easter Egg: SkiFree Game

## 🎯 Concept
Add the legendary **SkiFree** game as a hidden easter egg in Taminator Settings. Because every TAM needs a break from RFE tracking, and nothing says "90s nostalgia" like being chased by the Abominable Snowman!

## 🎮 Game Description

**SkiFree** (1991) - The iconic Windows game where you:
- Ski down an infinite snowy slope
- Avoid trees, rocks, and other obstacles
- Do sick jumps and tricks
- Try to outrun the **Abominable Snowman**
- (Spoiler: You can't outrun him forever... 👹)

## 🎨 UI Integration

### Settings → Easter Eggs
```
┌─────────────────────────────────────────────────────────┐
│ Settings                                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🎨 Theme Selection                                      │
│   [Theme options...]                                    │
│                                                         │
│ 🎪 Easter Eggs                                          │
│                                                         │
│ ┌───────────────────────────────────────────────────┐  │
│ │  ☑ Enable SkiFree Game                            │  │
│ │     The legendary Windows game from 1991!         │  │
│ │     [🎿 Play Now]  [View High Scores]             │  │
│ │                                                   │  │
│ │     ⚠️ Warning: Abominable Snowman ahead!         │  │
│ └───────────────────────────────────────────────────┘  │
│                                                         │
│ ┌───────────────────────────────────────────────────┐  │
│ │  Konami Code: ↑↑↓↓←→←→BA                          │  │
│ │     Unlocks Super Clippy Mode                     │  │
│ └───────────────────────────────────────────────────┘  │
│                                                         │
│ ┌───────────────────────────────────────────────────┐  │
│ │  Type "IDDQD" in any text field                   │  │
│ │     Unlocks God Mode (immortal in SkiFree!)       │  │
│ └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### SkiFree Game Window
```
┌─────────────────────────────────────────────────────────┐
│ ● ○ ○  SkiFree - Taminator Edition            _ □ X    │
├─────────────────────────────────────────────────────────┤
│  File   Game   Help                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    🎿 SkiFree 🎿                        │
│                                                         │
│                        ⛷️                               │
│                                                         │
│                    🌲    🌲                             │
│                                                         │
│              🌲           🌲      🌲                    │
│                                                         │
│                  🪨                                     │
│                                                         │
│         🌲              🌲              🌲              │
│                                                         │
│                              🏂                         │
│                                                         │
│    🌲      🌲       🌲       🌲       🌲      🌲        │
│                                                         │
│  Score: 1337    Distance: 420m    Speed: 42 mph       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ Controls: ←→ Turn | ↑ Speed Up | ↓ Slow Down | Space Jump│
│ Press F to outrun Yeti (doesn't work lol)              │
└─────────────────────────────────────────────────────────┘
```

### Abominable Snowman Encounter
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                        ⛷️💨                             │
│                                                         │
│                                                         │
│                                                         │
│                   👹 ROAAAAR!                           │
│                    ╱|╲                                  │
│                   ╱ | ╲                                 │
│                  ╱  |  ╲                                │
│                                                         │
│              "You have been eaten!"                     │
│                                                         │
│           Final Score: 1337    Distance: 420m          │
│                                                         │
│         [Play Again]  [View High Scores]  [Exit]       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🎮 Game Features

### Core Gameplay
- ✅ Infinite scrolling snowy slope
- ✅ Player controls (arrow keys + space)
- ✅ Obstacles (trees, rocks, other skiers)
- ✅ Jumps and tricks
- ✅ Speed mechanics
- ✅ Score and distance tracking
- ✅ **The Abominable Snowman** (appears after ~2000m)

### TAM-Specific Additions
- 🎯 **RFE Obstacles**: Instead of rocks, dodge "JIRA-12345" labels
- 📧 **Email Powerup**: Collect emails for bonus points
- 📎 **Clippy Cameo**: Clippy appears to "help" (blocks your path)
- 🪟 **Windows XP Mode**: XP-styled graphics when XP theme is active
- 🏆 **TAM Leaderboard**: High scores saved per user

### Easter Eggs Within the Easter Egg
1. **Press F**: Shows message "F pressed. Nothing happened. You can't escape the Yeti."
2. **Type IDDQD**: God mode - invincible from snowman (for 30 seconds)
3. **100% speed**: Unlock "Lightspeed Skier" achievement
4. **500 points**: Clippy appears saying "It looks like you're skiing! Need help?"
5. **Get eaten 5 times**: Unlock "Yeti Food" badge

## 🔧 Implementation

### HTML Canvas Game
```html
<!-- Add to index.html -->
<div id="skifree-game" style="display: none;">
  <div class="game-window">
    <div class="game-titlebar">
      <span>🎿 SkiFree - Taminator Edition</span>
      <button onclick="closeSkiFree()">X</button>
    </div>
    
    <div class="game-menu">
      <span>File</span>
      <span>Game</span>
      <span>Help</span>
    </div>
    
    <canvas id="ski-canvas" width="600" height="500"></canvas>
    
    <div class="game-status">
      <span>Score: <span id="ski-score">0</span></span>
      <span>Distance: <span id="ski-distance">0</span>m</span>
      <span>Speed: <span id="ski-speed">0</span> mph</span>
    </div>
    
    <div class="game-controls">
      Controls: ←→ Turn | ↑ Speed Up | ↓ Slow Down | Space Jump | F to outrun Yeti (doesn't work)
    </div>
  </div>
</div>
```

### JavaScript Game Logic
```javascript
// SkiFree game implementation
class SkiFreeGame {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.width = canvas.width;
    this.height = canvas.height;
    
    // Player
    this.player = {
      x: this.width / 2,
      y: 100,
      speed: 0,
      maxSpeed: 10,
      direction: 0  // -1 left, 0 straight, 1 right
    };
    
    // Game state
    this.score = 0;
    this.distance = 0;
    this.obstacles = [];
    this.gameOver = false;
    this.yetiAppeared = false;
    this.godMode = false;
    this.godModeTimer = 0;
    
    // Yeti
    this.yeti = {
      active: false,
      x: -100,
      y: -100,
      speed: 0
    };
    
    this.setupControls();
    this.generateObstacles();
  }
  
  setupControls() {
    document.addEventListener('keydown', (e) => {
      if (this.gameOver) return;
      
      switch(e.key) {
        case 'ArrowLeft':
          this.player.direction = -1;
          break;
        case 'ArrowRight':
          this.player.direction = 1;
          break;
        case 'ArrowUp':
          this.player.speed = Math.min(this.player.speed + 1, this.player.maxSpeed);
          break;
        case 'ArrowDown':
          this.player.speed = Math.max(this.player.speed - 1, 0);
          break;
        case ' ':
          this.jump();
          break;
        case 'f':
        case 'F':
          this.tryToEscapeYeti();
          break;
      }
    });
    
    document.addEventListener('keyup', (e) => {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        this.player.direction = 0;
      }
    });
    
    // Secret code: IDDQD (Doom god mode)
    let keyBuffer = '';
    document.addEventListener('keypress', (e) => {
      keyBuffer += e.key;
      if (keyBuffer.length > 5) {
        keyBuffer = keyBuffer.slice(-5);
      }
      if (keyBuffer === 'iddqd') {
        this.activateGodMode();
      }
    });
  }
  
  generateObstacles() {
    const types = ['🌲', '🪨', '🏂', '🎿', '📧'];
    
    // TAM-specific obstacles
    if (Math.random() > 0.7) {
      types.push('JIRA-' + Math.floor(Math.random() * 10000));
    }
    
    for (let i = 0; i < 20; i++) {
      this.obstacles.push({
        x: Math.random() * this.width,
        y: i * 100 - this.height,
        type: types[Math.floor(Math.random() * types.length)],
        hit: false
      });
    }
  }
  
  jump() {
    // Implement jump logic
    this.player.jumping = true;
    this.score += 10;
    
    setTimeout(() => {
      this.player.jumping = false;
    }, 500);
  }
  
  tryToEscapeYeti() {
    // Easter egg: "F" key does nothing
    this.showMessage("F pressed. Nothing happened. You can't escape the Yeti. 😈");
    
    // Actually makes yeti faster
    if (this.yeti.active) {
      this.yeti.speed += 1;
    }
  }
  
  activateGodMode() {
    this.godMode = true;
    this.godModeTimer = 30000;  // 30 seconds
    this.showMessage("🛡️ GOD MODE ACTIVATED! Yeti can't touch you... for now.");
    
    setTimeout(() => {
      this.godMode = false;
      this.showMessage("⚠️ God Mode expired. Good luck! 😅");
    }, 30000);
  }
  
  update() {
    if (this.gameOver) return;
    
    // Move player
    this.player.x += this.player.direction * 5;
    this.player.x = Math.max(0, Math.min(this.width, this.player.x));
    
    // Increase distance and score
    this.distance += this.player.speed / 10;
    this.score += Math.floor(this.player.speed / 2);
    
    // Move obstacles
    this.obstacles.forEach(obs => {
      obs.y += this.player.speed;
      
      // Check collision
      if (!obs.hit && this.checkCollision(this.player, obs)) {
        if (obs.type === '📧') {
          // Bonus points
          this.score += 50;
          obs.hit = true;
        } else {
          // Hit obstacle - slow down
          this.player.speed = Math.max(0, this.player.speed - 2);
        }
      }
    });
    
    // Remove off-screen obstacles and add new ones
    this.obstacles = this.obstacles.filter(obs => obs.y < this.height + 100);
    while (this.obstacles.length < 20) {
      const types = ['🌲', '🪨', '🏂', '🎿', '📧'];
      if (Math.random() > 0.7) {
        types.push('JIRA-' + Math.floor(Math.random() * 10000));
      }
      
      this.obstacles.push({
        x: Math.random() * this.width,
        y: -100,
        type: types[Math.floor(Math.random() * types.length)],
        hit: false
      });
    }
    
    // Spawn Yeti after 2000m
    if (this.distance > 2000 && !this.yetiAppeared) {
      this.spawnYeti();
    }
    
    // Update Yeti
    if (this.yeti.active) {
      // Yeti chases player
      const dx = this.player.x - this.yeti.x;
      const dy = this.player.y - this.yeti.y;
      const angle = Math.atan2(dy, dx);
      
      this.yeti.speed = this.player.speed + 2;  // Yeti is faster!
      this.yeti.x += Math.cos(angle) * this.yeti.speed;
      this.yeti.y += Math.sin(angle) * this.yeti.speed;
      
      // Check if yeti caught player
      if (this.checkCollision(this.player, this.yeti)) {
        if (!this.godMode) {
          this.gameOver = true;
          this.showGameOver();
        } else {
          // Bounce yeti away in god mode
          this.yeti.y -= 50;
          this.score += 100;
        }
      }
    }
    
    // Clippy appearance at 500 points
    if (this.score > 500 && this.score < 520 && !this.clippyShown) {
      this.showClippyMessage("It looks like you're skiing! Need help? (Just kidding, you're on your own! 😄)");
      this.clippyShown = true;
    }
  }
  
  spawnYeti() {
    this.yetiAppeared = true;
    this.yeti.active = true;
    this.yeti.x = this.width / 2;
    this.yeti.y = -200;
    
    this.showMessage("⚠️ THE ABOMINABLE SNOWMAN IS COMING! 👹");
  }
  
  checkCollision(a, b) {
    const distance = Math.sqrt(
      Math.pow(a.x - b.x, 2) + 
      Math.pow(a.y - b.y, 2)
    );
    return distance < 30;
  }
  
  draw() {
    // Clear canvas
    this.ctx.fillStyle = 'white';
    this.ctx.fillRect(0, 0, this.width, this.height);
    
    // Draw obstacles
    this.ctx.font = '32px Arial';
    this.obstacles.forEach(obs => {
      if (!obs.hit) {
        this.ctx.fillText(obs.type, obs.x, obs.y);
      }
    });
    
    // Draw player
    this.ctx.fillText('⛷️', this.player.x - 16, this.player.y);
    
    // Draw yeti
    if (this.yeti.active) {
      this.ctx.font = '48px Arial';
      this.ctx.fillText('👹', this.yeti.x - 24, this.yeti.y);
      
      // Draw "ROAAAAR!" text
      this.ctx.font = '20px Arial';
      this.ctx.fillStyle = 'red';
      this.ctx.fillText('ROAAAAR!', this.yeti.x - 40, this.yeti.y - 40);
      this.ctx.fillStyle = 'black';
    }
    
    // Update score display
    document.getElementById('ski-score').textContent = Math.floor(this.score);
    document.getElementById('ski-distance').textContent = Math.floor(this.distance);
    document.getElementById('ski-speed').textContent = this.player.speed;
  }
  
  gameLoop() {
    this.update();
    this.draw();
    
    if (!this.gameOver) {
      requestAnimationFrame(() => this.gameLoop());
    }
  }
  
  showMessage(msg) {
    // Show toast notification
    console.log('[SkiFree]', msg);
    // Implement toast UI
  }
  
  showClippyMessage(msg) {
    // Show Clippy saying something
    console.log('[Clippy]', msg);
  }
  
  showGameOver() {
    // Show game over screen
    this.ctx.fillStyle = 'rgba(0,0,0,0.7)';
    this.ctx.fillRect(0, 0, this.width, this.height);
    
    this.ctx.fillStyle = 'white';
    this.ctx.font = '48px Arial';
    this.ctx.textAlign = 'center';
    this.ctx.fillText('YOU HAVE BEEN EATEN!', this.width/2, this.height/2 - 50);
    
    this.ctx.font = '24px Arial';
    this.ctx.fillText(`Final Score: ${Math.floor(this.score)}`, this.width/2, this.height/2 + 10);
    this.ctx.fillText(`Distance: ${Math.floor(this.distance)}m`, this.width/2, this.height/2 + 40);
    
    // Save high score
    this.saveHighScore();
  }
  
  saveHighScore() {
    const highScores = JSON.parse(localStorage.getItem('skifree-scores') || '[]');
    highScores.push({
      score: Math.floor(this.score),
      distance: Math.floor(this.distance),
      date: new Date().toISOString(),
      name: 'TAM Player'
    });
    
    highScores.sort((a, b) => b.score - a.score);
    highScores.splice(10);  // Keep top 10
    
    localStorage.setItem('skifree-scores', JSON.stringify(highScores));
  }
  
  start() {
    this.gameLoop();
  }
}

// Initialize game
let skiGame = null;

function launchSkiFree() {
  document.getElementById('skifree-game').style.display = 'block';
  const canvas = document.getElementById('ski-canvas');
  skiGame = new SkiFreeGame(canvas);
  skiGame.start();
}

function closeSkiFree() {
  document.getElementById('skifree-game').style.display = 'none';
  if (skiGame) {
    skiGame.gameOver = true;
  }
}
```

### Settings Integration
```javascript
function showSettings() {
  document.getElementById('content').innerHTML = `
    <div class="settings-container">
      <h2>🎨 Themes</h2>
      <!-- Theme options... -->
      
      <h2>🎪 Easter Eggs</h2>
      
      <div class="easter-egg-card">
        <div class="easter-egg-header">
          <input type="checkbox" id="enable-skifree" 
                 ${localStorage.getItem('skifree-enabled') === 'true' ? 'checked' : ''}>
          <label for="enable-skifree">
            <strong>🎿 Enable SkiFree Game</strong>
          </label>
        </div>
        
        <p class="easter-egg-description">
          The legendary Windows game from 1991! Ski down the mountain and 
          avoid the Abominable Snowman. (Spoiler: You can't.)
        </p>
        
        <div class="easter-egg-actions">
          <button class="btn btn-primary" onclick="launchSkiFree()">
            🎿 Play Now
          </button>
          <button class="btn btn-secondary" onclick="showSkiFreeScores()">
            🏆 View High Scores
          </button>
        </div>
        
        <div class="easter-egg-warning">
          ⚠️ Warning: Abominable Snowman ahead! Press F to... well, try it and see.
        </div>
      </div>
      
      <div class="easter-egg-tips">
        <h3>🎮 Secret Codes</h3>
        <ul>
          <li><code>↑↑↓↓←→←→BA</code> - Konami Code (Unlocks Super Clippy)</li>
          <li><code>IDDQD</code> - God Mode in SkiFree (30 seconds)</li>
          <li><code>F key</code> - Try to outrun Yeti (good luck!)</li>
        </ul>
      </div>
    </div>
  `;
}
```

## 🏆 High Scores System

### Leaderboard
```javascript
function showSkiFreeScores() {
  const scores = JSON.parse(localStorage.getItem('skifree-scores') || '[]');
  
  const html = `
    <div class="skifree-scores">
      <h2>🏆 SkiFree High Scores</h2>
      
      <table class="scores-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Score</th>
            <th>Distance</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          ${scores.map((s, i) => `
            <tr>
              <td>${i + 1}</td>
              <td>${s.score}</td>
              <td>${s.distance}m</td>
              <td>${new Date(s.date).toLocaleDateString()}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <button class="btn btn-secondary" onclick="resetSkiFreeScores()">
        Reset Scores
      </button>
    </div>
  `;
  
  // Show in modal or separate view
  document.getElementById('content').innerHTML = html;
}
```

## 🎯 Achievements

```javascript
const SKIFREE_ACHIEVEMENTS = {
  first_game: {
    title: "First Run",
    description: "Play SkiFree for the first time",
    icon: "🎿"
  },
  yeti_food: {
    title: "Yeti Food",
    description: "Get eaten by the Yeti 5 times",
    icon: "👹"
  },
  speed_demon: {
    title: "Speed Demon",
    description: "Reach maximum speed",
    icon: "⚡"
  },
  distance_king: {
    title: "Distance King",
    description: "Ski 5000m in one run",
    icon: "👑"
  },
  god_mode: {
    title: "Divine Intervention",
    description: "Use god mode (IDDQD)",
    icon: "🛡️"
  },
  f_key_warrior: {
    title: "F Key Warrior",
    description: "Press F 10 times trying to escape the Yeti",
    icon: "F"
  },
  clippy_encounter: {
    title: "Clippy's Wisdom",
    description: "See Clippy's skiing advice",
    icon: "📎"
  }
};
```

## 🎨 XP Theme Integration

When Windows XP theme is active:
- Game window uses XP styling
- Menu bar looks like XP
- Buttons are XP-style
- Even the game over screen is XP-themed!

## 📊 Stats Tracking

```javascript
const skiStats = {
  gamesPlayed: 0,
  totalDistance: 0,
  timesEatenByYeti: 0,
  highestScore: 0,
  fKeyPresses: 0,
  godModeUsed: 0
};
```

## 🎪 TAM-Specific Features

1. **RFE Obstacles**: Dodge JIRA tickets while skiing
2. **Email Powerups**: Collect emails for bonus points
3. **Meeting Obstacles**: "Video call starting" blocks appear
4. **Clippy Commentary**: Random helpful/unhelpful skiing tips
5. **TAM Leaderboard**: Compete with other TAMs

---

**Status**: Fully designed, ready to implement
**Effort**: 2-3 days for full game
**Fun Factor**: INFINITE 🎿
**Nostalgia Level**: MAXIMUM ❄️
**Yeti Danger**: VERY HIGH 👹
**F Key Effectiveness**: 0% (but hilarious) 😂

