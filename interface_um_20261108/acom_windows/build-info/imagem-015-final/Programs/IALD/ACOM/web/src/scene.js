const TAU = Math.PI * 2;
const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function seededRandom(seed) {
  let state = seed >>> 0;
  return () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 4294967296;
  };
}

export function createSpaceScene(canvas) {
  const context = canvas.getContext('2d', { alpha: true });
  const random = seededRandom(11031996);
  const stars = Array.from({ length: 330 }, () => ({
    x: random(), y: random(), z: random(), size: .35 + random() * 1.35,
    alpha: .15 + random() * .65, phase: random() * TAU
  }));
  const dust = Array.from({ length: 84 }, (_, index) => ({
    angle: random() * TAU,
    radius: .12 + random() * .44,
    depth: .2 + random() * .8,
    speed: .12 + random() * .45,
    size: .35 + random() * 1.5,
    tone: index % 7 === 0 ? 'gold' : 'cyan'
  }));
  let width = 0;
  let height = 0;
  let ratio = 1;
  let running = !reducedMotion.matches;
  let phase = 'welcome';
  let progress = 0;
  let frame = 0;
  let previous = 0;
  let time = 0;

  function resize() {
    const bounds = canvas.getBoundingClientRect();
    ratio = Math.min(window.devicePixelRatio || 1, 1.5);
    width = Math.max(1, bounds.width);
    height = Math.max(1, bounds.height);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    render(time);
  }

  function render(now) {
    time = now;
    context.clearRect(0, 0, width, height);
    for (const star of stars) {
      const twinkle = running ? .72 + Math.sin(now * .0007 + star.phase) * .28 : 1;
      context.fillStyle = `rgba(205,225,230,${star.alpha * twinkle})`;
      const drift = running ? Math.sin(now * .000025 + star.phase) * 1.5 * star.z : 0;
      context.fillRect(star.x * width + drift, star.y * height, star.size, star.size);
    }

    const nodes = dust.map((particle) => ({
      x: (.5 + Math.cos(particle.angle) * particle.radius * 1.45) * width,
      y: (.5 + Math.sin(particle.angle) * particle.radius * 1.1) * height,
      size: particle.size,
      tone: particle.tone
    }));
    context.lineWidth = .45;
    nodes.forEach((node, index) => {
      const next = nodes[(index + 1) % nodes.length];
      const distance = Math.hypot(node.x - next.x, node.y - next.y);
      if (distance < Math.min(width, height) * .2) {
        context.strokeStyle = 'rgba(126,214,215,.028)';
        context.beginPath(); context.moveTo(node.x, node.y); context.lineTo(next.x, next.y); context.stroke();
      }
      context.beginPath();
      context.fillStyle = node.tone === 'gold' ? 'rgba(222,190,125,.18)' : 'rgba(126,214,215,.14)';
      context.arc(node.x, node.y, node.size, 0, TAU);
      context.fill();
    });
  }

  function loop(timestamp) {
    frame = 0;
    if (!running) return;
    if (timestamp - previous > 32) {
      previous = timestamp;
      render(timestamp * .001);
    }
    frame = requestAnimationFrame(loop);
  }

  function setRunning(value) {
    running = Boolean(value) && !reducedMotion.matches;
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    if (running) frame = requestAnimationFrame(loop);
    else render(time);
  }

  resize();
  window.addEventListener('resize', resize, { passive: true });
  setRunning(running);

  return {
    setPhase(value) { phase = value; render(time); },
    setProgress(value) { progress = clamp(value); render(time); },
    setRunning,
    renderOnce() { render(time); },
    destroy() { setRunning(false); window.removeEventListener('resize', resize); }
  };
}

export function createQuantumScene(canvas) {
  const context = canvas.getContext('2d');
  let width = 0;
  let height = 0;
  let ratio = 1;
  let running = !reducedMotion.matches;
  let stage = 0;
  let frame = 0;
  let previous = 0;
  let time = 0;

  function resize() {
    const bounds = canvas.getBoundingClientRect();
    ratio = Math.min(window.devicePixelRatio || 1, 1.5);
    width = Math.max(1, bounds.width);
    height = Math.max(1, bounds.height);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    render(time);
  }

  function render(now) {
    time = now;
    context.clearRect(0, 0, width, height);
    const cx = width * .5;
    const cy = height * .47;
    const unit = Math.min(width, height);
    const radius = unit * .28;
    context.lineWidth = .8;

    const glow = context.createRadialGradient(cx, cy, 0, cx, cy, radius * 1.7);
    glow.addColorStop(0, 'rgba(114,211,211,.075)');
    glow.addColorStop(1, 'rgba(114,211,211,0)');
    context.fillStyle = glow;
    context.fillRect(0, 0, width, height);

    context.strokeStyle = 'rgba(155,196,202,.24)';
    context.beginPath(); context.arc(cx, cy, radius, 0, TAU); context.stroke();
    for (const scale of [.34, .66]) {
      context.beginPath(); context.ellipse(cx, cy, radius, radius * scale, 0, 0, TAU); context.stroke();
    }
    context.beginPath(); context.ellipse(cx, cy, radius * .34, radius, 0, 0, TAU); context.stroke();
    context.beginPath(); context.moveTo(cx - radius * 1.18, cy); context.lineTo(cx + radius * 1.18, cy); context.stroke();
    context.beginPath(); context.moveTo(cx, cy - radius * 1.18); context.lineTo(cx, cy + radius * 1.18); context.stroke();

    const coherence = Math.max(.12, 1 - stage * .27);
    const angle = now * .00065;
    const vx = Math.cos(angle) * radius * coherence;
    const vy = -Math.sin(angle) * radius * .62 * coherence;
    const vector = context.createLinearGradient(cx, cy, cx + vx, cy + vy);
    vector.addColorStop(0, 'rgba(124,225,220,.3)');
    vector.addColorStop(1, 'rgba(124,225,220,1)');
    context.strokeStyle = vector;
    context.lineWidth = 1.8;
    context.beginPath(); context.moveTo(cx, cy); context.lineTo(cx + vx, cy + vy); context.stroke();
    context.fillStyle = 'rgba(124,225,220,1)';
    context.beginPath(); context.arc(cx + vx, cy + vy, 3.2, 0, TAU); context.fill();

    const fixedY = cy + radius * .76;
    context.fillStyle = 'rgba(222,190,125,1)';
    context.beginPath(); context.arc(cx, fixedY, 4.2, 0, TAU); context.fill();
    context.strokeStyle = 'rgba(222,190,125,.28)';
    context.lineWidth = 1;
    context.beginPath(); context.arc(cx, fixedY, 8 + Math.sin(now * .002) * 1.5, 0, TAU); context.stroke();

    context.fillStyle = 'rgba(201,215,215,.55)';
    context.font = `${Math.max(8, unit * .035)}px Consolas, monospace`;
    context.textAlign = 'center';
    context.fillText('ℋ', cx, cy - radius - 12);
    context.fillStyle = 'rgba(222,190,125,.72)';
    context.fillText('Fix(ℰ)', cx, Math.min(height - 12, fixedY + 22));
  }

  function loop(timestamp) {
    frame = 0;
    if (!running) return;
    if (timestamp - previous > 32) {
      previous = timestamp;
      render(timestamp * .001);
    }
    frame = requestAnimationFrame(loop);
  }

  function setRunning(value) {
    running = Boolean(value) && !reducedMotion.matches;
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    if (running) frame = requestAnimationFrame(loop);
    else render(time);
  }

  resize();
  window.addEventListener('resize', resize, { passive: true });
  setRunning(running);
  return {
    setStage(value) { stage = clamp(value, 0, 3); render(time); },
    setRunning,
    destroy() { setRunning(false); window.removeEventListener('resize', resize); }
  };
}
